#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

def delete_file(path_to_file):
    if not os.path.exists(path_to_file):
        print "No such file or directory: " + path_to_file
    elif os.path.isdir(path_to_file):
        print "There is a directory" + path_to_file
    else:
        testingNFS4.delete(path_to_file)
        print "Test 5: passed"
        return "Passed"
