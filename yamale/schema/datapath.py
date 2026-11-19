class DataPath(object):
    def __init__(self, *path: object) -> None:
        self._path = path

    def __add__(self, other: "DataPath") -> "DataPath":
        dp = DataPath()
        dp._path = self._path + other._path
        return dp

    def __str__(self) -> str:
        return ".".join(map(str, (self._path)))

    def __repr__(self) -> str:
        return "DataPath({})".format(repr(self._path))
