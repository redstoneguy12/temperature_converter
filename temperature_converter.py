# Script written by redstoneguy12
# Github: https://github.com/redstoneguy12/temperature_converter


import argparse
from decimal import Decimal
from glob import glob
from importlib import import_module
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("from_system")
argparser.add_argument("to_system")
argparser.add_argument("value", type=Decimal)
args = argparser.parse_args()

to_system = args.to_system
from_system = args.from_system
value = args.value


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
