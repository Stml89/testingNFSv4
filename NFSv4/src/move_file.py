#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

def move_file(path_to_file, user_dir, file_name):
    if not os.path.exists(path_to_file):
        print "No such file or directory: " + path_to_file
    elif os.path.isdir(path_to_file):
        print "There is a directory" + path_to_file
    else:
        firstMd5 = testingNFS4.func_calcMd5sum(path_to_file)
        testingNFS4.copy(path_to_file, user_dir)
        get_path_to_file = testingNFS4.func_pattern(user_dir, file_name)
        secondMd5 = testingNFS4.func_calcMd5sum(get_path_to_file)
        if firstMd5 != secondMd5:
            print "Test 1: failed"
            return "Failed"
        else:
            print "Test 1: passed"
            return "Passed"