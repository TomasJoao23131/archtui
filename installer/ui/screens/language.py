from textual.widgets import Static, Button, RadioSet, RadioButton
from textual.containers import Horizontal
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


LANGUAGES = [
    ("Português (Brasil)", "pt_BR"),
    ("Português (Portugal)", "pt_PT"),
    ("English (US)", "en_US"),
    ("English (UK)", "en_GB"),
    ("Español (España)", "es_ES"),
    ("Español (México)", "es_MX"),
    ("Español (Argentina)", "es_AR"),
    ("Français (France)", "fr_FR"),
    ("Deutsch (Deutschland)", "de_DE"),
    ("Italiano (Italia)", "it_IT"),
    ("Nederlands (Nederland)", "nl_NL"),
    ("Русский (Россия)", "ru_RU"),
    ("日本語 (日本)", "ja_JP"),
    ("中文 (简体, 中国)", "zh_CN"),
    ("中文 (繁體, 台灣)", "zh_TW"),
    ("한국어 (대한민국)", "ko_KR"),
    ("العربية (مصر)", "ar_EG"),
    ("Polski (Polska)", "pl_PL"),
    ("Čeština (Česko)", "cs_CZ"),
    ("Svenska (Sverige)", "sv_SE"),
    ("Norsk bokmål (Norge)", "nb_NO"),
    ("Dansk (Danmark)", "da_DK"),
    ("Suomi (Suomi)", "fi_FI"),
    ("Magyar (Magyarország)", "hu_HU"),
    ("Română (România)", "ro_RO"),
    ("Türkçe (Türkiye)", "tr_TR"),
    ("Ελληνικά (Ελλάδα)", "el_GR"),
    ("Українська (Україна)", "uk_UA"),
    ("Català (Catalunya)", "ca_ES"),
    ("Galego (Galiza)", "gl_ES"),
    ("Euskara (Euskal Herria)", "eu_ES"),
    ("Bahasa Indonesia", "id_ID"),
    ("Tiếng Việt (Việt Nam)", "vi_VN"),
    ("ภาษาไทย (ประเทศไทย)", "th_TH"),
    ("हिन्दी (भारत)", "hi_IN"),
]


class LanguageScreen(InstallerScreen):
    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Idioma do sistema", id="header-text"),
            Static(
                "Escolha o idioma que será configurado no sistema instalado.\n"
                "Isto define o locale (formato de datas, números e mensagens).",
                classes="help-text",
            ),
            RadioSet(
                *[RadioButton(lang[0], id=f"lang-{i}") for i, lang in enumerate(LANGUAGES)],
                id="language-list",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#lang-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            idx = self.get_radio_index("#language-list")
            self.app.config["language"] = LANGUAGES[idx][1]
            self.go_next("keyboard")
        elif event.button.id == "btn-back":
            self.app.switch_screen("welcome")

    def action_go_back(self) -> None:
        self.app.switch_screen("welcome")
