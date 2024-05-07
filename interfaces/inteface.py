from command import FormalCommand, ExecutableCommand, get_args


class Interface:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # set defaults
        self.sub_interfaces: dict[str, Interface] = {}
        self.commands: dict[str, FormalCommand] = {}
        self.name = ""
        self.is_global = False

        self.define_vars()

    def define_vars(self):
        # define sub_interfaces, commands, name
        pass

    def get_command(self, command: ExecutableCommand) -> bool:
        if len(command.interface_tree) == 0:
            if command.name in self.commands:
                self.exec_command(command)
                return True
            else:
                if self.is_global:
                    found = False
                    for i in self.sub_interfaces.values():
                        if i.get_command(command):
                            found = True
                            break
                    if found:
                        return True
                    else:
                        print(f"could not find the command '{command.name}' in interface '{self.name}'")
                else:
                    print(f"could not find the command '{command.name}' in interface '{self.name}'")
        else:
            if command.interface_tree[0] in self.sub_interfaces.keys():
                sub_interface = command.layer_down()
                return self.sub_interfaces[sub_interface].get_command(command)
            else:
                if self.is_global:
                    found = False
                    for i in self.sub_interfaces.values():
                        if i.get_command(command):
                            found = True
                            break
                    if found:
                        return True
                    else:
                        print(f"could not find the sub interface '{command.interface_tree[0]}' in interface '{self.name}'")

        return False

    def exec_command(self, command):
        args: dict = get_args(command, self.commands[command.name])
        self.commands[command.name].exec(args)
