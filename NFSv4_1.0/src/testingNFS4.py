#__author__ = 'stml'
#!/usr/bin/env python

import os
import shutil
import pwd
import grp
import sys
from stat import *
import subprocess
import hashlib

import move_file
import change_content
import delete_file
import change_permission
import change_owner

class MainFunctions:

    def sturt_up(self, link, fileName):
        full_path_to_file = os.path.join(link, fileName)
        #if path to exist
        if os.path.exists(link):
            if os.path.isfile(full_path_to_file):
                fileSize = os.path.getsize(full_path_to_file)
                if (fileSize <= 0):
                    self.fill_the_file(full_path_to_file)
            else:
                self.create_file(full_path_to_file)
        else:
            os.mkdir(link)
            self.create_file(full_path_to_file)

    def fill_the_file(self, file2):
        if not (os.access(file2.name, os.W_OK and os.R_OK)):
            print "Error writing to file."
        else:
            for i in xrange(3):
                file2.write("txtTestFile")

    def create_file(self, foldFileName):
        file_for_wr = open(foldFileName, "w+")
        self.fill_the_file(file_for_wr)
        file_for_wr.close()

    def log_to_flash(self, dir_rath, folder, prefix, result):
        path_to_folder = os.path.join(dir_rath, folder)
        path_to_file = os.path.join(path_to_folder, prefix)
        file_header = open(path_to_file, "w")
        i = 1
        for item in result:
            if i < 10:
                total = "00"+ str(i)
            elif i < 100:
                total = "0"+str(i)
            else:
                total = str(i)
            file_header.write("TC" + total + ":" + " %s\n" % item)
            i += 1
        print "Log file: " + path_to_file
        file_header.close

    def func_calcMd5sum(self, checkmd5):
        # Open, file and calculate MD5 on its contents
        with open(checkmd5) as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned

    def copy(self, part, part2):
        if not os.path.exists(part) and os.path.isdir(part):
            print "There is a directory" + part
        elif not os.path.exists(part2) and not os.path.isdir(part2):
            print "There isnt "  + part2 + " directory"
        else:
            try:
                shutil.copy2(part, part2)
            except IOError, e:
                print "Unable to copy file. %s" % e
        return part2

    def delete(self, path_to_file):
        try:
            os.remove(path_to_file)
            message_about_del_file = "File: " + path_to_file + " was successfully deleted"
            return message_about_del_file
        except IOError, e:
            error_string = "Unable to delete file. %s" % e
            return error_string

class TestSuite(MainFunctions):

    def change_file_content(self, path_to_file):
        file_to_read = open(path_to_file, "r")
        content = file_to_read.read()
        file_to_read.close()
        file_to_read = open(path_to_file, "w")
        file_to_read.write(content.replace(content, 'Orange'))
        file_to_read.close()
        return file_to_read

    #get os.chown(path, uid, gid)
    def get_owner_of_file(self, part):
        stat_info = os.stat(part)
        #user id
        uid = stat_info.st_uid
        #user name
        user = pwd.getpwuid(uid)[0]
        #group id
        gid = stat_info.st_gid
        #group name
        group = grp.getgrgid(gid)[0]

    #os.chown(path, uid, gid)
    def set_owner_of_file(self, part, own, own2):
        #write other owner name
        uid = pwd.getpwnam(own).pw_uid
        #write other group name
        gid = grp.getgrnam(own2).gr_gid

        os.chown(part, uid, gid)

    #os.chmod(path, mode)
    def check_file_permissions(self, currentfile):
        permFiles = oct( os.stat(currentfile)[ST_MODE])[-3:]
        return permFiles

    def set_file_permissions(self, currentfile, num_to_set):
        if not os.path.exists(currentfile) and os.path.isdir(currentfile):
            print "There is a directory " + currentfile
        else:
            #os.chmod(path, mode)
            subprocess.call(['chmod', num_to_set, currentfile])

class MenuTests():

    def __init__(self):
        self.user_dir = os.path.expanduser("~")
        self.test_folder = "Tests"
        self.def_file_name = '123.txt'
        self.summary = []

    def show_menu(self):
        print """
        ------------------------------
             Minsk SysQA: Menu
        ------------------------------

        menuContent:
        1. Copy file.
        2. Replace the contents of text file.
        3. Get the owner of a files.
        4. Change file permissions.
        5. Delete file.
        """

    def start_test(self):
        obj_main = MainFunctions()
        obj_change_content = change_content.ChangeContentTest()
        obj_move_file = move_file.MoveFileTest()
        obj_change_owner = change_owner.ChangeOwnerTest()
        obj_change_perm = change_permission.ChangePermissionTest()
        obj_del_file = delete_file.DeleteFileTest()

        #path to /userDir/Test
        user_dir_test_folder = os.path.join(self.user_dir, self.test_folder)
        #path to /userDir/Test/123.txt
        user_dir_file_name = os.path.join(user_dir_test_folder, self.def_file_name)

        obj_main.sturt_up(user_dir_test_folder, self.def_file_name)

        mov_res = obj_move_file.move_file(self.user_dir, user_dir_file_name, self.def_file_name)
        chan_cont_res = obj_change_content.change_content(user_dir_file_name)
        chan_own_res = obj_change_owner.change_owner(user_dir_file_name)
        chan_perm_res = obj_change_perm.change_permissions(user_dir_file_name)
        chan_del_res = obj_del_file.delete_file(user_dir_file_name)

        self.summary.append(mov_res)
        self.summary.append(chan_cont_res)
        self.summary.append(chan_own_res)
        self.summary.append(chan_perm_res)
        self.summary.append(chan_del_res)

    def save_result(self):
        obj_main = MainFunctions()
        obj_main.log_to_flash(self.user_dir, self.test_folder, "svc_msr.txt", self.summary)

if __name__ == "__main__":
        #Flush the keyboard buffer.
    if (sys.stdout.flush() or sys.stdin.flush()):
        print "Problem with clean stdin or stdout"

    print """
    ******************************
    Minsk SysQA: test application
    ******************************"""
    obj_main = MenuTests()
    obj_main.show_menu()
    obj_main.start_test()
    obj_main.save_result()

    print "Exit from test"