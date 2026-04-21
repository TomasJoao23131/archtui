from textual.widgets import Static, Button, OptionList
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


KEYBOARDS = [
    ("ABNT (Brasil)", "br"),
    ("QWERTY (Portugal)", "pt-latin9"),
    ("QWERTY (US)", "us"),
    ("QWERTY (Espanha)", "es"),
]


class KeyboardScreen(InstallerScreen):
    STEP_NUMBER = 2
    STEP_NAME = "Teclado"

    def compose(self):
        content = Container(
            Static("Selecionar Layout de Teclado", id="header-text"),
            Static("Escolha o layout de teclado:", id="help-text"),
            OptionList(*[kb[0] for kb in KEYBOARDS], id="keyboard-list"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="keyboard-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            selected_index = self.get_highlighted_index("#keyboard-list")
            self.app.config["keyboard"] = KEYBOARDS[selected_index][1]
            self.app.push_screen("partition")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
