__author__ = 'stml'
#__author__ = 'stml'
#!/usr/bin/env python
import  testingNFS4
import os

class ChangeOwnerTest():

    def change_owner(self, pathToFile):
        obj = testingNFS4.TestSuite();
        if not os.path.exists(pathToFile):
            print "No such file or directory: " + pathToFile
        elif os.path.isdir(pathToFile):
            print "There is a directory" + pathToFile
        else:
            owner = obj.get_owner_of_file(pathToFile)
            obj.set_owner_of_file(pathToFile, "stml", "lpadmin")

            obj.get_owner_of_file(pathToFile)
            obj.set_owner_of_file(pathToFile, "stml", "stml")

            owner2 = obj.get_owner_of_file(pathToFile)

            if(owner2 != owner):
                print "Test 3: failed"
                return "Failed"
            else:
                print "Test 3: passed"
                return "Passed"