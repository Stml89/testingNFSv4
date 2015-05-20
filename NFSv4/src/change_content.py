#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

def change_content(pathToFile):
    if not os.path.exists(pathToFile):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir(pathToFile):
        print "There is a directory" + pathToFile
    else:
        testingNFS4.change_file_content(pathToFile)
        print "Test 2: passed"
        return "Passed"