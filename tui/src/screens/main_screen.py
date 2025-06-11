from typing import Optional, List, Dict, Union

from textual import on
from textual.app import ComposeResult
from textual.containers import (
    Container,
    Horizontal,
    HorizontalScroll,
    Vertical,
    VerticalScroll,
)
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Link
from textual.widget import Widget

from src.api_client.api_client import APIClient
from src.screens.modals.implantation_tree_modal import ImplantationTreeModal


class UserInfoContainer(Vertical):
    def __init__(self, user: Optional[Dict[str, Union[int, str]]]):
        super().__init__()

        def _default(x: str):
            return user.get(x) if user is not None else "Loading..."

        self._id = _default("id")
        self._username = _default("username")
        self._first_name = _default("first_name")
        self._last_name = _default("last_name")
        self._email = _default("email")

        self.border_title = "User"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Label(f"User: {self._username}",
                      markup=False, id="username_label"),
                Label(f"id: {self._id}", markup=False, id="id_label"),
                id="username_container",
            ),
            Vertical(
                Label(f"{self._first_name} {self._last_name}",
                      id="fullname_label"),
                Link(f"{self._email}", id="email_label"),
                id="user_identity_container",
            ),
            id="user_info_content",
        )


class CorporationContainer(VerticalScroll):
    def __init__(self, corporation: Optional[List[Dict[str, Union[str, int]]]]):
        super().__init__()
        self._corporation: Optional[List[Dict[str, Union[str, int]]]] = (
            corporation if corporation is not None else None
        )

    def compose(self) -> ComposeResult:
        if self._corporation is not None:
            for corp in self._corporation:
                name = corp.get("name")
                id = corp.get("id")
                yield Horizontal(
                    Label(f"{name}", classes="corp_name"),
                    Label(f"Id: {id}", classes="corp_id"),
                    classes="corp_container",
                )
        self.border_title = "Corporations"


class GetTreeClicked(Message):
    def __init__(self, sender: Widget, site_id):
        super().__init__()
        self.sender: Widget = sender
        self.site_id: int = site_id


class SiteWidget(Horizontal):
    def __init__(self, site: Dict):
        super().__init__()
        self.site = site

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Container(Label(f"Id: {self.site.get('id')}"), classes="corp_id"),
            HorizontalScroll(
                Container(Label(f"{self.site.get('name')}"),
                          classes="corp_name"),
            ),
            Container(
                Label(f"Corp: {self.site.get('corporation')}"),
                classes="corporation",
            ),
            Container(
                Button(
                    "Get Tree",
                    variant="default",
                    classes="get_tree_button",
                ),
                classes="button_container",
            ),
        )

    @on(Button.Pressed, ".get_tree_button")
    def get_tree_event(self) -> None:
        self.post_message(GetTreeClicked(self, site_id=self.site.get("id")))


class SitesContainer(VerticalScroll):
    def __init__(
        self,
        sites: Optional[List[Dict[str, Union[str, int]]]],
        id: Optional[str] = None,
    ):
        super().__init__(id=id)
        self._sites: Optional[List[Dict[str, Union[str, int]]]] = sites

        self.border_title = "Sites"


class MainScreen(Screen):
    CSS_PATH = "./screens_styles.css"

    def __init__(self, api_client: APIClient):
        super().__init__()
        self._api_client: APIClient = api_client
        self._user = {}
        self._corporation = {}
        self._sites = [{}]

    async def _usercorp_data_request(self) -> APIClient.Response:
        response = await self._api_client.usercorp_request()

        return response

    async def _implantation_mobile_tree_request(self, site_id: int) -> APIClient.Response:
        response: APIClient.Response = await self._api_client.implantation_mobile_tree_request(site_id)

        return response

    def compose(self) -> ComposeResult:
        yield Header()

        yield Container(
            HorizontalScroll(id="user_info_container"), id="header_container"
        )

        yield Container(SitesContainer([], id="sites_container"), id="sites")

        yield Footer()

    async def on_mount(self) -> None:
        response = await self._usercorp_data_request()

        self._user = response.body.get("user")
        self._corporation = response.body.get("corporation")
        self._sites = response.body.get("sites")

        user_info_container = self.query_one(
            "#user_info_container", HorizontalScroll)
        user_info_container.mount(UserInfoContainer(self._user))
        user_info_container.mount(CorporationContainer(self._corporation))

        sites_container = self.query_one("#sites_container", SitesContainer)
        if self._sites is not None:
            for site in self._sites:
                await sites_container.mount(SiteWidget(site))

    def on_get_tree_clicked(self, message: GetTreeClicked) -> None:
        site_id = message.site_id

        clicked_button: Button = message.sender.query_one(".get_tree_button", Button)
        clicked_button.loading = True

        for button in self.query(".get_tree_button").results(Button):
            button.disabled = True

        self.run_worker(self._get_tree_request(site_id, clicked_button), exclusive=True)

    async def _get_tree_request(self, site_id: int, loading_container: Widget):
        response = await self._implantation_mobile_tree_request(site_id)

        if not response.state:
            self.notify(
                f"Couldn't find site with id {site_id}",
                title="Error",
                severity="error",
                timeout=3,
            )
        else:
            self.app.install_screen(
                ImplantationTreeModal(response.body), name="implantation_tree_modal"
            )
            self.app.push_screen("implantation_tree_modal")

        for button in self.query(".get_tree_button").results(Button):
            button.disabled = False
        loading_container.loading = False

