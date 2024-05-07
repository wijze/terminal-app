from interfaces.inteface import Interface
from command import FormalCommand, FormalArgument, ArgumentType

from datetime import datetime


DATE_TOKENS = ["yyyy", "yy", "MM", "M", "mm", "m", "DD", "D", "dd", "d"]
TIME_TOKENS = ["HH", "H", "hh", "h", "mm", "m", "ss", "s"]


def get_2_long(s):
    return s if len(s) == 2 else "0" + s


class DatetimeInterface(Interface):
    def define_vars(self):
        self.name = "datetime"
        self.is_global = True
        self.commands = {
            "date": FormalCommand("date", self.get_date, [
                FormalArgument("format", ArgumentType.STRING, True, "DD dd/M/yy", 0)
            ]),
            "time": FormalCommand("time", self.get_time, [
                FormalArgument("format", ArgumentType.STRING, True, "hh:mm", 0)
            ])
        }

    def get_date(self, args):
        time = datetime.now()
        now = {}
        now["yyyy"] = str(time.year)
        now["yy"] = now["yyyy"][2:]
        now["m"] = str(time.month)
        now["mm"] = get_2_long(now["m"])
        now["MM"] = MONTHS[time.month - 1]
        now["M"] = MONTHS_SHORT[time.month - 1]
        now["d"] = str(time.day)
        now["dd"] = get_2_long(now["d"])
        now["DD"] = WEEKDAYS[time.isoweekday() - 1]
        now["D"] = WEEKDAYS_SHORT[time.isoweekday() - 1]
        print(self.parse_format(args["format"], now))

    def get_time(self, args):
        time = datetime.now()
        now = {}
        now["H"] = str(time.hour) if time.hour < 12 else str(time.hour - 12)
        now["HH"] = get_2_long(now["H"])
        now["h"] = str(time.hour)
        now["hh"] = get_2_long(now["h"])
        now["m"] = str(time.minute)
        now["mm"] = get_2_long(now["m"])
        now["s"] = str(time.second)
        now["ss"] = get_2_long(now["s"])
        print(self.parse_format(args["format"], now))

    def parse_format(self, given_format, now: dict[str, str]):
        now = {key: now[key] for key in sorted(now.keys(), key=lambda s: len(s), reverse=True)}
        res = given_format
        for key in now:
            res = res.replace(key, "<" + str(list(now.keys()).index(key)) + ">")
        for key in now:
            res = res.replace("<" + str(list(now.keys()).index(key)) + ">", now[key])
        return res


MONTHS_SHORT = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
WEEKDAYS_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
