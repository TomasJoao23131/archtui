import os
from installer.__version__ import __version__
from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import OptionList, RadioSet, SelectionList, Static


STEPS = [
    (1, "Idioma"),
    (2, "Teclado"),
    (3, "Partições"),
    (4, "Sistema base"),
    (5, "Bootloader"),
    (6, "Utilizador"),
    (7, "Desktop"),
    (8, "Confirmar"),
    (9, "Instalar"),
]


class Sidebar(Container):
    """Barra lateral com progresso."""

    current_step = reactive(0)

    def __init__(self, step: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.current_step = step

    def compose(self):
        yield Static("INSTALAÇÃO", id="sidebar-title")
        for number, name in STEPS:
            w = Static(self._fmt(number, name), id=f"step-{number}")
            w.add_class("step-item", self._cls(number))
            yield w

    def update_step(self, step: int) -> None:
        self.current_step = step
        for number, name in STEPS:
            try:
                w = self.query_one(f"#step-{number}", Static)
                w.update(self._fmt(number, name))
                w.remove_class("step-completed", "step-active", "step-pending")
                w.add_class(self._cls(number))
            except Exception:
                pass

    def _fmt(self, number: int, name: str) -> str:
        if number < self.current_step:
            return f" ✓ {name}"
        elif number == self.current_step:
            return f" ▸ {name}"
        return f" · {name}"

    def _cls(self, number: int) -> str:
        if number < self.current_step:
            return "step-completed"
        elif number == self.current_step:
            return "step-active"
        return "step-pending"


def _get_hostname() -> str:
    """Hostname real ou fallback."""
    try:
        return os.uname().nodename
    except AttributeError:
        import socket
        return socket.gethostname()


class InstallerScreen(Screen):
    """Base para todos os ecrãs do instalador."""

    STEP_NUMBER = 0
    STEP_NAME = ""

    def go_next(self, name: str) -> None:
        self.app.switch_screen(name)

    def go_back(self, name: str) -> None:
        self.app.switch_screen(name)

    def get_highlighted(self, selector: str) -> int:
        ol = self.query_one(selector, OptionList)
        return ol.highlighted if ol.highlighted is not None else 0

    def get_radio_index(self, selector: str) -> int:
        rs = self.query_one(selector, RadioSet)
        return rs.pressed_index if rs.pressed_index >= 0 else 0

    def get_selected_values(self, selector: str) -> list:
        sl = self.query_one(selector, SelectionList)
        return list(sl.selected)

    def compose_with_sidebar(self, *content_widgets):
        self.app.state["step"] = self.STEP_NUMBER
        host = _get_hostname()
        yield Static(f" ArchTUI v{__version__} — root@{host}", id="header-bar")
        yield Sidebar(step=self.STEP_NUMBER, id="sidebar")
        yield Container(
            *content_widgets,
            Static(
                "[Tab] navegar  [Enter] selecionar",
                classes="nav-hint",
            ),
            id="main",
        )
