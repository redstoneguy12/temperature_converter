# Script written by redstoneguy12
# Github: https://github.com/redstoneguy12/temperature_converter


import argparse
from decimal import Decimal
from glob import glob
from importlib import import_module
import os
import sys

first_parser = argparse.ArgumentParser()

first_parser.format_help = lambda: """usage: temperature_converter.py [-h] [--list_all_scales] from_system to_system value

positional arguments:
  from_system
  to_system
  value

optional arguments:
  -h, --help         show this help message and exit
  --list_all_scales  This will list all of the scales that are currently
                     avaliable, including in extensions
"""
first_parser.format_usage = lambda: "usage: temperature_converter.py [-h] [--list_all_scales] from_system to_system value"  # noqa

group = first_parser.add_mutually_exclusive_group(required=False)
group.add_argument("--list_all_scales", action="store_true", help="This will list all of the scales that are currently avaliable, including in extensions")  # noqa

parser_default = argparse.ArgumentParser()
parser_default.add_argument("from_system")
parser_default.add_argument("to_system")
parser_default.add_argument("value", type=Decimal)

parser_default.format_usage = first_parser.format_usage

args = first_parser.parse_known_args(sys.argv[1:])

if not args[0].list_all_scales:
    args = parser_default.parse_args()
    to_system = args.to_system
    from_system = args.from_system
    value = args.value
    list_all_scales = False
else:
    list_all_scales = True


# start of conversion functions

def fahrenheit_to_celsius(num):
    (num - Decimal("32")) * (Decimal("5") / Decimal("9"))


def celsius_to_fahrenheit(num):
    num * (Decimal("9") / Decimal("5")) + Decimal("32")


def kelvin_to_celsius(num):
    num - Decimal("273.15")


def celsius_to_kelvin(num):
    num + Decimal("273.15")


def rankine_to_celsius(num):
    (num - Decimal("491.67")) / Decimal("1.8")


def celsius_to_rankine(num):
    num * Decimal("1.8") + Decimal("491.67")


# end of conversion functions

abbreviation_dict = {
    "f": "fahrenheit",
    "c": "celsius",
    "k": "kelvin",
    "ra": "rankine"}
to_celsius_dict = {
    "fahrenheit": fahrenheit_to_celsius,
    "celsius": lambda x: x,
    "kelvin": kelvin_to_celsius,
    "rankine": rankine_to_celsius,
}
from_celsius_dict = {
    "fahrenheit": celsius_to_fahrenheit,
    "celsius": lambda x: x,
    "kelvin": celsius_to_kelvin,
    "rankine": celsius_to_rankine}

# load extensions

for path in sorted(glob("Temperature_Extension*")):
    module = import_module(os.path.splitext(path)[0])
    abbreviation_dict.update(module.abbreviations)
    to_celsius_dict.update(module.to_celsius_entries)
    from_celsius_dict.update(module.from_celsius_entries)

# check if they specified to list avaliable

if list_all_scales:
    print("Input systems:")
    for system in to_celsius_dict.keys():
        print("\t" + system)
    print("Output systems:")
    for system in from_celsius_dict.keys():
        print("\t" + system)
    exit()

# convert it

to_system = to_system.lower()
from_system = from_system.lower()


def unabbreviate(abbreviated_value):
    from_dict = abbreviation_dict.get(abbreviated_value)

    if(from_dict is not None):
        return from_dict

    if(abbreviated_value in abbreviation_dict.values()):
        return abbreviated_value

    return from_dict


to_system = unabbreviate(to_system)
from_system = unabbreviate(from_system)

if to_system is None:
    print("To system not recognized")
    exit()

if from_system is None:
    print("From system not recognized")
    exit()

# convert it to celsius
value_celsius = to_celsius_dict.get(from_system)(value)
# convert it to desired system
print((from_celsius_dict.get(to_system)(value_celsius)))
