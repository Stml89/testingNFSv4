#__author__ = 'stml'
#!/usr/bin/env python
import  testingNFS4
import os

def changeContent( pathToFile ):
    if not os.path.exists( pathToFile ):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir( pathToFile ):
        print "There is a directory" + pathToFile
    else:
        testingNFS4.changeFileContent( pathToFile )
        print "Test 2: passed"
        return "Passed"