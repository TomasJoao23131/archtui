class InstallerState:
    STEPS = [
        (1, "Idioma", "language"),
        (2, "Teclado", "keyboard"),
        (3, "Partições", "partition"),
        (4, "Sistema Base", "base"),
        (5, "Bootloader", "bootloader"),
        (6, "Utilizador", "user"),
        (7, "Ambiente", "desktop"),
        (8, "Resumo", "summary"),
        (9, "Instalação", "installation"),
    ]

    def __init__(self):
        self._data = {
            "step": 0,
            "step_name": "",
            "step_screen": "",
        }

    def set_step(self, step: int, name: str, screen: str) -> None:
        self._data["step"] = step
        self._data["step_name"] = name
        self._data["step_screen"] = screen

    def get_current_step(self) -> int:
        return self._data.get("step", 0)

    def get_total_steps(self) -> int:
        return len(self.STEPS)

    def get_progress(self) -> float:
        return (self.get_current_step() / self.get_total_steps()) * 100

    def get_name(self) -> str:
        return self._data.get("step_name", "")

    def to_dict(self) -> dict:
        return self._data.copy()