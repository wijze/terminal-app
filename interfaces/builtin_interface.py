from interfaces.inteface import Interface
from command import FormalCommand, FormalArgument, ArgumentType
from interfaces.test_interface import TestInterface

from time import sleep


class BuiltinInterface(Interface):
    def define_vars(self):
        self.name = "test"
        self.is_global = True
        self.sub_interfaces = {
            "test": TestInterface(self, self.app)
        }
        self.commands = {
            "exit": FormalCommand("exit", self.exit, [
                FormalArgument("delay", ArgumentType.NUMBER, True, 0, 0)])
        }

    def exit(self, args):
        sleep(args["delay"])
        self.app.exit()