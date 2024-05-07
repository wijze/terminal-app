from command import FormalCommand
from interfaces.inteface import Interface
from interfaces.builtin_interface import BuiltinInterface


class GlobalInterface(Interface):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.callable_commands = []

    def define_vars(self):
        self.name = "global"
        self.is_global = True
        self.sub_interfaces = {
            "builtin": BuiltinInterface(self, self.app)
        }
