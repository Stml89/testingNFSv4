#__author__ = 'stml'
#!/usr/bin/env python

import os
from os import close, remove
import shutil
import pwd
import grp
import sys
from stat import *
import subprocess
from tempfile import mkstemp
import hashlib

import move_file
import change_content
import delete_file
import change_permission
import change_owner

#get os.chown(path, uid, gid)
def get_owner_of_file(part):
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
def set_owner_of_file(part, own, own2):
    #write other owner name
    uid = pwd.getpwnam(own).pw_uid
    #write other group name
    gid = grp.getgrnam(own2).gr_gid

    os.chown(part, uid, gid)

#os.chmod(path, mode)
def check_file_permissions(currentfile):
    permFiles = oct( os.stat(currentfile)[ST_MODE])[-3:]
    return permFiles

def set_file_permissions(currentfile, num_to_set):
    if not os.path.exists(currentfile) and os.path.isdir(currentfile):
        print "There is a directory " + currentfile
    else:
        #os.chmod(path, mode)
        subprocess.call(['chmod', num_to_set, currentfile])

def change_file_content(path_to_file):
    file_to_read = open(path_to_file, "r")
    content = file_to_read.read()
    file_to_read.close()
    file_to_read = open(path_to_file, "w")
    file_to_read.write(content.replace(content, 'Orange'))
    file_to_read.close()
    return file_to_read

#Flush the keyboard buffer.
def flush_input():
    sys.stdout.flush()
    sys.stdin.flush()

def log_to_flash(dir_rath, prefix, result):
    path_to_file = os.path.join(dir_rath, prefix)
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

def sturt_up(link, fileName):
    full_path_to_file = os.path.join(link, fileName)
    #if path to exist
    if os.path.exists(link):
        if os.path.isfile(full_path_to_file):
            fileSize = os.path.getsize(full_path_to_file)
            if (fileSize <= 0):
                fill_the_file(full_path_to_file)
        else:
            create_file(full_path_to_file)
    else:
        os.mkdir(link)
        create_file(full_path_to_file)

def create_file(foldFileName):
    file_for_wr = open(foldFileName, "w+")
    fill_the_file(file_for_wr)
    file_for_wr.close()

def fill_the_file(file2):
    if not (os.access(file2.name, os.W_OK and os.R_OK)):
        print "Error writing to file."
    else:
        for i in xrange(3):
            file2.write("txtTestFile")

def copy(part, part2):
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

def move(dist, dist_to):
    try:
        shutil.move(dist, dist_to)
    except IOError, e:
        print "Unable to move file. %s" % e
    return dist_to

def func_calcMd5sum(checkmd5):
    # Open, file and calculate MD5 on its contents
    with open(checkmd5) as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned

def func_pattern(folder_name, file_name):
    os.chdir(folder_name)
    # for f in glob.glob(pat):
    joinPath = os.path.join(folder_name, file_name)
    return joinPath

def delete(path_to_file):
    try:
        os.remove(path_to_file)
        message_about_del_file = "File: " + path_to_file + " was successfully deleted"
        return message_about_del_file
    except IOError, e:
        error_string = "Unable to delete file. %s" % e
        return error_string

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w+')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)

def menu_tests():
    print """
    ------------------------------
         Minsk SysQA: Menu
    ------------------------------

    "menuContent:"
    "1. Copy file."
    "2. Replace the contents of text file."
    "3. Get the owner of a files."
    "4. Change file permissions."
    "5. Delete file.
    """

    user_dir = os.path.expanduser("~")
    test_folder = "Tests"
    def_file_name = '123.txt'
    summary = []

    #path to /userDir/Test
    user_dir_test_folder = os.path.join(user_dir, test_folder)
    #path to /userDir/Test/123.txt
    user_dir_test_folder_file_name = os.path.join(user_dir_test_folder, def_file_name)
    #path to /userDir/123.txt
    user_dir_file_name = os.path.join(user_dir, def_file_name)

    sturt_up(user_dir_test_folder, def_file_name)

    mov_res = move_file.move_file(user_dir_test_folder_file_name, user_dir, def_file_name)
    summary.append(mov_res)
    chan_cont_res = change_content.change_content(user_dir_file_name)
    summary.append(chan_cont_res)
    chan_own_res = change_owner.change(user_dir_test_folder_file_name)
    summary.append(chan_own_res)
    chan_perm_res = change_permission.permissions(user_dir_test_folder_file_name)
    summary.append(chan_perm_res)
    chan_del_res = delete_file.delete_file(user_dir_test_folder_file_name)
    summary.append(chan_del_res)

    os.remove(user_dir_file_name)
    shutil.rmtree(user_dir_test_folder)

    print

    log_to_flash(user_dir, "svc_msr.txt", summary)

#       Main:
def menu_main():
    print"""
    ******************************
    Minsk SysQA: test application
    ******************************"""
    menu_tests()

    print("Exit from test ")

if __name__ == "__main__":
    if flush_input():
        print "flash the keyboard, FAIL"
    menu_main()