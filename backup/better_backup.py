"""
    Better back up script using the tarfile object
    Compresses a directory or file to be saved to a location specified in a property file.

    Author: Jacob Stoffregen
"""

import tarfile
import os
from pathlib import Path

"""
    Will read frrom a property file.
    File must be within the same directory as the backup script.


    Potential issue, no good mapping for files such as a .properties. Instead using
    a simple text file with a '=' to split the string is sufficient.

    Needed:
        file_name
            The name of the file saved. Must be at least one, but multiple are possible (main should be named file_name)
        file_location
            The file's current location. 
            Unsure how to do file pathing at this point as it could be tricky
        file_destination
            The directory the file will be saved to.
            Multiple save points????
        file_output_name
            What the compressed file will be called.

    Optional:


"""
line_separator = os.linesep


property_map = {}
list_of_keys = []

def readPropertyFile():
    with open("backup.properties") as properties:
        for line in properties:
            if line[0] != '#' and line != line_separator:
                line = line.split('=')
                property_map[line[0]] = line[1].strip(line_separator)
                list_of_keys.append(line[0])

    print("File read")


"""
    Check input from the property file.
        Files saved must exist
        File origin directory must exist
        File destination direcory must exist, if not can be created
        File output if exists must be deleted, if not no action taken.
"""
def checkNeededInputs():
    file_name = property_map['file_name']
    file_location = property_map['file_location']
    file_destination = property_map['file_destination']
    file_output_name = property_map['file_output_name']


    origin_test = Path.is_dir(file_location)

    print(origin_test)

    return "All files properly made"




"""
    Will find if a file with the same output name exists in the directory
    and if so will delete it.

"""


"""
    Tar the file and save it to the output directory
"""
readPropertyFile()
print(checkNeededInputs())
