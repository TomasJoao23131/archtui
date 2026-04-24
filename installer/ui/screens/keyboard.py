from textual.widgets import Static, Button, OptionList
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


KEYBOARDS = [
    ("ABNT2 (Brasil)", "br-abnt2"),
    ("QWERTY (Portugal)", "pt-latin9"),
    ("QWERTY (US Internacional)", "us"),
    ("QWERTY (Espanha)", "es"),
]


class KeyboardScreen(InstallerScreen):
    """Passo 2 — Layout de teclado. Enter na lista avança."""

    STEP_NUMBER = 2
    STEP_NAME = "Teclado"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 2 — Layout de Teclado", id="header-text"),
            Static(
                "Escolha o layout de teclado para a consola.\n"
                "Use ↑↓ para navegar e Enter para confirmar e avançar.",
                classes="help-text",
            ),
            OptionList(*[kb[0] for kb in KEYBOARDS], id="keyboard-list"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "keyboard-list":
            self.app.config["keyboard"] = KEYBOARDS[event.option_index][1]
            self.go_next("partition")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_highlighted("#keyboard-list")
            self.app.config["keyboard"] = KEYBOARDS[idx][1]
            self.go_next("partition")
        elif event.button.id == "btn-back":
            self.go_back("language")

    def action_go_back(self) -> None:
        self.go_back("language")
