from textual.app import App, ComposeResult
from textual.widgets import Label

from src.globals import api_client


class ProxyTUI(App):
    def compose(self) -> ComposeResult:
        yield Label("PROXY CLIENT TUI")

    def on_mount(self):
        api_client.app = self
