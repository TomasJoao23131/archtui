class InstallerConfig:
    def __init__(self):
        self._data = {}

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value

    def update(self, data: dict) -> None:
        self._data.update(data)

    def to_dict(self) -> dict:
        return self._data.copy()