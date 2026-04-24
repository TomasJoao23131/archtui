from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import OptionList, SelectionList, Static


STEPS = [
    (1, "Idioma"),
    (2, "Teclado"),
    (3, "Partições"),
    (4, "Sistema Base"),
    (5, "Bootloader"),
    (6, "Utilizador"),
    (7, "Ambiente"),
    (8, "Resumo"),
    (9, "Instalação"),
]


class Sidebar(Container):
    """Barra lateral com progresso visual."""

    current_step = reactive(0)

    def __init__(self, step: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.current_step = step

    def compose(self):
        yield Static("  ⬡  ArchTUI", id="sidebar-title")
        yield Static("─" * 26, id="sidebar-subtitle")
        for number, name in STEPS:
            widget = Static(self._format(number, name), id=f"step-{number}")
            widget.add_class("step-item")
            widget.add_class(self._cls(number))
            yield widget

    def update_step(self, step: int) -> None:
        self.current_step = step
        for number, name in STEPS:
            try:
                w = self.query_one(f"#step-{number}", Static)
                w.update(self._format(number, name))
                w.remove_class("step-completed", "step-active", "step-pending")
                w.add_class(self._cls(number))
            except Exception:
                pass

    def _format(self, number: int, name: str) -> str:
        if number < self.current_step:
            return f"  ✓  {number}. {name}"
        elif number == self.current_step:
            return f"  ▸  {number}. {name}"
        return f"     {number}. {name}"

    def _cls(self, number: int) -> str:
        if number < self.current_step:
            return "step-completed"
        elif number == self.current_step:
            return "step-active"
        return "step-pending"


class InstallerScreen(Screen):
    """Ecrã base com helpers de navegação."""

    STEP_NUMBER = 0
    STEP_NAME = ""

    def go_next(self, screen_name: str) -> None:
        self.app.switch_screen(screen_name)

    def go_back(self, screen_name: str) -> None:
        self.app.switch_screen(screen_name)

    def get_highlighted(self, selector: str) -> int:
        ol = self.query_one(selector, OptionList)
        return ol.highlighted if ol.highlighted is not None else 0

    def get_selected_values(self, selector: str) -> list:
        sl = self.query_one(selector, SelectionList)
        return list(sl.selected)

    def compose_with_sidebar(self, *content_widgets):
        self.app.state["step"] = self.STEP_NUMBER
        yield Sidebar(step=self.STEP_NUMBER, id="sidebar")
        yield Container(
            *content_widgets,
            Static("Tab: navegar campos │ Enter: confirmar │ ↑↓: opções", classes="nav-hint"),
            id="main",
        )
