from typing import Set
from PySide2 import QtCore


class KeyEventHandler:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

        self.pressed_keys: Set[QtCore.Qt.Key] = set()

    def get_pressed_keys(self):
        return self.pressed_keys

    def add_pressed_key(self, key: QtCore.Qt.Key):
        self.pressed_keys.add(key)

    def remove_pressed_key(self, key: QtCore.Qt.Key):
        self.pressed_keys.remove(key)
