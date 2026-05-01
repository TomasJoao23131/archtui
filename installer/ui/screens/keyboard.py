from textual.widgets import Static, Button, RadioSet, RadioButton
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


# País -> lista de (nome da variante, keymap_consola, xkb_layout:xkb_variant)
KEYBOARD_GROUPS = {
    "Portugal": [
        ("QWERTY", "pt-latin9", "pt:"),
        ("QWERTY (no dead keys)", "pt-latin1", "pt:nodeadkeys"),
    ],
    "Brasil": [
        ("ABNT2", "br-abnt2", "br:"),
        ("ABNT2 (no dead keys)", "br-abnt2", "br:nodeadkeys"),
    ],
    "EUA": [
        ("US QWERTY", "us", "us:"),
        ("US Internacional (dead keys)", "us-acentos", "us:intl"),
        ("Dvorak", "dvorak", "us:dvorak"),
        ("Colemak", "colemak", "us:colemak"),
    ],
    "Reino Unido": [
        ("UK QWERTY", "uk", "gb:"),
    ],
    "Espanha": [
        ("QWERTY", "es", "es:"),
        ("QWERTY (no dead keys)", "es-nodeadkeys", "es:nodeadkeys"),
        ("Latinoamericano", "la-latin1", "latam:"),
    ],
    "Franca": [
        ("AZERTY", "fr", "fr:"),
        ("AZERTY (no dead keys)", "fr-nodeadkeys", "fr:nodeadkeys"),
        ("Belgica AZERTY", "be-latin1", "be:"),
    ],
    "Alemanha": [
        ("QWERTZ", "de", "de:"),
        ("QWERTZ (no dead keys)", "de-nodeadkeys", "de:nodeadkeys"),
        ("Suica (Alemao)", "de_CH-latin1", "ch:de"),
        ("Suica (Frances)", "fr_CH", "ch:fr"),
    ],
    "Italia": [
        ("QWERTY", "it", "it:"),
    ],
    "Paises Baixos": [
        ("QWERTY", "nl", "nl:"),
    ],
    "Suecia": [
        ("Sueco", "sv-latin1", "se:"),
    ],
    "Noruega": [
        ("Noruegues", "no", "no:"),
    ],
    "Dinamarca": [
        ("Dinamarques", "dk", "dk:"),
    ],
    "Finlandia": [
        ("Finlandes", "fi", "fi:"),
    ],
    "Islandia": [
        ("Islandes", "is-latin1", "is:"),
    ],
    "Polonia": [
        ("Polaco", "pl", "pl:"),
    ],
    "Republica Checa": [
        ("QWERTZ", "cz-qwertz", "cz:qwerty"),
        ("QWERTY", "cz-lat2", "cz:"),
    ],
    "Eslovaquia": [
        ("QWERTY", "sk-qwerty", "sk:"),
    ],
    "Hungria": [
        ("Hungaro", "hu", "hu:"),
    ],
    "Romenia": [
        ("Romeno", "ro", "ro:"),
    ],
    "Croacia": [
        ("Croata", "croat", "hr:"),
    ],
    "Eslovenia": [
        ("Esloveno", "slovene", "si:"),
    ],
    "Servia": [
        ("Latim", "sr-latin", "rs:latin"),
    ],
    "Russia": [
        ("Russo", "ru", "ru:"),
    ],
    "Ucrania": [
        ("Ucraniano", "ua-utf", "ua:"),
    ],
    "Bulgaria": [
        ("Fonetico", "bg_pho-utf8", "bg:phonetic"),
    ],
    "Turquia": [
        ("Turco Q", "trq", "tr:"),
        ("Turco F", "trf", "tr:f"),
    ],
    "Grecia": [
        ("Grego", "gr", "gr:"),
    ],
    "Japao": [
        ("Japones (106 teclas)", "jp106", "jp:"),
    ],
    "Coreia do Sul": [
        ("Coreano (104 teclas)", "kr104", "kr:"),
    ],
    "India": [
        ("Devanagari", "in-eng", "in:"),
    ],
    "Tailandia": [
        ("Tailandes", "th-tis", "th:"),
    ],
    "Vietname": [
        ("Vietnamita", "vn", "vn:"),
    ],
    "Arabia Saudita": [
        ("Arabe", "arabic", "ara:"),
    ],
    "Israel": [
        ("Hebraico", "il", "il:"),
    ],
}

COUNTRY_LIST = list(KEYBOARD_GROUPS.keys())


class KeyboardScreen(InstallerScreen):
    STEP_NUMBER = 2
    STEP_NAME = "Teclado"

    BINDINGS = [
        Binding("escape", "go_back", "Voltar", show=False),
    ]

    def __init__(self):
        super().__init__()
        self._selected_country = COUNTRY_LIST[0]
        self._variant_counter = 0

    def compose(self):
        yield from self.compose_with_sidebar(
            Static("Layout de Teclado", id="header-text"),
            Static(
                "Seleciona o pais a esquerda e a variante a direita.",
                classes="help-text",
            ),
            Horizontal(
                Vertical(
                    Static("Pais / Regiao:", classes="field-label"),
                    RadioSet(
                        *[RadioButton(c, id=f"country-{i}") for i, c in enumerate(COUNTRY_LIST)],
                        id="country-list",
                    ),
                    id="kb-left-panel",
                ),
                Vertical(
                    Static("Variante:", classes="field-label"),
                    Container(id="variant-container"),
                    id="kb-right-panel",
                ),
                id="kb-panels",
            ),
            Horizontal(
                Button("<- Anterior", id="btn-back", variant="default"),
                Button("Seguinte ->", id="btn-next", variant="primary"),
                id="nav-buttons",
            ),
        )

    def on_mount(self):
        self.query_one("#country-0", RadioButton).value = True
        self._update_variants()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id == "country-list":
            idx = event.radio_set.pressed_index
            if 0 <= idx < len(COUNTRY_LIST):
                self._selected_country = COUNTRY_LIST[idx]
                self._update_variants()

    def _update_variants(self) -> None:
        container = self.query_one("#variant-container")
        # Remover qualquer RadioSet existente antes de montar um novo
        for old in container.query("RadioSet"):
            old.remove()
        self._variant_counter += 1
        variants = KEYBOARD_GROUPS.get(self._selected_country, [])
        vid = f"variant-list-{self._variant_counter}"
        radios = [RadioButton(v[0], id=f"var-{self._variant_counter}-{i}") for i, v in enumerate(variants)]
        rs = RadioSet(*radios, id=vid)
        container.mount(rs)
        if radios:
            radios[0].value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-next":
            variants = KEYBOARD_GROUPS.get(self._selected_country, [])
            try:
                vid = f"variant-list-{self._variant_counter}"
                rs = self.query_one(f"#{vid}", RadioSet)
                idx = rs.pressed_index if rs.pressed_index >= 0 else 0
            except Exception:
                idx = 0
            if idx < len(variants):
                self.app.config["keyboard"] = variants[idx][1]
                self.app.config["xkb_layout"] = variants[idx][2]
            else:
                self.app.config["keyboard"] = variants[0][1] if variants else "us"
                self.app.config["xkb_layout"] = variants[0][2] if variants else "us:"
            self.go_next("partition")
        elif event.button.id == "btn-back":
            self.go_back("language")

    def action_go_back(self) -> None:
        self.go_back("language")
