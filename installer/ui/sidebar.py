from textual.containers import Container
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static


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
    """Barra lateral com progresso visual. Atualiza automaticamente."""

    current_step = reactive(0)

    def __init__(self, step: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.current_step = step

    def compose(self):
        yield Static("  ⬡  ArchTUI", id="sidebar-title")
        yield Static("─" * 26, id="sidebar-subtitle")
        for number, name in STEPS:
            widget = Static(self._format_step(number, name), id=f"step-{number}")
            widget.add_class("step-item")
            widget.add_class(self._step_class(number))
            yield widget

    def update_step(self, step: int) -> None:
        """Atualiza o passo atual e re-renderiza os marcadores."""
        self.current_step = step
        for number, name in STEPS:
            try:
                widget = self.query_one(f"#step-{number}", Static)
                widget.update(self._format_step(number, name))
                widget.remove_class("step-completed", "step-active", "step-pending")
                widget.add_class(self._step_class(number))
            except Exception:
                pass

    def _format_step(self, number: int, name: str) -> str:
        if number < self.current_step:
            return f"  ✓  {number}. {name}"
        elif number == self.current_step:
            return f"  ▸  {number}. {name}"
        else:
            return f"  ○  {number}. {name}"

    def _step_class(self, number: int) -> str:
        if number < self.current_step:
            return "step-completed"
        elif number == self.current_step:
            return "step-active"
        return "step-pending"


class InstallerScreen(Screen):
    """Ecrã base para todos os passos do instalador."""

    STEP_NUMBER = 0
    STEP_NAME = ""

    def go_next(self, screen_name: str) -> None:
        """Avança para o próximo ecrã sem empilhar."""
        self.app.switch_screen(screen_name)

    def go_back(self, screen_name: str) -> None:
        """Volta ao ecrã anterior sem empilhar."""
        self.app.switch_screen(screen_name)

    def compose_with_sidebar(self, *content_widgets):
        """Monta o layout sidebar + conteúdo principal e atualiza o passo."""
        self.app.state["step"] = self.STEP_NUMBER
        sidebar = Sidebar(step=self.STEP_NUMBER, id="sidebar")
        yield sidebar
        yield Container(*content_widgets, id="main")
