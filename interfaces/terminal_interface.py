from interfaces.inteface import Interface
from command import FormalCommand, FormalArgument, ArgumentType


class TerminalInterface(Interface):
    def define_vars(self):
        self.name = "terminal"
        self.is_global = True
        self.commands = {
            "execute": FormalCommand("execute", self.execute_command, [
                FormalArgument("command", ArgumentType.STRING, True, "", 0)
            ])
        }

    def execute_command(self, args):
        self.app.enter_command(args["command"])
