from textual.widgets import Static, Button, OptionList
from textual.containers import Horizontal
from installer.ui.sidebar import InstallerScreen


KEYBOARDS = [
    ("ABNT2 (Brasil)", "br-abnt2"),
    ("QWERTY (Portugal)", "pt-latin9"),
    ("QWERTY (US Internacional)", "us"),
    ("QWERTY (Espanha)", "es"),
]


class KeyboardScreen(InstallerScreen):
    """Passo 2 — Layout de teclado."""

    STEP_NUMBER = 2
    STEP_NAME = "Teclado"

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Passo 2 — Layout de Teclado", id="header-text"),
            Static(
                "Escolha o layout de teclado para a consola do sistema.\n"
                "Se usar um teclado brasileiro, escolha ABNT2.\n"
                "Se usar um teclado português, escolha QWERTY (Portugal).",
                classes="help-text",
            ),
            OptionList(*[kb[0] for kb in KEYBOARDS], id="keyboard-list"),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            option_list = self.query_one("#keyboard-list", OptionList)
            idx = option_list.highlighted if option_list.highlighted is not None else 0
            self.app.config["keyboard"] = KEYBOARDS[idx][1]
            self.go_next("partition")
        elif event.button.id == "btn-back":
            self.go_back("language")
