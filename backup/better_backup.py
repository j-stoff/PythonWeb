"""
    Better back up script using the tarfile object
    Compresses a directory or file to be saved to a location specified in a property file.

    Author: Jacob Stoffregen
"""

import tarfile
import os

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
        Files saved must exist.
        File origin directory must exist.
        File destination direcory should exist, if not it will be created.
        File output if exists must be deleted, if not no action taken.
"""
def checkNeededInputs():
    origin_file_name = property_map['tar_target']
    origin_file_location = property_map['file_location']
    file_destination = property_map['file_destination']
    file_output_name = property_map['file_output_name']

    origin_directory_test = os.path.isdir(origin_file_location)
    origin_target_test = os.path.exists(origin_file_location + origin_file_name)

    if not origin_directory_test:
        return "The origin directory does not exist"
    elif not origin_target_test:
        return "The file does not exist"


    destination_directory_test = os.path.isdir(file_destination)

    if not destination_directory_test:
        os.makedirs(file_destination)
        print("Folder made for backup file...")


    #### Still need to test if file exists ####


    target_name = file_output_name + ".tar.gz"
    output_file_exists_test = os.path.isfile(file_destination + target_name)

    if output_file_exists_test:        
        tar_file_test = tarfile.is_tarfile(file_destination + target_name)

        if tar_file_test:
            ##Delete the file
            

            os.remove(file_destination + target_name)

            print("Original file deleted")


    return "All files properly made"



"""
    Tar the file and save it to the output directory
"""
def tarFileToDirectory():
    origin_file_name = property_map['tar_target']
    origin_file_location = property_map['file_location']
    file_destination = property_map['file_destination']
    file_output_name = property_map['file_output_name']
    target_name = file_output_name + ".tar.gz"

    with tarfile.open((file_destination + target_name), mode='w') as out:
        print("Taring file...")
        out.add(origin_file_location + origin_file_name)

def run():
    readPropertyFile()
    print(checkNeededInputs())
    tarFileToDirectory()

run()
