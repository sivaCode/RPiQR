__author__ = 'siva'

import os
import sys
import time
import csv
import threading
import signal
import datetime
import subprocess


def getParentPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def createPath(sPath) :
    if not os.path.exists(sPath) :
        os.makedirs(sPath)
    else :
        print("Path : {0} already exist, Cannot recreat".format(sPath))


def createFolder(folderPath)  :
    if not (os.path.isdir(folderPath)) :
        os.mkdir(folderPath)
        return 1
    else :
        print("Folder :  {0} already exist, Cannot recreate")
        return 0

def getCurrentDateTimeStamp():
    return time.strftime("%Y%m%d_%I%M%S%p")

def getCurrentTimeStamp():
    return time.strftime("%I%M%S%p")


def getsqlTimeStamp():
    return time.strftime("%H:%M%:%S")

def getsqlDate():
    return time.strftime("%Y-%m-%d")

def getCurrentDate():
    return time.strftime("%Y%m%d")

def fileExists(fPath):
    return os.path.isfile(fPath)

def createFile(fPath):
    try :
        f = os.open(fPath,'w')
        f.close()
        return 1
    except :
        return 0

def deleteFolder(dirPath):
    try:
        os.rmdir(dirPath)
        return 1
    except :
        return 0

def deleteFile(fPath):
    try:
        os.remove(fPath)
        return 1
    except :
        return 0

def moveFile(filePath, newpath):
    try:
        os.rename(filePath,newpath)
        return 1
    except :
        return 0

def writetoFile(fPath,text,reWrite=False):
    try :
        if fileExists(fPath) :
            f = open(fPath,'a')
        else :
            f = open(fPath,'w')
        if  f  :
            f.write(text)
            f.close()
            return 1
        else :
            return 0
    except :
        return 0

def getCSVrowCount(filePath, ingnoreHeader=False):
    with open(filePath,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        data = list(reader)
        row_count = len(data)
        f.close()
    if ingnoreHeader :
        row_count = row_count -1
    return row_count


class ShellExec(threading.Thread) :
    def __init__(self, cmdList):
        super(ShellExec, self).__init__()
        self.stdout = None
        self.stderr = None
        self.stopCap = False
        self.stopExec = False
        self.returnCode = -1
        self.cmdList = cmdList

    def run(self):
        print "Command : %s" %self.cmdList
        startTime = datetime.datetime.now()
        self.proc = subprocess.Popen(self.cmdList,
                     shell=False,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
        self.pid = self.proc.pid
        self.proc.wait()
        self.stdout, self.stderr = self.proc.communicate()
        self.returnCode = self.proc.returncode
        print ("Process execution time : {0} -  {1} Seconds".format(self.cmdList[len(self.cmdList)-1],datetime.datetime.now() - startTime))

    def getStatus(self):
        return self.returnCode

    def stopCapture(self):
        self.stopCap = True
        try :
            self.proc.stdin.write('q')
            #self.proc.stdin.flush()
        except IOError, ValueError  :
            print("subProcess Stopped")
        except :
            print ("SubProcess : Unexpected error : {0}".format(sys.exc_info()[0]))

    def stopExecution(self):
        self.stopExec = True
        os.kill(self.pid, signal.SIGINT)
