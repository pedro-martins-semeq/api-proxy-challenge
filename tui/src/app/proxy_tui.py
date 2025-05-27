from textual.app import App

from src.globals import api_client
from src.screens.connection_screen import ConnectionScreen


class ProxyTUI(App):
    def on_mount(self):
        api_client.app = self

        self.install_screen(ConnectionScreen(), name="connection_screen")

        api_client.request_connection()

    def on_successful_login(self) -> None:
        self.notify("Navigate to main screen...")
