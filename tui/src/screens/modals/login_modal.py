from typing import Optional
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input

from src.screens.modals.error_modal import ErrorModal


class LoginModal(ModalScreen[None]):
    def __init__(self, label: Optional[str] = None, username: Optional[str] = None):
        self.__default_username: str = "" if username is None else username
        self.__label = label
        super().__init__()

    def compose(self) -> ComposeResult:
        from src.globals import api_client

        container = Vertical()
        container.border_title = "Authentication Screen"
        container.border_subtitle = api_client.api_url

        with container:
            yield Container(Label(f"{self.__label}"), id="label_container")

            yield Container(
                Horizontal(
                    Label("Username: "),
                    Input(
                        id="username_input",
                        value=self.__default_username,
                        placeholder="my_username",
                    ),
                    id="username_container",
                ),
                Horizontal(
                    Label("Password: "),
                    Input(
                        id="password_input", password=True, placeholder="my_password"
                    ),
                    id="password_container",
                ),
                Horizontal(
                    Button(id="login_button", label="Login", variant="primary"),
                    Button(id="exit_button", label="Exit", variant="error"),
                    id="button_container",
                ),
                id="login_container",
            )

    @on(Button.Pressed, "#exit_button")
    def exit_event(self) -> None:
        self.dismiss()
        self.app.uninstall_screen("login_modal")

    @on(Button.Pressed, "#login_button")
    @on(Input.Submitted, "#password_input")
    async def login(self):
        from src.globals import api_client

        username_input: Input = self.query_one("#username_input", Input)
        password_input: Input = self.query_one("#password_input", Input)

        username = username_input.value.strip()
        password = password_input.value.strip()

        if not username or not password:
            self.notify(
                "Please, enter both [darkred bold]username[/] and [darkred bold]password[/]",
                title="Missing Credentials",
                severity="error",
            )
            return

        result = await api_client.validate_credentials(password, username)

        if not result.state:
            await self.show_error_modal("Incorrect username or password.")

        else:
            self.dismiss()
            self.app.uninstall_screen("login_modal")
            self.app.notify(
                f"Successfully connected as [green bold italic]{username}[/].",
                title="Authentication Success",
                severity="information",
            )
            api_client.app.on_successful_login()

    async def show_error_modal(self, message: str) -> None:
        await self.app.push_screen(ErrorModal("Authentication Error", message))
