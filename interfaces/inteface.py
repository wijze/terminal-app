from command import FormalCommand, ExecutableCommand, get_args

from enum import Enum


class CommandSearchResult(Enum):
    NONE = 0
    MATCH = 1
    PARTIAL = 2


class Interface:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # set defaults
        self.sub_interfaces: dict[str, Interface] = {}
        self.commands: dict[str, FormalCommand] = {}
        self.name = ""
        self.is_global = False
        self.is_top_level = False  # only the global interface

        self.define_vars()

    def define_vars(self):
        # define sub_interfaces, commands, name
        pass

    def get_command(self, command: ExecutableCommand, should_log=True) -> CommandSearchResult:
        if len(command.interface_tree) == 0:
            if command.name in self.commands:
                self.exec_command(command)
                return CommandSearchResult.MATCH
            elif self.is_global:
                for i in self.sub_interfaces.values():
                    if i.get_command(command, False) == CommandSearchResult.MATCH:
                        return CommandSearchResult.MATCH
            if should_log:
                print(f"could not find the command '{command.name}' in interface '{self.name}'")
            return CommandSearchResult.NONE
        else:
            if command.interface_tree[0] in self.sub_interfaces:
                sub_interface = command.layer_down()
                res = self.sub_interfaces[sub_interface].get_command(command)
                command.layer_up()
                return res if res == CommandSearchResult.MATCH else CommandSearchResult.PARTIAL
            elif self.is_global:
                best = CommandSearchResult.NONE
                for i in self.sub_interfaces.values():
                    res = i.get_command(command, False)
                    if res == CommandSearchResult.MATCH:
                        return CommandSearchResult.MATCH
                    elif res == CommandSearchResult.PARTIAL:
                        best = res
                if self.is_top_level and best == CommandSearchResult.NONE:
                    print(f"could not find the sub interface '{command.interface_tree[0]}' in interface '{self.name}'")
            elif should_log:
                print(f"could not find the sub interface '{command.interface_tree[0]}' in interface '{self.name}'")
        return CommandSearchResult.NONE

    def exec_command(self, command):
        args: dict = get_args(command, self.commands[command.name])
        self.commands[command.name].exec(args)
