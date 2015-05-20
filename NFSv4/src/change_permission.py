#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

def permissions(pathToFile):
    if not os.path.exists(pathToFile):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir(pathToFile):
        print "There is a directory" + pathToFile
    else:
        permissions = testingNFS4.check_file_permissions(pathToFile)

        #change file permissions
        if(permissions == "777"):
            num = "666"
        else:
            num = "777"

        testingNFS4.set_file_permissions(pathToFile, num)
        check_permissions = testingNFS4.check_file_permissions(pathToFile)
        if(permissions == check_permissions):
            print "Test 4: failed"
            return "Failed"
        else:
            print "Test 4: passed"
            return "Passed"