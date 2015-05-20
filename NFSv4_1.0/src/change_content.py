#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

class ChangeContentTest():

    def change_content(self, pathToFile):
        obj = testingNFS4.TestSuite();
        if not os.path.exists(pathToFile):
            print "No such file or directory: " + pathToFile
        elif os.path.isdir(pathToFile):
            print "There is a directory" + pathToFile
        else:
            obj.change_file_content(pathToFile)
            print "Test 2: passed"
            return "Passed"