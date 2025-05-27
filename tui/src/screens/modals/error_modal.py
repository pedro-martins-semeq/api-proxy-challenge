from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ErrorModal(ModalScreen[None]):
    def __init__(self, title: str, message: str, subtitle: str | None = None):
        self.__message: str = message
        self.__title: str = title
        self.__subtitle: str | None = subtitle
        super().__init__()

    def compose(self) -> ComposeResult:
        container = Vertical()
        container.border_title = self.__title
        if self.__subtitle is not None:
            container.border_subtitle = self.__subtitle

        with container:
            yield Container(
                Label(
                    f"[red bold]{self.__message}[/]",
                    id="message",
                ),
                id="label",
            )
            yield Horizontal(
                Button(label="Close", variant="error", id="close_button"),
                id="button_container",
            )

    @on(Button.Pressed, "#close_button")
    def close_dialog(self) -> None:
        self.dismiss()
