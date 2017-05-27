"""
    Better back up script using the tarfile object
    Author: Jacob Stoffregen
"""

import tarfile
import os


"""
    Will read from a file
    File must be within the same directory as the backup script.


    Potential issue, no good mapping for files such as a .properties. Instead using
    a simple text file with a '=' to split the string is sufficient.

    Needed:
        file_name
        file_location
        file_destination
        file_output_name

"""


line_separator = os.linesep


property_map = {}
list_of_keys = []

with open("property.txt") as properties:
    for line in properties:
        if line[0] != '#' and line != line_separator:
            print(line)
            line = line.split('=')
            property_map[line[0]] = line[1]
            list_of_keys.append(line[0])

print(property_map)
print(list_of_keys)
"""
    Will find if a file with the same output name exists in the directory
    and if so will delete it.

"""


"""
    Tar the file and save it to the output directory
"""