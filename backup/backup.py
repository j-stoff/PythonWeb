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

"""
    Function is designed to take in a value from a properties file and remove the trailing separator found at the end of the file.

    For example, the '\n' will appear on file IO in such a file and should not be part of the actual input.


    value:
        The value to be stripped of trailing line separator

"""
def removeTrailingSeparator(value):
    line_separator = os.linesep

    if isinstance(value, str):
        return value.strip(line_separator)

    
    if isinstance(value, list):
        value[-1] = value[-1].strip(line_separator)

        return value



"""
    Function for determining the target path based on the inputs.
    If the target and direcfory are the same, then the entire output is only to be the target.
    If not, then the directory is concatenated with the target for a specific file.

    tar_target:
        The target of the calling function.

    target_directory:
        The current directory the target resides in
"""

def determineTarget(tar_target, target_directory):
    if tar_target == target_directory:
        return tar_target
    else:
        return target_directory + tar_target


def readPropertyFile():
    with open("backup.properties") as properties:
        for line in properties:
            if line[0] != '#' and line != line_separator:
                line = line.split('=')

                value = line[1]

                if ',' in value:
                    value = value.split(',')
                    list_of_values = []

                    value = removeTrailingSeparator(value)

                    property_map[line[0]] = value

                else:
                    value = removeTrailingSeparator(value)
                    property_map[line[0]] = value


                list_of_keys.append(line[0])

                print(value)

    print("File read")


"""
    Check input from the property file.
        Files saved must exist.
        File origin directory must exist.
        File destination direcory should exist, if not it will be created.
        File output if exists must be deleted, if not no action taken.
"""
def checkNeededInputs():
    origin_target = property_map['tar_target']
    origin_target_locations = property_map['file_location']
    target_destination = property_map['file_destinations']
    target_output_name = property_map['file_output_name']

    origin_directory_test = os.path.isdir(origin_target_locations)

    if not origin_directory_test:
        return "The origin directory does not exist"

    tar_target_path = determineTarget(origin_target, origin_target_locations)

    origin_target_test = os.path.exists(tar_target_path)

    if not origin_target_test:
        return "The target for tarring does not exist"


    ##if len(target_destination) is 1, preform the normal operation

    destination_directory_test = os.path.isdir(target_destination)

    if not destination_directory_test:
        os.makedirs(target_destination)
        print("Folder made for backup file...")


    ##else, loop through each item and check that each directory exists, if not create it

    #target_name = file_output_name + ".tar.gz"
    output_file_exists_test = os.path.exists(target_destination + target_output_name)

    if output_file_exists_test:        
        tar_file_test = tarfile.is_tarfile(target_destination + target_output_name)

        if tar_file_test:
            ##Delete the file
            os.remove(target_destination + target_output_name)

            print("Original file deleted")
        else:
            print("Output file was not a tar file")


    return "All files properly made"



"""
    Tar the file and save it to the output directory
"""
def tarFileToDirectory():
    origin_target = property_map['tar_target']
    origin_target_locations = property_map['file_location']
    target_destination = property_map['file_destinations']
    target_output_name = property_map['file_output_name']

    tar_target_path = determineTarget(origin_target, origin_target_locations)

    relative_target_path = os.path.relpath(tar_target_path,"/home/jake-python/")

    #Add for in loop with all target destinations

    with tarfile.open((target_destination + target_output_name), mode='w:gz') as tar:
        tar.add(tar_target_path, arcname=os.path.basename(relative_target_path))



def runBackup():
    readPropertyFile()
    #print(checkNeededInputs())
    #tarFileToDirectory()
    #print("End of backup")

runBackup()
