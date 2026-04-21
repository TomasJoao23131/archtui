from textual.widgets import Static, Button, OptionList
from textual.containers import Container, Horizontal
from installer.ui.sidebar import InstallerScreen


LANGUAGES = [
    ("Portugues (Brasil)", "pt_BR"),
    ("Portugues (Portugal)", "pt_PT"),
    ("English (US)", "en_US"),
    ("Espanol", "es_ES"),
]


class LanguageScreen(InstallerScreen):
    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    def compose(self):
        content = Container(
            Static("Selecionar Idioma", id="header-text"),
            Static("Escolha o idioma do sistema:", id="help-text"),
            OptionList(*[lang[0] for lang in LANGUAGES], id="language-list"),
            Horizontal(
                Button("Anterior", id="btn-back", variant="default"),
                Button("Seguinte", id="btn-next", variant="primary"),
                id="nav-buttons"
            ),
            id="language-container"
        )
        yield from self.compose_with_sidebar(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            selected_index = self.get_highlighted_index("#language-list")
            self.app.config["language"] = LANGUAGES[selected_index][1]
            self.app.push_screen("keyboard")
        elif event.button.id == "btn-back":
            self.app.pop_screen()
