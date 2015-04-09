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
import glob

import moveFile
import changeContent
import deleteFile
import changePermission
import changeOwner

#Flush the keyboard buffer.
def flush_input( ):
    sys.stdout.flush( )
    sys.stdin.flush( )

def log_to_flash( dir_rath, prefix, rrez ):
    df = os.path.join( dir_rath, prefix )
    fh = open( df, "w" )
    i = 1
    for item in rrez:
        if i < 10:
            total = "00"+ str( i )
        elif i < 100:
            total = "0"+str( i )
        else:
            total = str( i )
        fh.write( "TC" + total + ":" + " %s\n" % item )
        i += 1
    print "Log file: " + df
    fh.close

def sturt_up( link, fileName ):
    fullPath = os.path.join( link, fileName )
    #if path to exist
    if os.path.exists( link ):
        if os.path.isfile( fullPath ):
            fileSize = os.path.getsize( fullPath )
            if ( fileSize <= 0 ):
                fill_The_File( fullPath )
        else:
            create_file( fullPath )
    else:
        os.mkdir( link )
        create_file( fullPath )

def create_file( foldFileName ):
    fh = open( foldFileName, "w+" )
    fill_The_File( fh )
    fh.close( )

def fill_The_File( file2 ):
    if not ( os.access( file2.name, os.W_OK and os.R_OK ) ):
        print "Error writing to file."
    else:
        for i in xrange( 3 ):
            file2.write( "txtTestFile" )

#get os.chown(path, uid, gid)
def get_owner_of_file( part ):
    stat_info = os.stat( part )
    #user id
    uid = stat_info.st_uid
    #user name
    user = pwd.getpwuid( uid )[ 0 ]
    #group id
    gid = stat_info.st_gid
    #group name
    group = grp.getgrgid( gid )[ 0 ]

#os.chown(path, uid, gid)
def set_owner_of_file( part, own, own2 ):
    #write other owner name
    uid = pwd.getpwnam( own ).pw_uid
    #write other group name
    gid = grp.getgrnam( own2 ).gr_gid

    os.chown( part, uid, gid )

#os.chmod(path, mode)
def checking_file_permissions( currentFile ):
    permFiles = oct( os.stat( currentFile )[ ST_MODE ] )[ -3: ]
    return permFiles

def set_file_permissions( currentFile, numToSet ):
    if not os.path.exists( currentFile ) and os.path.isdir( currentFile ):
        print "There is a directory " + currentFile
    else:
        #os.chmod(path, mode)
        subprocess.call( [ 'chmod', numToSet, currentFile ] )

def copy( part, part2 ):
    if not os.path.exists( part ) and os.path.isdir( part ):
        print "There is a directory" + part
    elif not os.path.exists( part2 ) and not os.path.isdir( part2 ):
        print "There is no "  + part2 + " directory"
    else:
        try:
            shutil.copy2( part, part2 )
        except IOError, e:
            print "Unable to copy file. %s" % e
    return part2

def move( dist, distTo ):
    try:
        shutil.move( dist, distTo )
    except IOError, e:
        print "Unable to move file. %s" % e
    return distTo

def func_calcMd5sum( checkmd5 ):
    # Open, file and calculate MD5 on its contents
    with open( checkmd5 ) as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned

def func_pattern( dp, pat ):
    os.chdir( dp )
    for f in glob.glob( pat ):
        joinPath = os.path.join( dp, pat )
    return joinPath

def delete( part ):
    try:
        os.remove( part )
        string = "File: " + part + " was successfully deleted"
        return string
    except IOError, e:
        errorString = "Unable to delete file. %s" % e
        return errorString

def changeFileContent( pathToFile ):
    file = open( pathToFile, "r" )
    contents = file.read( )
    file.close( )
    file = open( pathToFile, "w" )
    file.write(contents.replace( contents, 'Orange' ) )
    file.close( )
    return file

def replace( file_path, pattern, subst ):
    #Create temp file
    fh, abs_path = mkstemp( )
    new_file = open( abs_path,'w+' )
    old_file = open( file_path )
    for line in old_file:
        new_file.write( line.replace( pattern, subst ) )
    #close temp file
    new_file.close( )
    close( fh )
    old_file.close( )
    #Remove original file
    remove( file_path )
    #Move new file
    shutil.move( abs_path, file_path )

def menuTests( ):
    print ""
    print "------------------------------------"
    print "     Minsk SysQA: Menu "
    print "------------------------------------"

    print "menuContent:"
    print "1. Copy file."
    print "2. Replace the contents of text file."
    print "3. Get the owner of a files."
    print "4. Change file permissions."
    print "5. Delete file."
    print

    userDir = os.path.expanduser( "~" )
    testFolder = "Tests"
    fileName = '123.txt'
    rez = []

    #path to /userDir/Test
    userDirTestFolder = os.path.join( userDir , testFolder )
    #path to /userDir/Test/123.txt
    userDirTestFolderFileName = os.path.join( userDirTestFolder, fileName )
    #path to /userDir/123.txt
    userDirFileName = os.path.join( userDir, fileName )

    sturt_up( userDirTestFolder, fileName )

    movRez = moveFile.moveFile( userDirTestFolderFileName, userDir, fileName )
    rez.append( movRez )
    chanContRez = changeContent.changeContent( userDirFileName )
    rez.append( chanContRez )
    rezChan = changeOwner.change( userDirTestFolderFileName )
    rez.append( rezChan )
    chanPermRez = changePermission.permissions( userDirTestFolderFileName )
    rez.append( chanPermRez )
    delRez = deleteFile.deleteFile( userDirTestFolderFileName )
    rez.append( delRez )

    os.remove( userDirFileName )
    shutil.rmtree( userDirTestFolder )

    print

    log_to_flash( userDir, "svc_msr.txt", rez )

#       Main:
def menuMain( ):
    print "******************************"
    print "Minsk SysQA: test application "
    print "******************************"
    menuTests( )

    print( "Exit from test " )

if __name__ == "__main__":
    if flush_input( ):
        print "flash the keyboard, FAIL"
    menuMain( )