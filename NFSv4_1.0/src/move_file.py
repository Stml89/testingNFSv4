#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

class MoveFileTest():

    def move_file(self, path_to_file, user_dir, file_name):
        obj = testingNFS4.MainFunctions();
        if not os.path.exists(user_dir):
            print "No such file or directory: " + user_dir
        elif os.path.isdir(user_dir):
            print "There is a directory" + user_dir
        else:
            firstMd5 = obj.func_calcMd5sum(user_dir)
            obj.copy(user_dir, path_to_file)
            get_path_to_file = os.path.join(path_to_file, file_name)
            secondMd5 = obj.func_calcMd5sum(get_path_to_file)
            os.remove(get_path_to_file)
            if firstMd5 != secondMd5:
                print "Test 1: failed"
                return "Failed"
            else:
                print "Test 1: passed"
                return "Passed"