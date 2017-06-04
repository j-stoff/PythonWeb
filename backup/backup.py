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


"""
    Reads in a 'property' file that ignores lines that begin with a # and and splits the lines into key value pairs on either 
    side of a '='

"""

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

                

    print("File read")

"""
    Function to create a directory in order to store the file.

    location:
        A string that will be taken as a path to create a new directory.
        The path must be in canonical form.
"""

def makeDirectoryForBackup(location):
    os.makedirs(location)
    print("Created directory to store file. Located in at: " + location)


"""
    This function is designed to test the output directories if they exist or not. By default, the directories will be created
    if they do not exist already.

    destination:
        The path to the output directory

    create:
        If the directories should be made or not.
        On by default, if a directory is not made the program will not continue.
"""
def testDestination(destination, create=True):
    destination_test = False

    if isinstance(destination, str):
        destination_test = os.path.isdir(destination)

        if create and not destination_test:
            #if the create is on and there is no destination
            makeDirectoryForBackup(destination)
            return True
        elif destination_test:
            #if the destination was found return true
            return True
        else:
            return False

    if isinstance(destination, list):
        for entry in destination:
            destination_test = os.path.isdir(entry)

            if create and not destination_test:
                #if the create is on and there is no destination
                makeDirectoryForBackup(entry)
            elif not destination_test:
                #If no create is on and a destionation was false, stop and return false
                return False

        return True

"""
    Test designed to validate if a file with the same name is already in an output directory.
    If so, the file is deleted and a new one is created.

    destination:
        The output directory.

    File:
        The file to be validated if it exists.
"""
def testOutputFile(destination, file):


    if isinstance(destination, str):
        output_test = os.path.exists(destination + file)

        tar_file_test = tarfile.is_tarfile(destination + file)

        if output_test and tar_file_test:
            os.remove(destination + file)
            print("Old file deleted")
            return True
        


    if isinstance(destination, list):
        for entry in destination:
            output_test = os.path.exists(entry + file)

            tar_file_test = os.path.exists(entry + file)

            if output_test and tar_file_test:
                os.remove(entry + file)
                print("Previous file deleted")


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
    target_destinations = property_map['file_destinations']
    target_output_name = property_map['file_output_name']

    origin_directory_test = os.path.isdir(origin_target_locations)

    if not origin_directory_test:
        return "The origin directory does not exist"

    tar_target_path = determineTarget(origin_target, origin_target_locations)

    origin_target_test = os.path.exists(tar_target_path)

    if not origin_target_test:
        return "The target for tarring does not exist"


    ##if len(target_destination) is 1, preform the normal operation

    target_destination_test = testDestination(target_destinations)

    if not target_destination_test:
        return "One of the output directories does not exist, please correct this error."

    testOutputFile(target_destinations, target_output_name)
    """

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
    """

    return "All files properly made"




"""
    Tar the file and save it to the output directory
"""
def tarFileToDirectory():
    origin_target = property_map['tar_target']
    origin_target_locations = property_map['file_location']
    target_destinations = property_map['file_destinations']
    target_output_name = property_map['file_output_name']

    tar_target_path = determineTarget(origin_target, origin_target_locations)

    relative_target_path = os.path.relpath(tar_target_path,"/home/jake-python/")

    #Add for in loop with all target destinations

    if isinstance(target_destinations, str):
        with tarfile.open((target_destinations + target_output_name), mode='w:gz') as tar:
            tar.add(tar_target_path, arcname=os.path.basename(relative_target_path))


    elif isinstance(target_destinations, list):
        for entry in target_destinations:
            with tarfile.open((entry + target_output_name), mode="w:gz") as tar:
                tar.add(tar_target_path, arcname=os.path.basename(relative_target_path))


def runBackup():
    readPropertyFile()
    print(checkNeededInputs())
    tarFileToDirectory()
    print("End of backup")

runBackup()
