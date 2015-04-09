#__author__ = 'stml'
#!/usr/bin/env python
import  testingNFS4
import os

def deleteFile( pathToFile ):
    if not os.path.exists( pathToFile ):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir( pathToFile ):
        print "There is a directory" + pathToFile
    else:
        aaa = testingNFS4.delete( pathToFile )
        print "Test 5: passed"
        return "Passed"
