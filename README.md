# temperature_converter

**How to use:**  
Call it from the command line with the following syntax:
`python3 temperature_converter.py <temperature scale you want to convert from> <temperature scale you want to convert to> <temperature you want to convert>`  

**Writing extensions:**
This allows users to create extensions to it to add support for new temperature scales. Extensions should be a python script containing the following variables. The extensions must be in the same directory as the main script in order for them to work.  

`abbreviations = {"abbreviation": "full name"}  # This should be a dictionary containing abbreviations for temperature systems`  
`to_celsius_entries = {"full name": to_celsius_function}  # This should be a dictionary where the keys are the full name of the temperature system and the values are the functions for converting your system to Celsius. The function should take 1 argument, the temperature that is being converted in decimal.Decimal format.The function should return a decimal.Decimal containing the converted temperature.`  
`from_celsius_entries = {"full name": from_celsius_function}  # This should be a dictionary where the keys are the full name of the temperature system and the values are the functions for converting Celsius to your system. The function should take 1 argument, the temperature that is being converted in decimal.Decimal format.The function should return a decimal.Decimal containing the converted temperature.`

Your extension's filename must start with the string "Temperature_Extension" in order for the script to recognize it. The script will call them in alphabetical order, with the ones last alphabetically being called last
