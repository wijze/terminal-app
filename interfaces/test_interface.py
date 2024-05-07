from interfaces.inteface import Interface
from command import FormalCommand, FormalArgument, ArgumentType


class TestInterface(Interface):
    def define_vars(self):
        self.name = "test"
        self.is_global = True
        self.commands = {
            "sayHello": FormalCommand("sayHello", self.say_hello, [
                FormalArgument("name", ArgumentType.STRING, True, None, 0)
            ]),
            "test": FormalCommand("test", self.test, []),
            "plus": FormalCommand("plus", self.plus, [
                FormalArgument("a", ArgumentType.NUMBER, False, None, 0),
                FormalArgument("b", ArgumentType.NUMBER, False, None, 1),
            ])
        }

    @staticmethod
    def say_hello(args: dict):
        if args["name"]:
            print(f"hello, {args['name']}")
        else:
            print("hello")

    @staticmethod
    def test(args: dict):
        print("test 123")

    @staticmethod
    def plus(args: dict):
        print(args["a"] + args["b"])
