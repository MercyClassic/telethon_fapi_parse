from typing import Dict


class Cache:
    def __init__(self):
        self.__cache: Dict[int, Dict[str, str | bool]] = {}

    def set(self, data: Dict) -> None:
        self.__cache.update(data)

    def get(self, key: int) -> Dict[str, str | bool]:
        return self.__cache.get(key)

    def delete(self, key: id) -> None:
        self.__cache.pop(key, None)
