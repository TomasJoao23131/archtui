from textual.widgets import Static, Button, RadioSet, RadioButton
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from installer.ui.sidebar import InstallerScreen


# País -> lista de (nome da variante, keymap)
KEYBOARD_GROUPS = {
    "Portugal": [
        ("QWERTY", "pt-latin9"),
        ("QWERTY (no dead keys)", "pt-latin1"),
    ],
    "Brasil": [
        ("ABNT2", "br-abnt2"),
        ("ABNT2 (no dead keys)", "br-abnt2-ndeadkeys"),
    ],
    "EUA": [
        ("US QWERTY", "us"),
        ("US Internacional (dead keys)", "us-acentos"),
        ("Dvorak", "dvorak"),
        ("Colemak", "colemak"),
    ],
    "Reino Unido": [
        ("UK QWERTY", "uk"),
    ],
    "Espanha": [
        ("QWERTY", "es"),
        ("QWERTY (no dead keys)", "es-nodeadkeys"),
        ("Latinoamericano", "la-latin1"),
    ],
    "Franca": [
        ("AZERTY", "fr"),
        ("AZERTY (no dead keys)", "fr-nodeadkeys"),
        ("Belgica AZERTY", "be-latin1"),
    ],
    "Alemanha": [
        ("QWERTZ", "de"),
        ("QWERTZ (no dead keys)", "de-nodeadkeys"),
        ("Suica (Alemao)", "de_CH-latin1"),
        ("Suica (Frances)", "fr_CH"),
    ],
    "Italia": [
        ("QWERTY", "it"),
    ],
    "Paises Baixos": [
        ("QWERTY", "nl"),
    ],
    "Suecia": [
        ("Sueco", "sv-latin1"),
    ],
    "Noruega": [
        ("Noruegues", "no"),
    ],
    "Dinamarca": [
        ("Dinamarques", "dk"),
    ],
    "Finlandia": [
        ("Finlandes", "fi"),
    ],
    "Islandia": [
        ("Islandes", "is-latin1"),
    ],
    "Polonia": [
        ("Polaco", "pl"),
    ],
    "Republica Checa": [
        ("QWERTZ", "cz-qwertz"),
        ("QWERTY", "cz-lat2"),
    ],
    "Eslovaquia": [
        ("QWERTY", "sk-qwerty"),
    ],
    "Hungria": [
        ("Hungaro", "hu"),
    ],
    "Romenia": [
        ("Romeno", "ro"),
    ],
    "Croacia": [
        ("Croata", "croat"),
    ],
    "Eslovenia": [
        ("Esloveno", "slovene"),
    ],
    "Servia": [
        ("Latim", "sr-latin"),
    ],
    "Russia": [
        ("Russo", "ru"),
    ],
    "Ucrania": [
        ("Ucraniano", "ua-utf"),
    ],
    "Bulgaria": [
        ("Fonetico", "bg_pho-utf8"),
    ],
    "Turquia": [
        ("Turco Q", "trq"),
        ("Turco F", "trf"),
    ],
    "Grecia": [
        ("Grego", "gr"),
    ],
    "Japao": [
        ("Japones (106 teclas)", "jp106"),
    ],
    "Coreia do Sul": [
        ("Coreano (104 teclas)", "kr104"),
    ],
    "India": [
        ("Devanagari", "in-eng"),
    ],
    "Tailandia": [
        ("Tailandes", "th-tis"),
    ],
    "Vietname": [
        ("Vietnamita", "vn"),
    ],
    "Arabia Saudita": [
        ("Arabe", "arabic"),
    ],
    "Israel": [
        ("Hebraico", "il"),
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
            else:
                self.app.config["keyboard"] = variants[0][1] if variants else "us"
            self.go_next("partition")
        elif event.button.id == "btn-back":
            self.go_back("language")

    def action_go_back(self) -> None:
        self.go_back("language")
