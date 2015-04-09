#__author__ = 'stml'
#!/usr/bin/env python
import  testingNFS4
import os

def moveFile( pathToFile, userDir, fileName ):
    if not os.path.exists( pathToFile ):
        print "No such file or directory: " + pathToFile
    elif os.path.isdir( pathToFile ):
        print "There is a directory" + pathToFile
    else:
        firstMd5 = testingNFS4.func_calcMd5sum( pathToFile )
        testingNFS4.copy( pathToFile, userDir )
        da = testingNFS4.func_pattern( userDir, fileName )
        secondMd5 = testingNFS4.func_calcMd5sum( da )
        if firstMd5 != secondMd5:
            print "Test 1: failed"
            return "Failed"
        else:
            print "Test 1: passed"
            return "Passed"