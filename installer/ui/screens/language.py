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
    ("Itáliano (Itália)", "it_IT"),
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

TIMEZONES = [
    # Europa Ocidental
    ("Europe/Lisbon — Portugal", "Europe/Lisbon"),
    ("Europe/London — Reino Unido", "Europe/London"),
    ("Europe/Madrid — Espanha", "Europe/Madrid"),
    ("Europe/Paris — França", "Europe/Paris"),
    ("Europe/Brussels — Bélgica", "Europe/Brussels"),
    ("Europe/Amsterdam — Paises Baixos", "Europe/Amsterdam"),
    # Europa Central
    ("Europe/Berlin — Alemanha", "Europe/Berlin"),
    ("Europe/Rome — Itália", "Europe/Rome"),
    ("Europe/Zurich — Suíça", "Europe/Zurich"),
    ("Europe/Vienna — Austria", "Europe/Vienna"),
    ("Europe/Warsaw — Polónia", "Europe/Warsaw"),
    ("Europe/Prague — Rep. Checa", "Europe/Prague"),
    ("Europe/Budapest — Hungria", "Europe/Budapest"),
    ("Europe/Stockholm — Suécia", "Europe/Stockholm"),
    ("Europe/Oslo — Noruega", "Europe/Oslo"),
    ("Europe/Copenhagen — Dinamarca", "Europe/Copenhagen"),
    ("Europe/Helsinki — Finlandia", "Europe/Helsinki"),
    # Europa de Leste
    ("Europe/Bucharest — Roménia", "Europe/Bucharest"),
    ("Europe/Athens — Grécia", "Europe/Athens"),
    ("Europe/Istanbul — Turquia", "Europe/Istanbul"),
    ("Europe/Moscow — Rússia", "Europe/Moscow"),
    ("Europe/Kyiv — Ucrânia", "Europe/Kyiv"),
    # Americas
    ("America/Sao_Paulo — Brasil (Brasilia)", "America/Sao_Paulo"),
    ("America/Fortaleza — Brasil (Nordeste)", "America/Fortaleza"),
    ("America/Manaus — Brasil (Amazonia)", "America/Manaus"),
    ("America/Buenos_Aires — Argentina", "America/Argentina/Buenos_Aires"),
    ("America/Mexico_City — Mexico", "America/Mexico_City"),
    ("America/Bogota — Colombia", "America/Bogota"),
    ("America/Lima — Peru", "America/Lima"),
    ("America/Santiago — Chile", "America/Santiago"),
    ("America/New_York — EUA (Leste)", "America/New_York"),
    ("America/Chicago — EUA (Centro)", "America/Chicago"),
    ("America/Denver — EUA (Montanha)", "America/Denver"),
    ("America/Los_Angeles — EUA (Pacifico)", "America/Los_Angeles"),
    ("America/Toronto — Canada (Leste)", "America/Toronto"),
    ("America/Vancouver — Canada (Pacifico)", "America/Vancouver"),
    # Asia
    ("Asia/Tokyo — Japão", "Asia/Tokyo"),
    ("Asia/Shanghai — China", "Asia/Shanghai"),
    ("Asia/Kolkata — India", "Asia/Kolkata"),
    ("Asia/Seoul — Coreia do Sul", "Asia/Seoul"),
    ("Asia/Bangkok — Tailandia", "Asia/Bangkok"),
    ("Asia/Ho_Chi_Minh — Vietname", "Asia/Ho_Chi_Minh"),
    ("Asia/Jakarta — Indonesia", "Asia/Jakarta"),
    ("Asia/Dubai — Emirados Árabes", "Asia/Dubai"),
    ("Asia/Riyadh — Arabia Saudita", "Asia/Riyadh"),
    ("Asia/Jerusalem — Israel", "Asia/Jerusalem"),
    # Africa / Oceania
    ("Africa/Cairo — Egito", "Africa/Cairo"),
    ("Africa/Johannesburg — África do Sul", "Africa/Johannesburg"),
    ("Austrália/Sydney — Austrália (Leste)", "Austrália/Sydney"),
    ("Pacific/Auckland — Nova Zelândia", "Pacific/Auckland"),
    # Universal
    ("UTC — Universal", "UTC"),
]


class LanguageScreen(InstallerScreen):
    STEP_NUMBER = 1
    STEP_NAME = "Idioma"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Idioma e Fuso Horario", id="header-text"),
            Static(
                "Escolha o idioma (locale) e o fuso horario do sistema.",
                classes="help-text",
            ),
            Static("Idioma:", classes="field-label"),
            RadioSet(
                *[RadioButton(lang[0], id=f"lang-{i}") for i, lang in enumerate(LANGUAGES)],
                id="language-list",
            ),
            Static("Fuso horário:", classes="field-label"),
            RadioSet(
                *[RadioButton(tz[0], id=f"tz-{i}") for i, tz in enumerate(TIMEZONES)],
                id="timezone-list",
            ),
            Horizontal(
                Button("← Anterior", id="btn-back", variant="default"),
                Button("Seguinte →", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#lang-0", RadioButton).value = True
        self.query_one("#tz-0", RadioButton).value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            lang_idx = self.get_radio_index("#language-list")
            tz_idx = self.get_radio_index("#timezone-list")
            self.app.config["language"] = LANGUAGES[lang_idx][1]
            self.app.config["timezone"] = TIMEZONES[tz_idx][1]
            self.go_next("keyboard")
        elif event.button.id == "btn-back":
            self.app.switch_screen("welcome")

    def action_go_back(self) -> None:
        self.app.switch_screen("welcome")
