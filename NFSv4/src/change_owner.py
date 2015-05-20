__author__ = 'stml'
#__author__ = 'stml'
#!/usr/bin/env python
import  testingNFS4
import os

def change(pathToFile):
    if not os.path.exists(pathToFile):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir(pathToFile):
        print "There is a directory" + pathToFile
    else:
        owner = testingNFS4.get_owner_of_file(pathToFile)
        testingNFS4.set_owner_of_file(pathToFile, "stml", "lpadmin")

        testingNFS4.get_owner_of_file(pathToFile)
        testingNFS4.set_owner_of_file(pathToFile, "stml", "stml")

        owner2 = testingNFS4.get_owner_of_file(pathToFile)

        if(owner2 != owner):
            print "Test 3: failed"
            return "Failed"
        else:
            print "Test 3: passed"
            return "Passed"