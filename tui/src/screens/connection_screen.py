from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Input, Button
from textual.containers import Horizontal, Vertical, Container
import httpx

from src.utils import is_valid_url
from src.screens.modals.error_modal import ErrorModal


class ConnectionScreen(Screen):
    CSS_PATH = "./screens_styles.css"

    def compose(self) -> ComposeResult:
        yield Header()

        container = Vertical()
        container.border_title = "Proxy Api - Connection Screen"
        container.border_subtitle = "Semeq - PedroMartins - intern"
        with container:
            yield Container(Label("Insert the API URL: "), id="label")
            yield Input(
                value="http://localhost:8000",
                id="url_input",
                placeholder="http://localhost:8000",
            )
            yield Horizontal(
                Button(id="connect_button", label="Connect", variant="primary"),
                id="button_container",
            )

        yield Footer()

    @on(Button.Pressed, "#connect_button")
    @on(Input.Submitted, "#url_input")
    async def validate_connection(self) -> None:
        from src.globals import api_client

        input_widget = self.query_one("#url_input", Input)
        url = input_widget.value.strip()

        if not is_valid_url(url):
            self.app.notify(
                (
                    "[darkred bold]Invalid Url[/]: Url must start with "
                    + "[darkblue italic]http[/] or [darkblue italic]https[/] "
                    + "and be well-formed."
                ),
                title="CONNECTION ERROR",
                severity="error",
                timeout=3,
            )
            return

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                await client.get(f"{url}/")

        except (httpx.ConnectError, httpx.HTTPError):
            await self.show_error_modal("Could not reach the API with the given url.")
            return

        api_client.api_url = url
        self.notify("Login screen is required...", severity="warning")
        # TODO - Request login screen

    async def show_error_modal(self, message: str) -> None:
        await self.app.push_screen(ErrorModal("Connection Error", message))
