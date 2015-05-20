#__author__ = 'stml'
#!/usr/bin/env python

import  testingNFS4
import os

class DeleteFileTest():

    def delete_file(self, path_to_file):
        obj = testingNFS4.TestSuite()
        if not os.path.exists(path_to_file):
            print "No such file or directory: " + path_to_file
        elif os.path.isdir(path_to_file):
            print "There is a directory" + path_to_file
        else:
            obj.delete(path_to_file)
            print "Test 5: passed"
            return "passed"
