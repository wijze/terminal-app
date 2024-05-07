from enum import Enum


class ExecutableCommandData:
    def __init__(self, name, named_args, unnamed_args, modifiers):
        self.commandTree: str = name
        self.named_args = named_args
        self.unnamed_args = unnamed_args
        self.modifiers = modifiers

    def __str__(self):
        return f"Command: {self.commandTree}:\n {self.named_args} \n {self.unnamed_args} \n {self.modifiers}"


class ExecutableCommand:
    def __init__(self, interface_tree, name, data: ExecutableCommandData):
        self.interface_tree: list = interface_tree
        self.name = name
        self.data = data

    def layer_down(self) -> str:
        this_layer = self.interface_tree[0]
        self.interface_tree = self.interface_tree[1:]
        return this_layer


class FormalCommand:
    def __init__(self, name, exec_func, args):
        self.name = name
        self.exec = exec_func
        self.interface_tree = []
        self.args: list[FormalArgument] = args

    def add_interface_level(self, interface):
        self.interface_tree.append(interface)


class ArgumentType(Enum):
    STRING = 1
    NUMBER = 2
    BOOL = 3


class FormalArgument:
    def __init__(self, name, arg_type: ArgumentType, optional, default_val, unnamed_index) -> None:
        self.name = name
        self.type = arg_type
        self.optional = optional
        self.default = default_val
        self.unnamed_index = unnamed_index


def parse_inp(inp_str: str) -> ExecutableCommandData:
    unnamed_args = []
    modifiers = []
    named_args = {}

    parts = inp_str.split(" ")
    command = parts[0]
    parts = parts[1:]

    named_arg = ""
    for p in parts:
        if named_arg != "":
            if p.startswith("/") or p.startswith("-"):
                named_args[named_arg] = True
                named_arg = ""
            else:
                named_args[named_arg] = p
                named_arg = ""
                continue

        if p.startswith("/"):
            modifiers.append(p[1:])
        elif p.startswith("-"):
            named_arg = p[1:]
        else:
            unnamed_args.append(p)

    if named_arg != "":
        named_args[named_arg] = True

    return ExecutableCommandData(command, named_args, unnamed_args, modifiers)


def get_interface_tree(command: ExecutableCommandData):
    interface_tree = []
    for part in command.commandTree.split("."):
        interface_tree.append(part)

    name = interface_tree[-1]
    interface_tree = interface_tree[:-1]

    if len(interface_tree) > 0 and interface_tree[0] == "global":
        interface_tree = interface_tree[1:]

    return interface_tree, name


def get_args(ran_command: ExecutableCommand, formal_command: FormalCommand) -> dict:
    args = {}
    for arg in formal_command.args:
        found_arg = ""
        if arg.name in ran_command.data.named_args:
            found_arg = ran_command.data.named_args[arg.name]
        elif arg.unnamed_index < len(ran_command.data.unnamed_args):
            found_arg = ran_command.data.unnamed_args[arg.unnamed_index]
        elif arg.optional:
            found_arg = arg.default

        if found_arg:
            match arg.type:
                case ArgumentType.STRING:
                    pass
                case ArgumentType.NUMBER:
                    if found_arg.isnumeric():
                        found_arg = int(found_arg)
                    else:
                        raise Exception(f"invalid type of argument '{arg.name}': expected NUMBER")
                case ArgumentType.BOOL:
                    if found_arg == "false":
                        found_arg = False
                    elif found_arg == "true":
                        found_arg = True
                    else:
                        raise Exception(f"invalid type of argument '{arg.name}': expected BOOL")
                case _:
                    print("warning: found unknown argument type: ", arg.type)
        else:
            raise Exception(f"missing required arg: '{arg.name}' of command '{formal_command.name}'")

        args[arg.name] = found_arg

    return args
