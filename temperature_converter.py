#!/bin/python3

# Script written by redstoneguy12
# Github: https://github.com/redstoneguy12/temperature_converter


from decimal import Decimal
from glob import glob
from importlib import import_module
import os
import sys


class NoScaleError(Exception):
    '''Raised when you try to convert to or from an unknown scale'''
    pass


def fahrenheit_to_celsius(num):
    return (num - Decimal("32")) * (Decimal("5") / Decimal("9"))


def celsius_to_fahrenheit(num):
    return num * (Decimal("9") / Decimal("5")) + Decimal("32")


def kelvin_to_celsius(num):
    return num - Decimal("273.15")


def celsius_to_kelvin(num):
    return num + Decimal("273.15")


def rankine_to_celsius(num):
    return (num - Decimal("491.67")) / Decimal("1.8")


def celsius_to_rankine(num):
    return num * Decimal("1.8") + Decimal("491.67")


# end of conversion functions

abbreviation_dict = {
    "f": "Fahrenheit",
    "c": "Celsius",
    "k": "Kelvin",
    "ra": "Rankine"}
to_celsius_dict = {
    "Fahrenheit": fahrenheit_to_celsius,
    "Celsius": lambda x: x,
    "Kelvin": kelvin_to_celsius,
    "Rankine": rankine_to_celsius,
}
from_celsius_dict = {
    "Fahrenheit": celsius_to_fahrenheit,
    "Celsius": lambda x: x,
    "Kelvin": celsius_to_kelvin,
    "Rankine": celsius_to_rankine}


def load_extensions():
    for path in sorted(glob("Temperature_Extension*")):
        module = import_module(os.path.splitext(path)[0])
        abbreviation_dict.update(module.abbreviations)
        to_celsius_dict.update(module.to_celsius_entries)
        from_celsius_dict.update(module.from_celsius_entries)


def get_available_scales():
    return {
            'input': to_celsius_dict.keys(),
            'output': from_celsius_dict.keys()
           }


def unabbreviate(abbreviated_value):
    from_dict = abbreviation_dict.get(abbreviated_value)

    if(from_dict is not None):
        return from_dict

    if(abbreviated_value in abbreviation_dict.values()):
        return abbreviated_value

    return from_dict


def convert(from_scale, to_scale, value):
    to_scale = to_scale.lower()
    from_scale = from_scale.lower()

    to_scale = unabbreviate(to_scale)
    from_scale = unabbreviate(from_scale)

    if to_scale is None:
        raise NoScaleError("To scale not recognized")

    if from_scale is None:
        raise NoScaleError("From scale not recognized")

    # convert it to celsius
    value_celsius = to_celsius_dict.get(from_scale)(value)
    # convert it to desired scale
    return from_celsius_dict.get(to_scale)(value_celsius)


if __name__ == '__main__':
    import argparse

    first_parser = argparse.ArgumentParser()

    first_parser.format_help = lambda: """usage: temperature_converter.py [-h] [--list_all_scales] from_scale to_scale value

    positional arguments:
      from_scale
      to_scale
      value

    optional arguments:
      -h, --help         show this help message and exit
      --list_all_scales  This will list all of the scales that are currently
                         avaliable, including in extensions
    """
    first_parser.format_usage = lambda: "usage: temperature_converter.py [-h] [--list_all_scales] from_scale to_scale value\n"  # noqa

    group = first_parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--list_all_scales", action="store_true", help="This will list all of the scales that are currently avaliable, including in extensions")  # noqa

    parser_default = argparse.ArgumentParser()
    parser_default.add_argument("from_scale")
    parser_default.add_argument("to_scale")
    parser_default.add_argument("value", type=Decimal)

    parser_default.format_usage = first_parser.format_usage

    args = first_parser.parse_known_args(sys.argv[1:])

    load_extensions()

    if not args[0].list_all_scales:
        args = parser_default.parse_args()
        to_scale = args.to_scale
        from_scale = args.from_scale
        value = args.value
    else:
        scales = get_available_scales()

        print('Input:')
        for scale in scales['input']:
            print('\t', scale)
        print('Output:')
        for scale in scales['output']:
            print('\t', scale)

    try:
        print(convert(from_scale, to_scale, value))
    except NoScaleError as e:
        print(e)
