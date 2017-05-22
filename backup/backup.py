from subprocess import run

run(["echo", "Did it work?"])


"""
    Move command to move files into a specific place, just change the destination
"""

#run(["mv remove.txt -t ~/Dropbox/backup"], shell=True)



"""
    Copy command that will copy files to destination
"""

run(["cp backup.py -t ~/Dropbox/backup"], shell=True)

