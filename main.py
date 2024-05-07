from command import ExecutableCommand, parse_inp, get_interface_tree
from interfaces.global_interface import GlobalInterface


def main():
    app = App()
    app.main_loop()


class App:
    def __init__(self):
        self.running = True
        self.global_interface = GlobalInterface(None, self)

    def main_loop(self):
        while self.running:
            current_inp = input("command: ")
            self.enter_command(current_inp)

    def enter_command(self, inp):
        if inp == "":
            return
        inp_command_data = parse_inp(inp)
        inp_command_interface_tree, inp_command_name = get_interface_tree(inp_command_data)
        inp_command = ExecutableCommand(inp_command_interface_tree, inp_command_name, inp_command_data)

        self.global_interface.get_command(inp_command)

    def exit(self):
        self.running = False


if __name__ == "__main__":
    main()
