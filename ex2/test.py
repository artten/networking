import os

for currentpath, folders, files in os.walk('.'):
    for file in files:
        print(os.path.join( file))
    for folder in folders:
        print(os.path.join( folder) + "          1")
