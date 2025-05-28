from typing import Optional, List, Dict, Union, Any

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Collapsible, Label


class ImplantationTreeModal(ModalScreen):
    CSS_PATH = "./modals_styles.css"

    def __init__(self, implantation_tree: dict):
        super().__init__()

        def _default(x: str):
            return (
                implantation_tree.get(x)
                if implantation_tree is not None
                else "Loading..."
            )

        self._id = _default("id")
        self._name = _default("name")
        self._revision = _default("revision")

        tree = implantation_tree.get("tree")
        self._tree: Union[Dict, List] = tree if tree is not None else []

        self._page_size = 25
        self._index_start: int = 0
        self._total: int = len(self._tree) if isinstance(
            self._tree, list) else 1
        self._total_pages: int = max(
            1, (self._total + self._page_size - 1) // self._page_size
        )

    def compose(self) -> ComposeResult:
        modal_container = Vertical(
            Horizontal(
                Label(f"Site: {self._id}", id="site_id_label"),
                Label(f"{self._name}", id="name_label"),
                Label(f"Revision: {self._revision}", id="revision_label"),
                id="header_container",
            ),
            JsonViewer(
                self._tree,
                range_start=self._index_start,
                range_end=self._index_start + self._page_size,
                id="asset_container",
            ),
            Vertical(
                Horizontal(
                    Button("Prev", variant="default", id="prev_button"),
                    Label(
                        f"{self._current_page + 1}/{self._total_pages}", id="page_label"
                    ),
                    Button("Next", variant="default", id="next_button"),
                    id="navigation_buttons_container",
                ),
                Container(
                    Button("Close", variant="primary", id="close_button"),
                    id="close_button_container",
                ),
                id="buttons_container",
            ),
            id="modal_container",
        )

        modal_container.border_title = f"Implantation Mobile Tree - Site: {self._id}"
        yield modal_container

    @property
    def _current_page(self) -> int:
        return self._index_start // self._page_size

    def _update_viewer(self):
        container = self.query_one("#asset_container", JsonViewer)
        container.remove_children()
        tree = self._tree
        if isinstance(tree, list):
            page_data = tree[self._index_start: self._index_start +
                             self._page_size]
        else:
            page_data = tree

        for item in container._render_json(page_data):
            container.mount(item)

        self.query_one("#page_label", Label).update(
            f"{self._current_page + 1}/{self._total_pages}"
        )

    @on(Button.Pressed, "#close_button")
    def close_modal(self):
        self.dismiss()
        self.app.uninstall_screen("implantation_tree_modal")

    @on(Button.Pressed, "#next_button")
    def next_page(self):
        if self._index_start + self._page_size < self._total:
            self._index_start += self._page_size
            self._update_viewer()

    @on(Button.Pressed, "#prev_button")
    def prev_page(self):
        if self._index_start - self._page_size >= 0:
            self._index_start -= self._page_size
            self._update_viewer()


class JsonViewer(VerticalScroll):
    def __init__(
        self,
        tree: Union[Dict, List],
        range_start: Optional[int] = None,
        range_end: Optional[int] = None,
        id: Optional[str] = None,
    ):
        super().__init__(id=id)
        self._tree = tree
        self._range_start = range_start
        self._range_end = range_end

    def compose(self) -> ComposeResult:
        if isinstance(self._tree, list) and self._range_start is not None:
            self._tree = self._tree[self._range_start: self._range_end]

        yield from self._render_json(self._tree)

    def _render_json(self, tree: Any, depth: int = 0):
        if isinstance(tree, dict):
            for key, value in tree.items():
                if isinstance(value, list):
                    yield Collapsible(
                        Label(f"[bold]{key}[/bold] (list)"),
                        *self._render_json(value, depth + 1),
                        title=key,
                    )
                elif isinstance(value, dict):
                    yield Collapsible(
                        Label(f"[bold]{key}[/bold] (dict)"),
                        *self._render_json(value, depth + 1),
                        title=key,
                    )
                else:
                    yield Container(Label(f"{' ' * depth}{key}: {value}"))
        elif isinstance(tree, list):
            for index, item in enumerate(tree):
                if isinstance(item, (dict, list)):
                    if isinstance(item, dict):
                        label = f"{item.get('name')} | Id: {item.get('id')}"
                    else:
                        label = None

                    title = label if label is not None else f"Item {index}"
                    yield Collapsible(
                        *self._render_json(item, depth + 1),
                        title=title,
                    )
                else:
                    yield Container(Label(f"{' ' * depth} - {item}"))
        else:
            yield Container(Label(str(tree)))
