from textual.widgets import Static, Button, RadioSet, RadioButton
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
    STEP_NUMBER = 2
    STEP_NAME = "Teclado"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Layout de Teclado", id="header-text"),
            Static(
                "Escolha o layout de teclado para a consola.\n"
                "Se usar um teclado português, escolha QWERTY (Portugal).",
                classes="help-text",
            ),
            RadioSet(
                *[RadioButton(kb[0], id=f"kb-{i}") for i, kb in enumerate(KEYBOARDS)],
                id="keyboard-list",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#kb-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_radio_index("#keyboard-list")
            self.app.config["keyboard"] = KEYBOARDS[idx][1]
            self.go_next("partition")
        elif event.button.id == "btn-back":
            self.go_back("language")

    def action_go_back(self) -> None:
        self.go_back("language")
