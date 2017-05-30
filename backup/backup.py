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

def determineTarget(tar_target, tar_directory):
    if tar_target == tar_directory:
        return tar_target
    else:
        return tar_directory + tar_target


def readPropertyFile():
    with open("backup.properties") as properties:
        for line in properties:
            if line[0] != '#' and line != line_separator:
                line = line.split('=')
                property_map[line[0]] = line[1].strip(line_separator)
                list_of_keys.append(line[0])


"""
    Check input from the property file.
        Files saved must exist.
        File origin directory must exist.
        File destination direcory should exist, if not it will be created.
        File output if exists must be deleted, if not no action taken.
"""
def checkNeededInputs():
    origin_target = property_map['tar_target']
    origin_target_location = property_map['file_location']
    target_destination = property_map['file_destination']
    target_output_name = property_map['file_output_name']

    origin_directory_test = os.path.isdir(origin_target_location)

    if not origin_directory_test:
        return "The origin directory does not exist"

    tar_target_path = determineTarget(origin_target, origin_target_location)

    origin_target_test = os.path.exists(tar_target_path)

    if not origin_target_test:
        return "The target for tarring does not exist"




    destination_directory_test = os.path.isdir(target_destination)

    if not destination_directory_test:
        os.makedirs(target_destination)
        print("Folder was created for the backup file...")


    #target_name = file_output_name + ".tar.gz"
    output_file_exists_test = os.path.exists(target_destination + target_output_name)

    if output_file_exists_test:        
        tar_file_test = tarfile.is_tarfile(target_destination + target_output_name)

        if tar_file_test:
            ##Delete the file
            os.remove(target_destination + target_output_name)

            print("Original file deleted")
        else:
            return "Output file was not a tar file"


    return "All files properly made"



"""
    Tar the file and save it to the output directory

    Determines the canonical path to the target file and
    a relative path to the target file.

    The relative path is used to remove the excess directory structure or a full
    recursive copy of the target is made.
"""
def tarFileToDirectory():
    origin_target = property_map['tar_target']
    origin_target_location = property_map['file_location']
    target_destination = property_map['file_destination']
    target_output_name = property_map['file_output_name']

    tar_target_path = determineTarget(origin_target, origin_target_location)

    relative_target_path = os.path.relpath(tar_target_path,"/home/jake-python/")

    with tarfile.open((target_destination + target_output_name), mode='w:gz') as tar:
        tar.add(tar_target_path, arcname=os.path.basename(relative_target_path))



def runBackup():
    readPropertyFile()
    print(checkNeededInputs())
    tarFileToDirectory()
    print("End of backup")

runBackup()
