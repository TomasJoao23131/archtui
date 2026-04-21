from textual.containers import Container
from textual.screen import Screen
from textual.widgets import OptionList, SelectionList, Static


STEPS_SIDEBAR = [
    "1. Idioma",
    "2. Teclado",
    "3. Partições",
    "4. Sistema Base",
    "5. Bootloader",
    "6. Utilizador",
    "7. Ambiente",
    "8. Resumo",
    "9. Instalação",
]


class Sidebar(Container):
    def __init__(self, state: dict, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def compose(self):
        yield Static("ArchTUI", id="sidebar-title")
        yield Static("Progresso", id="sidebar-subtitle")
        for i, step in enumerate(STEPS_SIDEBAR, 1):
            is_active = self.state.get("step", 0) == i
            is_completed = self.state.get("step", 0) > i
            marker = "[✓]" if is_completed else "[ ]" if not is_active else "[>"
            yield Static(f"{marker} {step}", id=f"step-{i}")


class InstallerScreen(Screen):
    STEP_NUMBER = 0
    STEP_NAME = ""

    def set_current_step(self) -> None:
        if self.STEP_NUMBER:
            self.app.state["step"] = self.STEP_NUMBER
            self.app.state["step_name"] = self.STEP_NAME

    def get_highlighted_index(self, selector: str) -> int:
        option_list = self.query_one(selector, OptionList)
        return option_list.highlighted if option_list.highlighted is not None else 0

    def get_selected_values(self, selector: str) -> list:
        selection_list = self.query_one(selector, SelectionList)
        return list(selection_list.selected)

    def compose_with_sidebar(self, content: Container):
        self.set_current_step()
        yield Sidebar(self.app.state, id="sidebar")
        yield Container(content, id="main")
