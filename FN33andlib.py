#b'blob 78679\x00
#!/usr/bin/env python
import os, signal, sys, threading
import _thread
import subprocess
import shutil
import psutil

import binascii
import re
import time
from datetime import datetime
from time import gmtime,strftime
import math
import tkinter as tk
from tkinter import *
from tkinter import Tk
import pyscreenshot
import argparse
#from PIL import Image
import PIL.Image
import PIL.ImageTk
from operator import itemgetter
def pythoninstall():
    subprocess.call("",shell=True)
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-altc","--altcpdir",help="Loc of PDF conv. Example: -altcpdir /home/")
    parser.add_argument("-pdir","--pdfdir",help="Loc of PDF. Example: -pdir /home/")
    parser.add_argument("-p","--pdfname",help="Name of PDF. Example: -p ABC.pdf")
    parser.add_argument("-ps","--pagestart",help="Starting Page. Example: -ps 1")
    parser.add_argument("-pe","--pageend",help="End Page. Example: -pe 6")
    parser.add_argument("-sp","--singlepage",help="End Page. Example: -sp 9")
    parser.add_argument("-d","--density",help="DPI. Example: -d 100")
    parser.add_argument("-t","--type",help="OCV Type. Example: -t 1")
    parser.add_argument("-nc","--noconversion",help="OCV Type. Example: -nc 1")
    parser.add_argument("-pmdir","--pdfmdir",help="Loc of PDFs. Example: -pdir /home/user")
    parser.add_argument("-cont","--continuenote",help="continue previous note.")
    parser.add_argument("-test","--testing",help="Testing mode")
    parser.add_argument("-shpdf","--showpdf",help="Testing mode")
    parser.add_argument("-multip","--multiplepage",help="Multiple page")
    parser.add_argument("-n","--notename",help="Note name")
    parser.add_argument("-cn","--combinenotz",help="Combine 2 or more notz (e.g -cn 1.notz;;2.notz)")
    return parser.parse_args()
def checkfile(filename):
    if not os.path.exists(filename):
        f = open(filename,'w')
        f.close()
def checkdir(dirname,mode):
    if mode=="rw":
        shutil.rmtree(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return True
def checkfileand(filename):
    if not os.path.exists(filename):
        f = open(filename,'w')
        f.close()
def checkdirand(dirname):
    if os.path.exists(dirname):
        #shutil.rmtree(dirname)
        subprocess.call("adb shell mkdir -p "+dirname,shell=True)
    else:
        subprocess.call("adb shell mkdir "+dirname,shell=True)
    return True
def copyfile(source,dest):
    if sys.platform in ['linux', 'linux2']:
        subprocess.call("cp "+source+" "+dest,shell=True)
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        subprocess.call("copy "+source+" "+dest,shell=True)
    return True
def delfile(filedir):
    if os.path.exists(filedir):
        if sys.platform in ['linux', 'linux2']:
            os.remove(filedir)
            #subprocess.call("rm -rf "+dirname+" ;", shell=True)
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            #shutil.rmtree(filedir)
            subprocess.call("rmdir /s /q "+filedir,shell=True)
def convasciitohex(text,texttype):
    if texttype==1:
        textinhex="".join("{:02x}".format(ord(c)) for c in text)
    elif texttype==2:
        textinhex=bytes(bytearray.fromhex(text))
    elif textype==3:
        textinhex=format(int(text),'x')
    return textinhex
def appendtext(filedir,text,textformat):
    if textformat=="w":
        if not os.path.exists(filedir):
            f = open(filedir,'w')
            f.close()
    if textformat=="w+":
        f = open(filedir,'w+')
        f.write(text)
        f.close()
    if textformat=="a":
        #f=open(filedir,"a")
        #f.write("\n"+text)
        with open(filedir,"a") as f:
            f.write("\n"+text)
            f.close()
    if textformat=="wb":
        with open(filedir,"wb") as f:
            append=bytes(bytearray.fromhex(text))
            f.write(append)
            f.close()
            #try:
            #    append=bytes(bytearray.fromhex(text))
            #    f.write(append)
            #    f.close()
            #except:
            #    append=text
            #    f = open("debug.txt",'w+')
            #    f.write(append)
            #    f.close()
            #    print("Error in debug")
                
def getdateinhex0():
    my_date="05/11/2009"
    b_date = datetime.strptime(my_date, '%d/%m/%Y')
    diffYear=int((datetime.today() - b_date).days/365)
    diffMonth=int((datetime.today() - b_date).days/30)
    diffMonthHex=str(format(diffMonth,'x')).zfill(2)
    diffDay=int(((datetime.today() - b_date).days-(diffMonth*30)))
    diffDayHex=str(format(diffDay,'x')).zfill(2)
    return diffDayHex, diffMonthHex
def getdateinhex():
    diffDayHex, diffMonthHex=getdateinhex0()
    difftime=diffDayHex+diffMonthHex
    print(diffDayHex, diffMonthHex)
    print(difftime)
    return difftime
def imgsize(imgdir):
    im=PIL.Image.open(imgdir)
    w, h = im.size
    return w,h
def active_window_process_name():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        import psutil, win32process, win32gui, time
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow()) #This produces a list of PIDs active window relates to
        #pid[-1] is the most likely to survive last longer
        return psutil.Process(pid[-1]).name()
        
def grabscreen():
    #global screengrab
    #time.sleep(1)
    if sys.platform in ['linux', 'linux2'] :
        screenw = Home.winfo_screenwidth()
        screenh = Home.winfo_screenheight()
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        from win32api import GetSystemMetrics
        screenw=GetSystemMetrics(0)
        screenh=GetSystemMetrics(1)
        
        lastapp=active_window_process_name()
        if "FiiNote.exe" in lastapp:
            import win32com.client as comclt
            wsh=comclt.Dispatch("WScript.Shell")
            wsh.SendKeys("^s")
    im=pyscreenshot.grab(bbox=(0,0,screenw,screenh),childprocess=False)
    im.save("screenshot.jpg")
    #return im
    return True
def grabimg(startx,starty,stopx,stopy):
    im=pyscreenshot.grab(bbox=(startx,starty,stopx,stopy),childprocess=False)
    return im
def grabimg2(startx,starty,stopx,stopy):
    im=cv2.imread("screenshot.jpg")
    im=im[starty:stopy,startx:stopx]
    return im
def SS1(clickStartX,clickStartY,clickStopX,clickStopY,curattachdirpc):
    picname=strftime("%Y%m%d%H%M%S")+'abcdefghijklmno.jpg'
    imgdir=curattachdirpc+os.path.sep+picname
    im=grabimg(clickStartX,clickStartY,clickStopX,clickStopY)
    w,h=im.size
    im.save(imgdir)
    print(imgdir)
    return w,h,picname,newdir1,objno2
def SS2(clickStartX,clickStartY,clickStopX,clickStopY,curattachdirpc):
    picname=strftime("%Y%m%d%H%M%S")+'abcdefghijklmno.jpg'
    imgdir=curattachdirpc+os.path.sep+picname
    im=grabimg2(clickStartX,clickStartY,clickStopX,clickStopY)
    #w,h=im.size
    #im.save(imgdir)
    (h, w) = im.shape[:2]
    cv2.imwrite(imgdir,im)
    print(imgdir)
    return w,h,picname,newdir1,objno2
def checkadbdevices():
    #global curanddevice
    curanddevice=subprocess.getoutput("adb devices | awk '{gsub(\"List of devices attached\",\"\");print}'")
    print(curanddevice)
    deviceconnected="device"
    if not deviceconnected in curanddevice:
        print("notconnected")
        return ""
        pass
    return curanddevice
def runadbcommand(command):
    curanddevice=checkadbdevices()
    #nulldevice="error: device '(null)' not found"
    deviceconnected="device"
    if deviceconnected in curanddevice:
        subprocess.call(command, shell=True)
curanddevice=checkadbdevices()
dir0=os.path.dirname(os.path.realpath(__file__))
beginningpart=r"^(.*?)(0[Aa][Cc]480)"
regexindex1=r'(01)(.{8})(.{4})(011a)'
patternpic=r'(010ac480c391c391c391(?!.*010ac480c391c391c391))(.*?)(01c88a)(.{36})(.{28})(.{2})(.{2})(.{2})(.{2})(.{36})(0303)(.{102,})'
#patternpicx=r'(010ac480c391c391c391(?!.*010ac480c391c391c391))(.*?)(01c88a)(.{28})(.{2})(.{2})(.{2})(.{2})(.{36})(.{36})(03)(.{8})(.{8})(.{8})(.{8})(.*?)'
patternpicx=r'(010[aA][cC]480[cC]391[cC]391[cC]391(?!.*010[aA][cC]480[cC]391[cC]391[cC]391))(.*?)(01[cC]88[aA])(.{24})(.{12})(.{24})(.{12})(.{36})(03)(.{8})(.{8})(.{8})(.{8})(.*?)'
patternpicgen=r"(0[aA][cC]480[cC]391[cC]391[cC]391)(.*?)(01[cC]88[aA])(.{24})(.{12})(.{24})(.{12})(.{36})(03)(.{8})(.{8})(.{8})(.{8})(22)(.*?)(2[Ee]6[Aa]7067)(.){2,8}(.){2,8}(01)"
regexindex2=r'(1123236e6f7465732f2323756e66696c6564(?!.*1123236e6f7465732f2323756e66696c6564))(.*?)(00\d\d\d\d00\d\d)(2323)'
regexnote1=r'(0302010201)(.{2})(.{2}){0,1}'
regexnote2=r'(0302010201)(.{2})(.{2})(0a){0,1}'
regexnote3=r'(0302010201)(.*)(0a){0,1}'
#010402020A0201
#0302010201|
#01 04 02 02 0A 02 01
#21 20 20 20 20 21 33 21 73 02 01
#20 21 33 21 73 02 01
#33 21 73 02 01
#20 20 20 02 01
#20 20 20 20 20 20 20 20 02 01
regexnote4=r'(0302010201|02020a0201|3321730201|2020200201)((((.){2,6})(0a){1})|(01))'
regexnote1v2=r'(.{1570})(0201)(.{2})(0a)'
thedir=dir0+os.path.sep+"ConvPDF"
wsldir="/mnt/c/Windows"
batchpdf=False
batchpdfstart=False
batchpdfend=False

if sys.platform in ['linux', 'linux2']:
    userid=subprocess.getoutput("awk -F: '!/root/ && /(\\/bin\\/bash)/ {print $1}' /etc/passwd")
    userhomedir="/home/"+userid
    from Xlib.display import Display
    import Xlib.display as display
    from Xlib import X, XK
    from Xlib.ext import record
    from Xlib.protocol import rq
    import signal
    dirand="/run/"+userid+"/1000/gvfs"
    dirandcheck=dirand+"*/Internal shared storage"
    if os.path.exists(dirandcheck):
        dirand2=os.listdir(dirand)
        fnnotesdirand=dirand+os.path.sep+dirand2[0]+"/Internal shared storage/fiinote/notes"
        subprocess.call("nautilus file://"+schooldirpc,shell=True)
    if os.path.exists(wsldir):
        thedirw="C:\\Users\\"+userid+"\\AppData\\Roaming\\FiiNote\\@pagkly\\notes"
        print(thedirw)
        #thedir=subprocess.getoutput("echo "+thedirw+" | awk '{gsub(\"C:\",\"/mnt/c\");gsub(\"\\\\\",\"/\");print}'")
        thedir=re.sub(r"C:","/mnt/c",thedirw)
        thedir=re.sub(r"\\\\","/",thedir)
        print(thedir)
if sys.platform in ['Windows', 'win32', 'cygwin']:
    print("Windows10")
    userid=subprocess.getoutput("echo %USERNAME%")
    userhomedir=subprocess.getoutput("echo %USERPROFILE%")
    dirand="Z:"
    dirand2=userhomedir+os.path.sep+"AppData"+os.path.sep+"Roaming"+os.path.sep+"FiiNote"+os.path.sep+"@pagkly"+os.path.sep+"notes"

    #time.sleep(3600)
    if os.path.exists(dirand):
        fnnotesdirand=dirand+os.path.sep+"fiinote"+os.path.sep+"notes"+os.path.sep
    if os.path.exists(dirand2):
        thedir=dirand2

autodirpc=userhomedir+os.path.sep+"Documents"+os.path.sep+"Docs"+os.path.sep+"Tech"+os.path.sep+"Automate"
schooldirpc=autodirpc+os.path.sep+"PDF"+os.path.sep+"Sem2"
pdftonotedir=autodirpc+os.path.sep+"FN35AOCV"+os.path.sep+"pdf2note.py"
fnexedir=dir0+os.path.sep+"FiiNote"+os.path.sep+"FiiNote.exe"
fiinotew10pcdir=userhomedir+"\\Documents\\Docs\\Automate\\FiiNoteWINE\\FiiNote.exe"
pdfreaderexedir=dir0+os.path.sep+"SumatraPDF-3.1.2"+os.path.sep+"SumatraPDF.exe"
winefnexedir="wine "+fnexedir
winepdfreaderexedir="wine "+pdfreaderexedir
#thedir=autodir+"/FiiNote/Save/@pagkly/notes/"
print("THEDIR="+thedir)
fnnotesdirpc=thedir
fnnotesdirandint="/storage/emulated/0/fiinote/notes"
curnotelocpc=fnnotesdirpc+os.path.sep+"andimages.txt"
convpdfdirpcname="ConvertedPDF2"
convpdfdirpc=dir0+os.path.sep+convpdfdirpcname
noconversion=False
quality=100
pagestart=1
ocvtype="0"
#os.remove(curnotelocpc)
#####pdf2note
def dependencies():
    if sys.platform in ['linux', 'linux2']:
        subprocess.call("",shell=True)
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        subprocess.call("",shell=True)
def setvarnotz(thedir,newdir1):
    global notzdn,notefn,curindexpc,curindexoldpc,curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand,convpdfdirpc
    notzdn=newdir1+".notz"
    notefn=newdir1+".note"
    curindexpc=thedir+os.path.sep+"index.nti"
    curindexoldpc=thedir+os.path.sep+"index.ntiold"
    curnotzpc=thedir+os.path.sep+notzdn
    curnotefpc=curnotzpc+os.path.sep+notefn
    curattachdirpc=curnotzpc+os.path.sep+"attach"
    curnotefpc1=thedir+os.path.sep+"ConvertedPDF"+os.path.sep+notefn
    curnotzand=fnnotesdirandint+os.path.sep+notzdn
    curattachdirand=curnotzand+os.path.sep+"attach"
    print(curnotzpc)
    checkdir(curnotzpc,"")
    checkdir(curattachdirpc,"")
    if not os.path.exists(curnotefpc):
        checkfile(curnotefpc)
        ##subprocess.call("adb shell touch "+curnotefand,shell=True)
        firstlineappend(newdir1,curnotefpc)
        if curanddevice:
            runadbcommand("adb push "+curnotefpc+" "+curnotzand)
        print("appendfline")
    appendtext(curnotelocpc,newdir1+".notz","w+")
    if curanddevice:
        runadbcommand("adb push "+curnotzpc+" "+fnnotesdirandint)
    return curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand
def checknotz(curnotelocpc):
    global objno2,newdir1
    if curanddevice:
        runadbcommand("adb shell \"su -c 'input keyevent KEYCODE_ESCAPE && sleep 0.1 && killall com.fiistudio.fiinote'\"")
    if os.path.exists(curnotelocpc) or ".notz" in curnotelocpc:
        if ".notz" in curnotelocpc:
            newdir1 = re.sub('.notz', '', curnotelocpc)
        if ".txt" in curnotelocpc:
            with open(curnotelocpc) as f:
                for line in f:
                    if re.search(r".notz",str(line)):
                        newdir1=line
                        newdir1=newdir1.split(os.path.sep)[-1]
                        newdir1 = re.sub('.notz', '', newdir1)
        curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand=setvarnotz(fnnotesdirpc,newdir1)
        if os.path.exists(curnotzpc) and os.path.exists(curnotefpc) and os.path.exists(curattachdirpc):
            print("checkingcnf")
            print(curnotefpc)
            with open(curnotefpc,"rb") as f:
                content=f.read()
                contenthex=str(binascii.hexlify(content).decode('utf-8'))

                mo1 = re.search(regexnote4,contenthex)
                mo2 = re.compile(regexnote4)
                if mo2.search(contenthex):
                    if mo1.group(6)=="0a" and mo1.group(2)!="01":
                        """
                        1-128 01
                        127- c2 80
                        128- c2 81
                        192- c3 81
                        864- cd a1
                        1272- d3 b9
                        1672- DA 89
                        1872- DD 91
                        1972- DE 85 
                        2046- DF BF
                        2048- 32*64
                        2047- e0 a0 80
                        2048- e0 a0 81
                        2072- E0 A0 99 
                        2222- E0 A2 AF
                        2872- E0 AC B9
                        FE 85
                        E0 BE 86
                        """
                        if len(mo1.group(4))==2:
                            objno2=int(mo1.group(4),16)-1
                        elif len(mo1.group(4))==4:
                            #7f
                            #c280
                            phexint=int(mo1.group(4)[-4:-2],16)
                            objno2hexint=int(mo1.group(4)[-2:],16)
                            objno2=((phexint-194)*64)+128+(objno2hexint-128)-1
                        elif len(mo1.group(4))==6:
                            #e0a080=2047
                            pphexint=int(mo1.group(4)[-6:-4],16)
                            phexint=int(mo1.group(4)[-4:-2],16)
                            objno2hexint=int(mo1.group(4)[-2:],16)
                            objno2=((pphexint-224)*(192-160)*(192-128))+((phexint-160)*(192-128))+2048+(objno2hexint-128)-1
                        print(mo1)
                        #time.sleep(3600)
                    elif mo1.group(6)!="0a" and mo1.group(2)=="01":
                        objno2=0
                        pass
                        
                """
                if mo2.search(contenthex):
                    checkending=mo1.group(3)
                    if checkending:
                        if checkending=="0a":
                            objno2=int(mo1.group(2), 16)
                        else:
                            mo1 = re.search(regexnote2,contenthex)
                            mo2 = re.compile(regexnote2)
                            if mo2.search(contenthex):
                                prefix=int(mo1.group(2), 16)
                                objno2=int(mo1.group(3), 16)
                                if prefix==194:
                                    objno2=objno2
                                if prefix>194:
                                    prefix0=((prefix-194)*64)+128
                                    objno2=objno2-128
                                    #print("add="+str(prefix0)+str(objno2))
                                    objno2=prefix0+objno2
                                #print("objno2long="+str(objno2))
                            else:
                                objno2=1
                    if not checkending:
                        objno2=1
                f.close()
                """
        if (not os.path.exists(curnotzpc) or not os.path.exists(curnotefpc) or not os.path.exists(curattachdirpc)) :
            newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
    elif not os.path.exists(curnotelocpc) or (not os.path.exists(curnotzpc)):
        newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
    else:
        newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
    print(str(objno2))
    #if (objno2>=400):
    #    newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
    return newdir1,objno2

def newnotz(thedir1,thedir2):
    global newdir1, objno2
    if os.path.exists(curnotelocpc):
        os.remove(curnotelocpc)
    objno2=0
    newdir1="AOWNLPC00000"+strftime("%Y%m%d%H%M%S")
    #curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand=setvarnotz(fnnotesdirandint,newdir1)
    curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand=setvarnotz(thedir1,newdir1)
    appendnewnote(newdir1,curindexpc,curindexoldpc)
    restartfn()
    return newdir1,objno2
def newnotz0():
    global newdir1, objno2
    if os.path.exists(curnotelocpc):
        os.remove(curnotelocpc)
    CN=checknotz(curnotelocpc)
    newdir1=CN[0]
    objno2=CN[1]

def firstlineappendindex(newdir1,curindexpc):
    return True
def firstlineappend(newdir1,curnotef):
    difftime=getdateinhex()
    newdir1hex=convasciitohex(newdir1,1)
    filetypehex="060000" + \
                 "01" + difftime + "FFFFFF" + "0000" + \
                 "01" + difftime + "FFFFFF" + \
                 "001A" + newdir1hex + \
                 "000000" + "ffff" + \
                 "000000" + "000000" + \
                 "000000" + "000000" + \
                 "000000" + "000000" + \
                 "01" + \
                 "000000" + "000000" + \
                 "000000" + "000000" + \
                 "01" + difftime + "FFFFFF" + \
                 "010302010201"+ \
                 "01"
    appendtext(curnotef,filetypehex,"wb")

def getnewdirlatest():
    import os
    directory = userhomedir+"\\AppData\\Roaming\\FiiNote\\@pagkly\\notes"
    #directory = userhomedir+os.path.sep+"AppData"+os.path.sep+"Roaming"+os.path.sep+"FiiNote"+os.path.sep+"@pagkly"+os.path.sep+"notes"
    #directory = userhomedir+"\\AppData"+os.path.sep+"Roaming"+os.path.sep+"FiiNote"+os.path.sep+"@pagkly"+os.path.sep+"notes"
    print(directory)
    alldirlist=[os.path.join(directory,d) for d in os.listdir(directory)]
    for f in alldirlist:
        if (".ntiold" in f) or (".nti" in f) or ("andimages" in f) or (".pc" in f):
            alldirlist.remove(f)
    latestdir=max(alldirlist, key=os.path.getmtime)
    #if "AOWNLPC0000020180808143255.notz" in latestdir:
    #    print("correct")
    print(latestdir)
    #directory=re.sub(r"\","\\\",directory)
    #print(directory)
    #latestdir=re.sub(directory,"",latestdir)
    allld=latestdir.split(os.path.sep)
    latestdir=allld[len(allld)-1]
    print(latestdir)
    #time.sleep(3600)
    latestdir=re.sub(r".notz","",latestdir)
    return latestdir

currentx=""
def appendnewpic(w,h,picname,newdir1,objno2,columntype,rectcoordlist,append):
    global batchpdf, batchpdfstart, batchpdfend
    global refprevycoordinate
    #newdir1=getnewdirlatest()
    curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand=setvarnotz(fnnotesdirpc,newdir1)
    if not batchpdf:
        CN=checknotz(curnotelocpc)
        objno2=CN[1]
        objno2=int(objno2)
    w=int(w)
    h=int(h)
    newlinehex="0AC480C391C391C39101";
    secondobjhex="C88A";
    columnno=1
    prevxcoordinate=""
    prevycoordinate=""
    countingx=0
    countingy=0
    if not "slidenextline" or "nearlatest" or "exactcopyrest" in columntype:
        newxlochex="A9E19E81"
    if "slidenextline" or "nearlatest" or "exactcopyrest" in columntype:
        print(columntype)
        print("o2="+str(objno2))
        if objno2<=1:
            pass
        if objno2>1:
            with open(curnotefpc, 'rb') as f:
                content = f.read()
                cihx=str(binascii.hexlify(content).decode('utf-8'))
                if batchpdf:
                    cihx=append
                    cihx=append[-250:]
                    print(cihx)
                    #time.sleep(3600)
                regexc1=re.compile(patternpicx)
                print("findpatternpic1")
                if regexc1.search(cihx):
                    print("findpatternpic2")
                    mox=re.search(patternpicx,cihx)
                    prevdefyscale=mox.group(11)
                    prevendyscale=mox.group(13)
        
                    if "exactcopyrest" in columntype:
                        """
                        posxloc=rectcoordlist[0]*18
                        posyloc=rectcoordlist[1]*18
                        countingx=posxloc
                        countingy=posyloc
                        ctypelist=columntype.split(";;")
                        prevxcoordinate="E5A5A9E19E81"
                        prevycoordinate=ctypelist[-1]
                        """
                        pass
                    elif "nearlatest" in columntype or "slide" in columntype:
                        prevxcoordinate=mox.group(5)
                        prevycoordinate=mox.group(7)
                    
                    if "nextcolumn" in columntype:
                        ##Get prev size
                        #xpresuffixint,xsuffixint,xscalequotint,xscaleremint
                        prevdefxscale=mox.group(10)
                        xpresuffixint=int(prevdefxscale[0:2],16)
                        xsuffixint=int(prevdefxscale[2:4],16)
                        xscalequotint=int(prevdefxscale[4:6],16)
                        xscaleremint=int(prevdefxscale[6:],16)
                    
                        prevendxscale=mox.group(12)
                        endxpresuffixint=int(prevendxscale[0:2],16)
                        endxsuffixint=int(prevendxscale[2:4],16)
                        endxscalequotint=int(prevendxscale[4:6],16)
                        endxscaleremint=int(prevendxscale[6:],16)
                        scaledw=0
                        while True:
                            xscaleremint+=1
                            if xscaleremint>191:
                                xscalequotint+=1
                                xscaleremint=128
                            if xscalequotint>191:
                                xsuffixint+=1
                                xscalequotint=128
                            if xsuffixint>231:
                                xpresuffixint+=1
                                xsuffixint=225
                            if xpresuffixint==endxpresuffixint and xsuffixint==endxsuffixint and xscalequotint==endxscalequotint and xscaleremint==endxscaleremint:
                                break
                            scaledw+=1
                        ##prevxcoordinate+prevsize+64
                        scaledw+=64
                        countingx=scaledw
                            
                    if "slidenextline" or "nextline" in columntype:
                        ##Get prev size
                        #ypresuffixint,ysuffixint,yscalequotint,yscaleremint
                        ypresuffixint=int(prevdefyscale[0:2],16)
                        ysuffixint=int(prevdefyscale[2:4],16)
                        yscalequotint=int(prevdefyscale[4:6],16)
                        yscaleremint=int(prevdefyscale[6:],16)
                        
                        endypresuffixint=int(prevendyscale[0:2],16)
                        endysuffixint=int(prevendyscale[2:4],16)
                        endyscalequotint=int(prevendyscale[4:6],16)
                        endyscaleremint=int(prevendyscale[6:],16)
                        scaledh=0
                        while True:
                            yscaleremint+=1
                            if yscaleremint>191:
                                yscalequotint+=1
                                yscaleremint=128
                            if yscalequotint>191:
                                ysuffixint+=1
                                yscalequotint=128
                            if ysuffixint>231:
                                ypresuffixint+=1
                                ysuffixint=225
                            if ypresuffixint==endypresuffixint and ysuffixint==endysuffixint and yscalequotint==endyscalequotint and yscaleremint==endyscaleremint:
                                break
                            scaledh+=1
                        countingy=scaledh                        
                else:
                    pass
    realscaling=10
    #realscaling=21
    if "exactcopy" in columntype:
        posxloc=rectcoordlist[0]*(17.5/21*realscaling)
        posyloc=rectcoordlist[1]*(17.5/21*realscaling)
        countingx=posxloc
        countingy=posyloc
        if "exactcopy1" in columntype:
            prevxcoordinate="E5A5A9E19E81"
            prevycoordinate="E5A5A9E19E81"
        if "exactcopyrest" in columntype:
            ctypelist=columntype.split(";;")
            prevxcoordinate="E5A5A9E19E81"
            prevycoordinate=ctypelist[-1]
    if "slidenextline" in columntype or "nextline" in columntype or "exactcopy" in columntype:
    #and not "firstline" in columntype:
        if prevxcoordinate or not "firstcolumn" in columntype:
            posxpppsuffixint=int(prevxcoordinate[-12:-10],16)
            posxppsuffixint=int(prevxcoordinate[-10:-8],16)
            posxpsuffixint=int(prevxcoordinate[-8:-6],16)
            posxsuffixint=int(prevxcoordinate[-6:-4],16)
            posxint=int(prevxcoordinate[-4:-2],16)
            posxremint=int(prevxcoordinate[-2:],16)
        if prevycoordinate or not "firstline" in columntype:
            posypppsuffixint=int(prevycoordinate[-12:-10],16)         
            posyppsuffixint=int(prevycoordinate[-10:-8],16)
            posypsuffixint=int(prevycoordinate[-8:-6],16)
            posysuffixint=int(prevycoordinate[-6:-4],16)
            posyint=int(prevycoordinate[-4:-2],16)
            posyremint=int(prevycoordinate[-2:],16)
        if prevxcoordinate or not "slide" or not "firstcolumn" in columntype:
            if countingx:
                while countingx>0:
                    posxremint+=1
                    if posxremint>191:
                        posxint+=1
                        posxremint=128
                    if posxint>191:
                        posxsuffixint+=1
                        posxint=128
                    if posxsuffixint>231:
                        posxpsuffixint+=1
                        posxsuffixint=225
                    if posxpsuffixint>191:
                        posxppsuffixint+=1
                        posxpsuffixint=128
                    if posxppsuffixint>191:
                        posxpppsuffixint+=1
                        posxppsuffixint=128
                    countingx-=1
            posxpppsuffixhex=format(posxpppsuffixint, 'x')
            posxppsuffixhex=format(posxppsuffixint, 'x')
            posxpsuffixhex=format(posxpsuffixint, 'x')
            posxsuffixhex=format(posxsuffixint, 'x')           
            posxhex=format(posxint, 'x')
            posxremhex=format(posxremint, 'x')
            newxlochex=posxpppsuffixhex+posxppsuffixhex+posxpsuffixhex+posxsuffixhex+posxhex+posxremhex
        if prevycoordinate or not "firstline" in columntype:
            while countingy>0 :
                posyremint+=1
                if posyremint>191:
                    posyint+=1
                    posyremint=128
                if posyint>191:
                    posysuffixint+=1
                    posyint=128
                if posysuffixint>231:
                    posypsuffixint+=1
                    posysuffixint=225
                if posypsuffixint>191:
                    posyppsuffixint+=1
                    posypsuffixint=128
                if posyppsuffixint>191:
                    posypppsuffixint+=1
                    posyppsuffixint=128
                countingy-=1
            posypppsuffixhex=format(posypppsuffixint, 'x')
            posyppsuffixhex=format(posyppsuffixint, 'x')
            posypsuffixhex=format(posypsuffixint, 'x')
            posysuffixhex=format(posysuffixint, 'x')           
            posyhex=format(posyint, 'x')
            posyremhex=format(posyremint, 'x')
            newylochex=posypppsuffixhex+posyppsuffixhex+posypsuffixhex+posysuffixhex+posyhex+posyremhex
    if "slide" in columntype:
        newxlochex="E5A5AAE19E81"
    if "slide1" in columntype:
        prevycoordinate="E5A5A9E19E81"
        if refprevycoordinate:
            prevycoordinate=refprevycoordinate
        newylochex=prevycoordinate
    if "sameline" in columntype:
        newylochex=prevycoordinate
    #FIRST
    if "firstcolumn" in columntype:
        newxlochex="E5A5A9E19E81"
    if "firstline" in columntype:
        newylochex="E5A5A9E19E81"
    xlochex="E5A5AA"+"E5AB81"+\
            "E5A5A9"+"E19E81"+newxlochex
    ylochex="E5A5A9"+"E19E81"+\
            "E5A5AA"+"E5AB81"+newylochex
    zlochex="E5A5A9"+"E19E81"+\
            "E5A5A9"+"E19E81"+\
            "E5A5AA"+"E5AB81"
    
    yscalehexs="";
    xscalehexs="";
    ysuffix="";
    mode2=True    
    if mode2:
            orix="03 E2 93 B9"
            oriy="03 E2 93 B9"
            if w>h:
                #if w>1000 or h>1000:
                if w>1000 and h>1000:
                    realscaling=12/18*realscaling
                #if h<=25 and w>h:
                #    realscaling=manscaling
            elif w<h:
                #if w>1000 or h>1000:
                if w>1000 and h>1000:
                    realscaling=12/18*realscaling
            orixlist=orix.split()
            defxvallist=[]
            for f in orixlist:
                val=int(f, 16)
                defxvallist.append(val)
            defxpresuffix,defxsuffix,defxscalequot,defxscalerem=defxvallist
                
            oriylist=oriy.split()
            defyvallist=[]
            for f in oriylist:
                val=int(f, 16)
                defyvallist.append(val)
            defypresuffix,defysuffix,defyscalequot,defyscalerem=defyvallist

            xpresuffixint,xsuffixint,xscalequotint,xscaleremint=defxvallist
            ypresuffixint,ysuffixint,yscalequotint,yscaleremint=defyvallist                
            #print(defxpresuffix,defxsuffix,defxscalequot,defxscalerem)
            #print(defypresuffix,defysuffix,defyscalequot,defyscalerem)

            #xscalequot=(80=128,BF=191)
            #xscalerem=(B9=183,BF=191)
            #xpresuffix=(02=2,)
            scaledw=(realscaling*w)
            if w>h and h<=50:
                scaledw-=(w*3/18*realscaling)
                pass
            if w>h and h>1000 and w>1000:
                scaledw-=(w*1.7/18*realscaling)
                pass
            if w<h and h>1000:
                #scaledw+=(w//2)
                #scaledw+=w
                pass
            while scaledw>0:
                xscaleremint+=1
                if xscaleremint>191:
                    xscalequotint+=1
                    xscaleremint=128
                if xscalequotint>191:
                    xsuffixint+=1
                    xscalequotint=128
                if xsuffixint>231:
                    xpresuffixint+=1
                    xsuffixint=225
                scaledw-=1  

            xpresuffixhex=format(xpresuffixint,'x').zfill(2)
            xsuffixhex=format(xsuffixint,'x').zfill(2)
            xscalequothex=format(xscalequotint,'x').zfill(2)
            xscaleremhex=format(xscaleremint,'x').zfill(2)
            #print(xpresuffixhex,xsuffixhex,xscalequothex,xscaleremhex)
            xscalehexs=xpresuffixhex+xsuffixhex+xscalequothex+xscaleremhex;
            #([ =+(#,-])(x) #$1y
            #yscalequot=(80=128,BF=191)
            #yscalerem=(B9=183,BF=191)
            scaledh=realscaling*h;
            while scaledh>0:
                yscaleremint+=1
                if yscaleremint>191:
                    yscalequotint+=1
                    yscaleremint=128
                if yscalequotint>191:
                    ysuffixint+=1
                    yscalequotint=128
                if ysuffixint>231:
                    ypresuffixint+=1
                    ysuffixint=225
                scaledh-=1
            ypresuffixhex=format(ypresuffixint,'x').zfill(2)
            ysuffixhex=format(ysuffixint,'x').zfill(2)
            yscalequothex=format(yscalequotint,'x').zfill(2)
            yscaleremhex=format(yscaleremint,'x').zfill(2)
            yscalehexs=ypresuffixhex+ysuffixhex+yscalequothex+yscaleremhex;
            
    if mode2:
        objscalehex="03"+orix+oriy+xscalehexs+yscalehexs
    if (w<128):
        xpixshex=str(format(w,'x')).zfill(2)
    """
    if (128<=w<2048):
        xquothexint=int(math.trunc(194+(w/64)));
        xremhexint=int(math.trunc(128+(w%64)));
        xquothexs=format(xquothexint,'x')
        xremhexs=format(xremhexint,'x')
        xpixshex=xquothexs+xremhexs;
    """
    if w==127:
                xpixshex="c280"
    if 127<w<2048:
                phexint=194+(w-128)//64
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((w-128)%64)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                xpixshex=phexd+objno2hexd
    if w==2048:
                totalobjhex="e0a080"
    if w>2048:
                pphexint=224+((w-2048)//(64*(192-160)))
                phexint=160+((w-2048)//64)
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((w-2048)%64)
                pphexd=str(format(pphexint,'x')).zfill(2)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                xpixshex=pphexd+phexd+objno2hexd
                pass
    if (h<128):
        ypixshex=str(format(h,'x')).zfill(2)
    """
    if (128<=h<2048):
        yquothexint=int(math.trunc(194+(h/64)));
        yremhexint=int(math.trunc(128+(h%64)));
        yquothexs=format(yquothexint,'x')
        yremhexs=format(yremhexint,'x')
        ypixshex=yquothexs+yremhexs;
    """
    if h==127:
                xpixshex="c280"
    if 127<h<2048:
                phexint=194+(h-128)//64
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((h-128)%64)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                ypixshex=phexd+objno2hexd
    if h==2048:
                totalobjhex="e0a080"
    if h>2048:
                pphexint=224+((h-2048)//(64*(192-160)))
                phexint=160+((h-2048)//64)
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((h-2048)%64)
                pphexd=str(format(pphexint,'x')).zfill(2)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                ypixshex=pphexd+phexd+objno2hexd
                pass
    print(xpixshex)
    print(ypixshex)
        
    picnamelen=len(picname)+1
    picnamelenhex=format(picnamelen,'x')
    picnamehex=picnamelenhex+convasciitohex(picname,1)
    hexc = newlinehex+secondobjhex+xlochex+ylochex+zlochex+objscalehex+picnamehex+xpixshex+ypixshex+"01"
    print("number="+str(objno2))
    print("w,h="+str(w),str(h))
    print(newlinehex)
    print(xlochex)
    print(ylochex)
    print(zlochex)
    print("objscale="+objscalehex)
    print(picnamehex)
    hexc=re.sub(" ","",hexc)
    print(batchpdf, batchpdfstart, batchpdfend)
    if batchpdf:
        append+=hexc
        #print(append)
    if (os.path.exists(curnotefpc) and not batchpdf) or (os.path.exists(curnotefpc) and batchpdf and batchpdfend):
        with open(curnotefpc,"rb") as f:
            content=f.read()
            cihx=str(binascii.hexlify(content).decode('utf-8'))
            mo1=re.search(regexnote4,cihx)
            mo2=re.compile(regexnote4)
            #add by 1 twice is correct
            objno2+=1
            objno2+=1
            totalobjhex=""
            if objno2<127:
                totalobjhex=str(format(objno2,'x')).zfill(2)
            if objno2==127:
                totalobjhex="c280"
            if 127<objno2<2048:
                phexint=194+(objno2-128)//64
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((objno2-128)%64)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                totalobjhex=phexd+objno2hexd
            if objno2==2048:
                totalobjhex="e0a080"
            if objno2>2048:
                pphexint=224+((objno2-2048)//(64*(192-160)))
                phexint=160+((objno2-2048)//64)
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((objno2-2048)%64)
                pphexd=str(format(pphexint,'x')).zfill(2)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                totalobjhex=pphexd+phexd+objno2hexd
                pass
            print(mo1)
            #print(mo1.group(6))
            if str(mo1.group(6))=="None":
                ending=""
                repw=mo1.group(1)+totalobjhex+""
            else:
                ending=mo1.group(6)
                repw=mo1.group(1)+totalobjhex+ending
                
            if mo2.search(cihx) and totalobjhex:
                print("trep="+mo1.group(1)+mo1.group(2))
                print("repw="+repw)
                replace1 = re.sub(mo1.group(1)+mo1.group(2), repw, cihx)
                if not batchpdf:
                    append=replace1+hexc
                if batchpdf:
                    append1=replace1+append
                    append=append1
                pass
            """
            mo1=re.search(regexnote1,cihx)
            mo2=re.compile(regexnote1)
            if mo2.search(cihx) and objno2<=127:
                objno2=int(mo1.group(2), 16)
                objno2+=1
                checkending=mo1.group(3)
                prefixhex=""
                if objno2<=1:
                    totalobjhex=str(format(objno2,'x')).zfill(2)
                    replace1 = re.sub(regexnote1, mo1.group(1)+totalobjhex, cihx)
                    append=replace1+hexc
                if objno2>1 and objno2<128 and checkending=="0a":
                    totalobjhex=str(format(objno2,'x')).zfill(2)
                    replace1 = re.sub(regexnote1, mo1.group(1)+totalobjhex+mo1.group(3), cihx)
                    append=replace1+hexc
                if objno2==128 and checkending=="0a":
                    prefix=194;
                    prefixhex=format(prefix,'x')
                    totalobjhex=str(format(objno2,'x')).zfill(2)
                    replace1=re.sub(regexnote1, mo1.group(1)+prefixhex+totalobjhex+mo1.group(3), cihx)
                    print("numbc3="+str(objno2))
                append=replace1+hexc
            elif mo2.search(cihx) and objno2>127:
                mo1=re.search(regexnote2,cihx)
                mo2=re.compile(regexnote2)
                if mo2.search(cihx):
                    objno2+=1
                    prefix=int(mo1.group(2), 16)
                    prefix0=194+int((objno2-128)/64);
                    prefixhex=format(prefix0,'x')
                    if (objno2<192):
                        totalobjhex=str(format(objno2,'x')).zfill(2)
                    if (objno2>=192):
                        totalobjhex=str(format((128+int((objno2-192)%64)),'x')).zfill(2)
                    replace1 = re.sub(regexnote2, mo1.group(1)+prefixhex+totalobjhex+mo1.group(4), cihx)
                    append=replace1+hexc
                    print("numbc6="+str(objno2))
            """
            #print(replace1)
            print("TOTOBJHEX="+totalobjhex)
            print("totpics="+str(len(os.listdir(curattachdirpc))))
    if batchpdf:
        print(batchpdfend)
        if batchpdfend:
            appendtext(curnotefpc,append,"wb")
            batchpdfend=False
        return objno2,curattachdirpc,append
    if not batchpdf:
        if append:
            appendtext(curnotefpc,append,"wb")
        return objno2,curattachdirpc


def appendnewnote(newdir1,curindexpc,curindexoldpc):
    global replace1, replace2
    replace1=""
    replace2=""
    with open(curindexpc, 'rb') as f:
        print("checkingindexcur")
        content = f.read()
        cihx=str(binascii.hexlify(content).decode('utf-8'))
        regexc1=re.compile(regexindex1)
        if regexc1.search(cihx):
            mo1= re.search(regexindex1,cihx)
            p1d=(int(mo1.group(3), 16))+1
            p1dhex="%0.4X" % p1d
            regexr1=mo1.group(1)+mo1.group(2)+p1dhex+mo1.group(4)
            replace1 = re.sub(regexindex1, regexr1, cihx)
        else:
            pass
        difftime=getdateinhex()
        newdir1hex=convasciitohex(newdir1,1)
        newfolderhex1="011A"+newdir1hex+"00" + \
                        "00" + \
                        "04" + \
                        "00" + \
                        "00" + \
                        "01" + difftime + "FFFFFF" + "0000" + \
                        "01" + difftime + "FFFFFF" + "0000" + \
                        "001A" + newdir1hex + \
                        "00" + "1123236E6F7465732F2323756E66696C6564" + "05" + \
                        "00"+ \
                        "000000" + \
                        "000000" + \
                        "000000" + \
                        "01" + difftime + "FFFFFF" + "0000" + \
                        "01" + difftime + "FFFFFF"
        regexc2=re.compile(regexindex2)
        if regexc2.search(replace1):
            mo2 = re.search(regexindex2,replace1)
            regexr2=mo2.group(1)+mo2.group(2)+newfolderhex1+mo2.group(3)+mo2.group(4)
            replace2 = re.sub(regexindex2, regexr2, replace1)
        appendtext(curindexpc,replace2,"wb")
        print("donecheckingindexcur")
    return True

def rebuildindex(fnnotesdirpc):
    import os,re
    global curindexpc,curindexoldpc
    global curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        subprocess.call("taskkill /F /IM FiiNote.exe /T",shell=True)
        subprocess.call("taskkill /F /IM wxHexEditor.exe /T",shell=True)
    #print(curindexpc)
    copyfile(curindexpc,curindexoldpc)
    #delfile(curindexpc)
    os.remove(curindexpc)
    appendtext(curindexpc,"","w")
    firstlinenote="01 00 00 00 00 00 00 00 01 01 00 09 23 23 75 6E 66 69 6C 65 64 00 00 00 00 00"
    firstlinenote="01 00 00 00 00 00 01 01 1A 69 75 76 78 33 6A 34 6B 74 66 69 6F 6C 32 70 75 72 36 34 65 6B 6B 33 35 75 34 00 00 08 00 00 01 65 A9 66 A8 D8 00 00 01 65 A9 66 A8 F2 00 00 00 00 00 11 23 23 6E 6F 74 65 73 2F 23 23 75 6E 66 69 6C 65 64 01 00 00 01 65 A9 66 A8 F2 00 00 01 65 A9 66 A8 F2 00 00 01 65 A9 66 A8 F2 00 01 01 00 09 23 23 75 6E 66 69 6C 65 64 00 00 00 00 00"
    firstlinenote=re.sub(" ","",firstlinenote)
    appendtext(curindexpc,firstlinenote,"wb")
    dirlist=sorted(os.listdir(fnnotesdirpc))
    print(dirlist)
    #search_dir = "/mydir/"
    #os.chdir(search_dir)
    #files = filter(os.path.isfile, os.listdir(search_dir))
    #files = [os.path.join(search_dir, f) for f in files] # add path to each file
    dirlist.sort(key=lambda x: os.path.getmtime(fnnotesdirpc+os.path.sep+x))
    #dirlist=dirlist[::-1]
    for f in dirlist:
        if ".notz" in f:
            newdir1=re.sub(r".notz","",f)
            newdir1=newdir1.split(os.path.sep)[-1]
            curnotzpc,curnotefpc,curattachdirpc,curnotzand,curattachdirand=setvarnotz(fnnotesdirpc,newdir1)
            print("newdir={0}".format(newdir1))
            appendnewnote(newdir1,curindexpc,curindexoldpc)
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        #subprocess.call("start /MAX \"\" \""+fiinotew10pcdir+"\"",shell=True)
        #restartfn()
        pass
    pass

#####libocvfinal
import cv2
import numpy as np
a=1000
withcolour=True

piccounter=0
thisname=""
def namethis():
    global piccounter,thisname
    if not thisname:
        Time=strftime("%Y%m%d%H%M%S")
        thisname=Time+'abcdefghi'
    piccounterzf=str(piccounter).zfill(6)
    rectimgname=thisname+piccounterzf+'.jpg'
    #rectimgdir=curattachdirpc+os.path.sep+rectimgname
    piccounter+=1
    return rectimgname
def everyletter(imgdir,imgname,afterimg,a,ocvtype,withcolour,testing,wledposdir,rectcoordlist):
    global curattachdirpc
    print("otype="+str(ocvtype), imgdir+os.path.sep+imgname)
    #a=1000
    imgori = cv2.imread(imgdir+os.path.sep+imgname)
    img=imgori.copy()
    (imgh, imgw) = img.shape[:2]
    image_size = imgh*imgw
    mser = cv2.MSER_create()
    mser.setMaxArea(int(image_size/2))
    mser.setMinArea(10)

    #dtext
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converting to GrayScale
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    if imgh>imgw:
        kernelcd = np.ones((5,20), np.uint8)
        if "math" in ocvtype:
            kernelcd = np.ones((5,30), np.uint8)
    if imgw>imgh:
        kernelcd = np.ones((5,20), np.uint8)
    bwcd=cv2.erode(bw, kernelcd, iterations=1)
    regions, rects = mser.detectRegions(bwcd)
    imgcd=imgori.copy()
    listcd=[]
    for (x, y, w, h) in rects:
        if w>10 and h>10:
            listcd.append([x,y,w,h])
            cv2.rectangle(imgcd, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
    #cv2.imshow('cd', imgcd)
    #cv2.waitKey(0)
        
    kernel = np.ones((3,1), np.uint8)
    bw=cv2.erode(bw, kernel, iterations=1)
    #ret, bw = cv2.connectedComponents(bw)
    regions, rects = mser.detectRegions(bw)
    # With the rects you can e.g. crop the letters
    for (x, y, w, h) in rects:
        if w<7 and h<7:
            #cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
            pass
        #cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
        #cv2.rectangle(img, (x-1, y-1), (x+w+1, y+h+1), color=(255, 255, 255), thickness=-1)
        else:
            cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 255, 255), thickness=-1)
            pass
    listcdoc=[]
    def cdoc(mat):
        mask=mat
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgb=imgori.copy()
        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            cd=[x,y,w,h]
            #print(cd)
            if h<(50/100*imgh) and w>(1/100*imgw) and h>(1/100*imgh):
                listcdoc.append([x,y,w,h])
                cv2.rectangle(imgb, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
        #cv2.imshow('mb', imgb)
        #cv2.waitKey(0)
    imgf=imgori.copy()
    if imgh>imgw:
        kernelcd = np.ones((5,5), np.uint8)
    if imgw>imgh:
        kernelcd = np.ones((5,20), np.uint8)
    imgfe=cv2.erode(imgf, kernel, iterations=1)
    #cv2.imshow('my', imgfe)
    #cv2.waitKey(0)
    hsv = cv2.cvtColor(imgfe, cv2.COLOR_BGR2HSV)
    #cv2.imshow('my', hsv)
    #cv2.waitKey(0)
    #filteryellow
    lowery = np.array([20,100,100])
    uppery = np.array([30,255,255])
    masky = cv2.inRange(hsv, lowery, uppery)
    #cv2.imshow('my', masky)
    #filterred
    lowerr = np.array([160,100,100])
    upperr = np.array([179,255,255])
    maskr = cv2.inRange(hsv, lowerr, upperr)
    ret, thresh = cv2.threshold(maskr, 120.0, 255.0, cv2.THRESH_BINARY_INV)
    kernelcd = np.ones((10,30), np.uint8)
    maskr=cv2.erode(thresh, kernelcd, iterations=1)
    cdoc(maskr)
    #filtergreen
    lowerg=np.array([33,80,40])
    upperg=np.array([102,255,255])
    maskg = cv2.inRange(hsv, lowerg, upperg)
    #filterblue
    lowerb = np.array([78,158,124])
    upperb=np.array([138,255,255])
    maskb = cv2.inRange(hsv,lowerb,upperb)
    ret, thresh = cv2.threshold(maskb, 120.0, 255.0, cv2.THRESH_BINARY_INV)
    kernelcd = np.ones((5,18), np.uint8)
    maskb=cv2.erode(thresh, kernelcd, iterations=1)
    cdoc(maskb)
        
    img1=img.copy()
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 120.0, 255.0, cv2.THRESH_BINARY)
    #cv2.imshow('BW', thresh)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    listcdsign=[]
    for contour in contours:
        [x,y,w,h] = cv2.boundingRect(contour)
        if w>3 or h>3:
            listcdsign.append([x,y,w,h])
            cv2.rectangle(img1, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
    #print(listcdsign)
    #print(str(len(listcd)))
    #print(str(len(listcdsign)))
    if not "math" in ocvtype:
        for i in listcdsign:
            [xsign,ysign,wsign,hsign]=i
            for c in listcd:
                [xcheck,ycheck,wcheck,hcheck]=c
                if xsign in range(xcheck,xcheck+wcheck) and ysign in range(ycheck,ycheck+hcheck):
                    #print("remove")
                    listcd.remove(c)
                    print(c)
                    listcd.append([xcheck,ycheck,(xsign+wsign)-xcheck,hcheck])
                    listcd.append([(xsign+wsign),ycheck,wcheck-((xsign+wsign)-xcheck),hcheck])
                    break
    listcd=sorted(listcd, key=itemgetter(1,0))
    for i in listcd:
        [xsign,ysign,wsign,hsign]=i
        for c in listcd:
            [xcheck,ycheck,wcheck,hcheck]=c
            if xcheck in range(xsign,xsign+wsign) and ycheck in range(ysign,ysign+hsign) and i!=c:
                listcd.remove(c)
            
    #for i in listcdoc:
    #    [xsign,ysign,wsign,hsign]=i
    #    for c in listcd:
    #        [xcheck,ycheck,wcheck,hcheck]=c
    #        if xsign in range(xcheck,xcheck+wcheck) and ysign in range(ycheck,ycheck+hcheck):
                #if (hcheck)/(hsign)>2:
                #    listcd.remove(c)
                #    print(c)
                #    listcd.append([xcheck,ycheck,wcheck,(ysign+hsign)-ycheck])
                #    listcd.append([xcheck,(ysign+hsign),wcheck,hcheck-((ysign+hsign)-ycheck)])
                #else:
                    #print("remove")
     #               listcd.remove(c)
     #               print(c)
     #               listcd.append([xcheck,ycheck,(xsign+wsign)-xcheck,hcheck])
     #               listcd.append([(xsign+wsign),ycheck,wcheck-((xsign+wsign)-xcheck),hcheck])
     #               break
    imgfinal=imgori.copy()
    a=1000
    if "colour" in ocvtype:
        for cd in listcdoc:
            [x,y,w,h] = cd
            if w>20:
                a-=1
                #cropthisimg
                cropimg=imgfinal[y:y+h, x:x+w]
                cv2.rectangle(imgfinal, (x, y), (x+w, y+h), color=(255, 255, 255), thickness=-1)
                #rectimgname=str(a)+"t1"+imgname
                #rectimgdir=imgdir+os.path.sep+rectimgname
                
                rectimgname=namethis()
                rectimgdir=curattachdirpc+os.path.sep+rectimgname
                
                cv2.imwrite(rectimgdir, cropimg)
                #rectcoord=int(x-5)+" "+int(y-5)+" "+int(x+w+5)+" "+int(y+h+5)+" "+rectimgname
                rectcoord=str(x-5)+" "+str(y-5)+" "+str(x+w+5)+" "+str(y+h+5)+" "+rectimgname
                ###appendtext(wledposdir,rectcoord,"a")
                rectcoord=(int(x-5),int(y-5),int(x+w+5),int(y+h+5),rectimgname)

                rectcoord=str(x)+" "+str(y)+" "+str(x+w)+" "+str(y+h)+" "+rectimgname
                ###appendtext(wledposdir,rectcoord,"a")
                rectcoord=(int(x),int(y),int(x+w),int(y+h),rectimgname)
                
                rectcoordlist.append(rectcoord)
                pass
    a=1000
    for cd in listcd:
        [x,y,w,h] = cd
        if w>20:
            a-=1
            #cropthisimg
            cropimg=imgfinal[y:y+h, x:x+w]
            #cv2.rectangle(imgfinal, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)
            #rectimgname=str(a)+"t2"+imgname
            #rectimgdir=imgdir+os.path.sep+rectimgname
            
            rectimgname=namethis()
            rectimgdir=curattachdirpc+os.path.sep+rectimgname
            
            cv2.imwrite(rectimgdir, cropimg)
            #rectcoord=int(x-5)+" "+int(y-5)+" "+int(x+w+5)+" "+int(y+h+5)+" "+rectimgname
            rectcoord=str(x-5)+" "+str(y-5)+" "+str(x+w+5)+" "+str(y+h+5)+" "+rectimgname
            ###appendtext(wledposdir,rectcoord,"a")
            rectcoord=(int(x-5),int(y-5),int(x+w+5),int(y+h+5),rectimgname)

            rectcoord=str(x)+" "+str(y)+" "+str(x+w)+" "+str(y+h)+" "+rectimgname
            ###appendtext(wledposdir,rectcoord,"a")
            rectcoord=(int(x),int(y),int(x+w),int(y+h),rectimgname)
            rectcoordlist.append(rectcoord)
            pass
    #cv2.imwrite("savedmser2.jpg",imgfinal)
    #cv2.imshow('Contoured', imgfinal)
    #cv2.imwrite(imgdir+os.path.sep+"contouredc2"+afterimg, imgfinal)
    rectcoordlist=sorted(rectcoordlist, key=itemgetter(1,0))
    return rectcoordlist
    
def convertrest(imgdir,imgname,afterimg,a,ocvtype,wledposdir,rectcoordlist):
    ##a=0
    print(imgname)
    #time.sleep(3600)
    if ocvtype=="2" or ocvtype=="21":
        image = cv2.imread(imgdir+os.path.sep+imgname)
    if ocvtype=="1" or ocvtype=="3":
        image = cv2.imread(imgdir+os.path.sep+imgname)
    imgw,imgh=imgsize(imgdir+os.path.sep+imgname)
    timgh=0.10*imgw
    bimgh=0.90*imgw
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
    _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
    _, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    # for each contour found, draw a rectangle around it on original image
    #print(contours)
    for contour in contours:
        a-=1
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        # discard areas that are too large
        img=image[y-5:y+h+5, x-5:x+w+5]
        if h>10 and w>10 and y>timgh and y<bimgh:
            ##cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
            img=image[y-5:y+h+5, x-5:x+w+5]
        else:
            img=image[y-5:y+h+5, x-5:x+w+5]
        #rectimgname=str(a)+"t2"+imgname
        #rectimgdir=imgdir+os.path.sep+rectimgname
        
        rectimgname=namethis()
        rectimgdir=curattachdirpc+os.path.sep+rectimgname
        
        cv2.imwrite(rectimgdir, img)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), -1)
        #rectcoord=int(x-5)+" "+int(y-5)+" "+int(x+w+5)+" "+int(y+h+5)+" "+rectimgname
        rectcoord=str(x-5)+" "+str(y-5)+" "+str(x+w+5)+" "+str(y+h+5)+" "+rectimgname
        ###appendtext(wledposdir,rectcoord,"a")
        rectcoord=(int(x-5),int(y-5),int(x+w+5),int(y+h+5),rectimgname)
        rectcoordlist.append(rectcoord)
            
    # write original image with added contours to disk
    cv2.imwrite(imgdir+os.path.sep+"contouredc2"+afterimg, image)
    #ocv1/3
    ##converttext(dir_path,"13.jpg",1000)
    #ocv2
    ##converttext(dir_path,"conv0003.jpg",1000)
    #rectcoordlist=[]
    rectcoordlist=sorted(rectcoordlist, key=itemgetter(1,0))
    return rectcoordlist

def converttext(imgdir,imgname,afterimg,a,ocvtype,colour,testing,wledposdir,rectcoordlist):
    large=cv2.imread(imgdir+os.path.sep+imgname)
    imgw,imgh=imgsize(imgdir+os.path.sep+imgname)
    timgh=0.10*imgw
    bimgh=0.90*imgw
    print(imgdir+os.path.sep+imgname+" "+str(imgw)+","+str(imgh))
    if ocvtype=="1" or ocvtype=="2" or ocvtype=="4" or ocvtype=="5":
        rgb=large
        #if imgw>imgh:
        #    rgb=cv2.pyrDown(large)
    if ocvtype=="3":
        rgb=cv2.pyrDown(large)
    if ocvtype=="21":
        rgb=cv2.pyrUp(large)
        rgb=cv2.pyrUp(rgb)
    rgb2=rgb.copy()
    small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    #cv2.imwrite(imgdir+os.path.sep+'grab1.png',connected)
    # using RETR_EXTERNAL instead of RETR_CCOMP
    _, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(bw.shape, dtype=np.uint8)
    #print(contours)
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        if ocvtype=="1" or ocvtype=="3" :
            if r > 0.45 and w > 100 and h > 10 and y>timgh and y<bimgh:
                a-=1
                ##img = rgb[y:y+h-1, x:x+w-1]
                img=rgb[y-5:y+h+5, x-5:x+w+5]
                rectimgname=str(a)+"t1"+imgname
                rectimgdir=imgdir+os.path.sep+rectimgname
                cv2.imwrite(rectimgdir, img)
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 255, 255), -1)
                
                #rectcoord=int(x-5)+" "+int(y-5)+" "+int(x+w+5)+" "+int(y+h+5)+" "+rectimgname
                rectcoord=str(x-5)+" "+str(y-5)+" "+str(x+w+5)+" "+str(y+h+5)+" "+rectimgname
                ###appendtext(wledposdir,rectcoord,"a")
                rectcoord=(int(x-5),int(y-5),int(x+w+5),int(y+h+5),rectimgname)
                rectcoordlist.append(rectcoord)
        elif ocvtype=="2" or ocvtype=="21":
            if r > 0.45 and w > 25 and h > 10:
                a-=1
                ##img = rgb[y+15:y+h-15, x+15:x+w-15]
                img=rgb[y:y+h, x:x+w]
                if ocvtype=="2":
                    cv2.imwrite(imgdir+os.path.sep+str(a)+"t1"+imgname, img)
                elif ocvtype=="21":
                    cv2.rectangle(rgb, (x-3, y-3), (x+w+3, y+h+3), (255, 255, 255), -1)
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 255, 255), -1)
                converttext(imgdir, str(a)+"t1"+imgname+".jpg","2"+afterimg+".jpg",a,4,"neutral",testing)
        elif ocvtype=="4":
            if r > 0.45 and w > 25 and h > 10:
                a-=1
                ##img = rgb[y:y+h-1, x:x+w-1]
                img=rgb[y-5:y+h+5, x-5:x+w+5]
                cv2.imwrite(imgdir+os.path.sep+str(a)+"t3"+imgname, img)
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 255, 255), -1)
        elif ocvtype=="5":
            if w > 25 and h > 10 and y>timgh and y<bimgh:
                a-=1
                ##img = rgb[y:y+h-1, x:x+w-1]
                img=rgb[y-5:y+h+5, x-5:x+w+5]
                cv2.imwrite(imgdir+os.path.sep+str(a)+"t3"+imgname, img)
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 255, 255), -1)

        if testing and y>timgh and y<bimgh:
            #img0=rgb[y-5:y+h+5, x-5:x+w+5]
            #cv2.imwrite(imgdir+os.path.sep+str(a)+"t0qc"+imgname, img0)
            #cv2.rectangle(rgb2, (x, y), (x+w, y+h), (255, 255, 255), -1)
            #print("testing")
            pass
    if ocvtype=="1" or ocvtype=="3":
        ##rgb = cv2.pyrUp(rgb)
        cv2.imwrite(imgdir+os.path.sep+afterimg, rgb)
        convertrest(imgdir,"contouredc"+imgname,afterimg,a,ocvtype,wledposdir,rectcoordlist)
        #converttext(imgdir,"contouredc"+imgname,"contouredc2"+afterimg,a,5,"neutral",testing)
    if ocvtype=="4":
        ##rgb = cv2.pyrUp(rgb)
        cv2.imwrite(imgdir+os.path.sep+afterimg, rgb)
        convertrest(imgdir,"contouredc"+imgname,afterimg,a,ocvtype,wledposdir,rectcoordlist)
    if ocvtype=="5":
        cv2.imwrite(imgdir+os.path.sep+afterimg, rgb)
#    cv2.imwrite(imgdir+os.path.sep+afterimg+".jpg", img)
    if testing:
        #cv2.imwrite(imgdir+os.path.sep+"mask"+afterimg, mask)
        #cv2.imwrite(imgdir+os.path.sep+"rect2"+afterimg, rgb2)
        print("testing")
        pass
    rectcoordlist=sorted(rectcoordlist, key=itemgetter(1,0))
    return rectcoordlist
def convertcolour(imgdir,imgname,afterimg,colour,size):
    a=1000
    idx=0
    # Convert BGR to HSV
    frame=cv2.imread(imgdir+os.path.sep+imgname)
    if size=="down":
        frame=cv2.pyrDown(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if colour=="red":
        lowerr = np.array([110,50,50])
        upperr = np.array([130,255,255])
        mask = cv2.inRange(hsv, lowerr, upperr)
    elif colour=="green":
        lowerg=np.array([33,80,40])
        upperg=np.array([102,255,255])
        mask = cv2.inRange(hsv, lowerg, upperg)
    elif colour=="blue":
        lowerb = np.array([110,50,50])
        upperb = np.array([130,255,255])
        mask = cv2.inRange(hsv,lowerb,upperb)
    #cv2.imwrite(imgdir+os.path.sep+'grabblue.png', mask)

    kernel = np.ones((5,5),'int')
    dilated = cv2.dilate(mask,kernel)
    ##cv2.imwrite(imgdir+os.path.sep+'grabblue1.png',dilated)
    #res = cv2.bitwise_and(frame,frame,mask=mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    ##cv2.imwrite(imgdir+os.path.sep+'grabblue2.png',connected)

    #_,thrshed = cv2.threshold(cv2.cvtColor(connected,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
    #_,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    _, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print(contours)
    for idx in range(len(contours)):
        a-=1
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        if r > 0.45 and w > 50 and h > 10:
            a-=1
            img=frame[y-5:y+h+5, x-5:x+w+5]
            #rectcoord=int(x-5)+" "+int(x+w+5)+" "+int(y-5)+" "+int(y+h+5)+" "+imgname
            rectcoord=[int(x-5),int(y-5),int(x+w+5),int(y+h+5),rectimgname]
            rectcoordlist.append(rectcoord)
            cv2.imwrite(imgdir+os.path.sep+str(a)+"t1blue"+imgname, img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), -1)
    cv2.imwrite(imgdir+os.path.sep+afterimg, frame)
    rectcoordlist=sorted(rectcoordlist, key=itemgetter(1,0))
    return rectcoordlist

def pushnewdir1toand(newdir1,curindexpc,curindexoldpc):
    curanddevice=checkadbdevices()
    #nulldevice="error: device '(null)' not found"
    deviceconnected="device"
    if deviceconnected in curanddevice:
        copydir(fnnotesdirpc+os.path.sep+newdir1,fnnotesdirand)
        appendnewnote(newdir1,curindexpc,curindexoldpc)
    return True

refprevycoordinate=""
exactcopycont=False
def runpdftonote(convpdfdirpc,pdfdir,pdfname,pagelst,ocvtype,continuenote,testing,multiplepage):
    global batchpdf, batchpdfstart, batchpdfend
    append=""
    print("startpdftonote")
    #column=1
    column=""
    pagestart=pagelst[0]
    pageend=pagelst[-1]
    batchpdf=True
    if noconversion:
        print("noconv")
        countpage=0
        #b=objno2
        if usethisnewdir1:
            CN=checknotz(usethisnewdir1)
            newdir1=CN[0]
            objno2=CN[1]
        else:
            delfile(convpdfdirpc)
            newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
        for i in pagelst :
            print("Page"+str(i))
            convpname,imgname=convertpdf2jpg2(pdfdir,pdfname,quality,i,convpdfdirpc,"")
            page=re.sub(r"(convp|.jpg)","",imgname)
            page=re.sub(r"(conv)","wledpos",imgname)
            wledposdir=re.sub(convpdfdirpcname,"",page)
            rectcoordlist=[(0,0,0,0,convpname+".jpg")]
            objno2,append=convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir,rectcoordlist,append)
            """
            if a==10 or i==(pageend-1):
                #convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir)
                objno2=convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir,rectcoordlist)
                a=0
                column+=1
            """
            print(imgname)
            countpage+=1
    if not noconversion:
        countpage=0
        if usethisnewdir1:
            CN=checknotz(usethisnewdir1)
            newdir1=CN[0]
            objno2=CN[1]
        else:
            delfile(convpdfdirpc)
            newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
        
        for i in pagelst:
            #if usethisnewdir1:
            #    exactcopycont=True
            if i==pagestart and not usethisnewdir1:
                column="exactcopy1"
            if i>pagestart or (i==pagestart and usethisnewdir1):
                with open(curnotefpc, 'rb') as f:
                    content = f.read()
                    cihx=str(binascii.hexlify(content).decode('utf-8'))
                    if i==pagestart and usethisnewdir1:
                        #cihx=cihx[-250:]
                        print("cihxps="+cihx)
                    if batchpdf and not (i==pagestart and usethisnewdir1):
                        cihx=append
                        cihx=append[-250:]
                        print("cihx="+cihx)
                        #time.sleep(3600)
                    
                    regexc1=re.compile(patternpicx)
                    print("findpatternpic1")
                    if regexc1.search(cihx):
                        print("findpatternpic2")
                        mox= re.search(patternpicx,cihx)
                        prevxcoordinate=mox.group(5)
                        prevycoordinate=mox.group(7)
                        prevdefyscale=mox.group(11)
                        prevendyscale=mox.group(13)
                        column="exactcopyrest;;"+prevycoordinate
                        if i==pagestart and usethisnewdir1:
                            global refprevycoordinate
                            refprevycoordinate=prevycoordinate
                            print("NNlasty="+refprevycoordinate)
                            #time.sleep(3600)
                    print(str(column))
                    #time.sleep(3600)
                #time.sleep(3600)
                pass
            #if i==pageend:
            #    batchpdfend=True
            delfile(convpdfdirpc)
            if multiplepage:
                if countpage>=multiplepage:
                    countpage=0
                    newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
                if multiplepage=="all":
                    pass
            if not multiplepage and i>pagestart:
                #newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
                pass
            #CN=checknotz(curnotelocpc)
            #newdir1=CN[0]
            #objno2=CN[1]
            
            a=1000
            ##i-=1
            convpname,imgname=convertpdf2jpg2(pdfdir,pdfname,quality,i,convpdfdirpc,"")
            #imgname=re.sub(r"(.pdf|.jpg|.png|.bmp.svg)","",imgname)
            #imgname=re.sub(convpdfdirpc,"",imgname)
            page=re.sub(r"(convp|.jpg)","",imgname)
            page=re.sub(r"(conv)","wledpos",imgname)
            wledposdir=re.sub(convpdfdirpcname,"",page)
            print(wledposdir)
            ###appendtext(wledposdir,"","w+")
            rectcoordlist=[]
            print(str(i)+" "+convpname,imgname)
            if testing:
                pdfconvimg=convpdfdirpc+os.path.sep+"contouredc"+convpname+".jpg"
                pdfdir0img=dir0+os.path.sep+"contouredc"+convpname+".jpg"
                #rectcoordlist=converttext(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg",1000,1,"neutral",testing,wledposdir,rectcoordlist)
                rectcoordlist=everyletter(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg",1000,ocvtype,withcolour,testing,wledposdir,rectcoordlist)
                a-=1
                column+=1
            if not testing:
                straight=True
                if not straight:
                    pdfconvimg=convpdfdirpc+os.path.sep+"contouredc"+convpname+".jpg"
                    pdfdir0img=dir0+os.path.sep+"contouredc"+convpname+".jpg"
                    #convertcolour(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg","green","down")
                    rectcoordlist=convertcolour(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg","green","",wledposdir,rectcoordlist)
                    subprocess.call("mv "+pdfconvimg+" "+pdfdir0img,shell=True)
                    objno2=convertjpg2note(convpdfdirpc,2,newdir1,1,wledposdir)

                    shutil.rmtree(convpdfdirpc)
                    checkdir(convpdfdirpc,"")
                    subprocess.call("mv "+pdfdir0img+" "+pdfconvimg,shell=True)
                    rectcoordlist=convertcolour(convpdfdirpc,"contouredc"+convpname+".jpg","contouredc"+convpname+".jpg","blue","",wledposdir,rectcoordlist)
                    subprocess.call("mv "+pdfconvimg+" "+pdfdir0img,shell=True)
                    objno2=convertjpg2note(convpdfdirpc,1,newdir1,objno2,wledposdir)

                    shutil.rmtree(convpdfdirpc)
                    checkdir(convpdfdirpc,"")
                    subprocess.call("mv "+pdfdir0img+" "+pdfconvimg,shell=True)
                    rectcoordlist=converttext(convpdfdirpc,"contouredc"+convpname+".jpg","contouredc"+convpname+".jpg",1000,ocvtype,"neutral","",wledposdir,rectcoordlist)
                    subprocess.call("mv "+pdfconvimg+" "+pdfdir0img,shell=True)
                    append,objno2=convertjpg2note(convpdfdirpc,2,newdir1,objno2,wledposdir)

                if straight:
                    #shutil.rmtree(convpdfdirpc)
                    #checkdir(convpdfdirpc,"")
                    #subprocess.call("mv "+pdfdir0img+" "+pdfconvimg,shell=True)
                    ##rectcoordlist=converttext(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg",1000,1,"neutral","",wledposdir,rectcoordlist)
                    rectcoordlist=everyletter(convpdfdirpc,convpname+".jpg","contouredc"+convpname+".jpg",1000,ocvtype,withcolour,testing,wledposdir,rectcoordlist)
                    #subprocess.call("mv "+pdfconvimg+" "+pdfdir0img,shell=True)
                    objno2,append=convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir,rectcoordlist,append)
                    #print("objno2="+str(objno2))
                    #print("page="+str(i))
                    #print("append="+append)
                    #time.sleep(3600)

                ###subprocess.call("cp "+convpdfdirpc+os.path.sep+convpname+".jpg "+pdfdir+os.path.sep+"attach/00.jpg",shell=True)
                ###subprocess.call("cp "+convpdfdirpc+os.path.sep+convpname+".jpg "+pdfdir+os.path.sep+"attach",shell=True)
                a-=1
            countpage+=1

        print("append="+append)
        print("noconv")
        countpage=0
        #b=objno2
        #delfile(convpdfdirpc)
        #newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
        
        for i in pagelst :
            print("Page"+str(i))
            #delfile(convpdfdirpc)
            #convpdfdirpc
            global curattachdirpc
            convpname,imgname=convertpdf2jpg2(pdfdir,pdfname,quality,i,curattachdirpc,"")
            page=re.sub(r"(convp|.jpg)","",imgname)
            page=re.sub(r"(conv)","wledpos",imgname)
            wledposdir=re.sub(convpdfdirpcname,"",page)
            
            rectcoordlist=[(0,0,0,0,convpname+".jpg")]
            #rectcoordlist=[(0,0,0,0,slideimgname)]
            if i==pagestart:
                column="slide1"
                print("rpvy="+refprevycoordinate)
                if refprevycoordinate:
                    column="slide1;;"+refprevycoordinate
            elif i>pagestart:
                column="slidenextline"
            if i==pageend:
                batchpdfend=True
            objno2,append=convertjpg2note(curattachdirpc,column,newdir1,objno2,wledposdir,rectcoordlist,append)
            """
            if a==10 or i==(pageend-1):
                #convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir)
                objno2=convertjpg2note(convpdfdirpc,column,newdir1,objno2,wledposdir,rectcoordlist)
                a=0
                column+=1
            """
            print(imgname)
            countpage+=1

        
    if args.pdfmdir :
        relevant_path=args.pdfmdir
        included_extensions = ['pdf']
        pdf_names = [fn for fn in os.listdir(relevant_path)
                      if any(fn.endswith(ext) for ext in included_extensions)]
        print(len(pdf_names))
        for i in range(0,len(pdf_names)):
            print(pdf_names[i])
            subprocess.call("python3 "+pdftonotedir+" -pdir \""+relevant_path+"\" -p \""+pdf_names[i]+"\" -d 100 -t 1 -nc 1" ,shell=True)
    return rectcoordlist,wledposdir

def runshowpdf(convpdfdirpc,pdfdir,pdfname,pagestart,pageend,ocvtype,continuenote):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    convpdfdirpc1=convpdfdirpc+os.path.sep+pdfname
    if not os.path.exists(convpdfdirpc1):
        os.makedirs(convpdfdirpc1)
    imgname=convertpdf2jpg2(pdfdir,pdfname,quality,pagestart,convpdfdirpc1)
    imgdir=convpdfdirpc+os.path.sep+pdfname+os.path.sep+imgname+".jpg"
    print(imgdir)
    img=mpimg.imread(imgdir)
    imgplot=plt.imshow(img)
    #countarea
    plt.show()
    image = PIL.Image.open(open(imgdir, 'rb'))
    #image.show()
    return True

#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#import tkinter as tk
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    if __name__ == "__main__":
        #rootimgv = tk.Tk()
        #aMainApplication(root).pack(side="top", fill="both", expand=True)
        #rootimgv.mainloop()
        pass
def prevpage(pdfdir,page):
    page+=1
    showpdf()
    return True
def nextpage(pdfdir,page):
    page+=1
    showpdf()
    return True
def detecttouch():
    return True
def progresswhitelist():
    return True
def whitelistarea(xpos,ypos,wimg,himg):
    return True
def progresspage():
    return True

def convertpdf2jpg(pdfdir,pdfname,quality,page,convpdfdirpc):
    ##for i in range(int(pagestart),int(pageend)):
    #ppmcommand2="convert -verbose -density "+str(quality)+" -trim "+pdfdir+os.path.sep+pdfname+"["+str(page)+"] -quality 100 -flatten -sharpen 0x1.0 "+convpdfdirpc+os.path.sep+convpname
    pdfpage=subprocess.getoutput("pdfinfo \""+pdfdir+os.path.sep+pdfname+"\" | grep Pages: | awk '{print $2}'")
    pagez=str(page).zfill(4)
    convpname="conv"+pagez
    ppmcommand="pdftoppm \""+pdfdir+os.path.sep+pdfname+"\" \""+convpdfdirpc+os.path.sep+convpname+"\" -jpeg -f "+str(page)+" -singlefile"
    #ppmcommand="pdftoppm \""+pdfdir+os.path.sep+pdfname+"\" \""+convpdfdirpc+os.path.sep+convpname+"\" -png -f "+str(page)+" -singlefile"
    print(ppmcommand)
    print(convpname)
    subprocess.call(ppmcommand,shell=True)
    imgdir=convpdfdirpc+os.path.sep+convpname+".jpg"
    while True:
        if os.path.exists(imgdir):
            print(imgdir)
            break
    return convpname
def getpdfinfo(pdfdir,pdfname,ver):
        if sys.platform in ['linux', 'linux2']:
                pdfinfocommand="pdfinfo"
                pdftoppmcommand="pdftoppm"
                pdfpage=subprocess.getoutput(pdfinfocommand+" \""+pdfdir+os.path.sep+pdfname+"\" | grep Pages: | awk '{print $2}'")
                pdfpage=int(pdfpage)
        if sys.platform in ['Windows', 'win32', 'cygwin']:
                userid=subprocess.getoutput("echo %USERNAME%")
                userhomedir=subprocess.getoutput("echo %USERPROFILE%")
                popplerver="poppler-0.51"
                popplerdir="C:\\Users\\"+userid+"\\Downloads\\"+popplerver+"_x86\\"+popplerver+"\\bin"
                pdfinfocommand=popplerdir+"\\pdfinfo.exe"
                pdftoppmcommand=popplerdir+"\\pdftoppm.exe"
                if ver=="wsl":
                        pdfdir0=conwindirtovwsldir(pdfdir)
                        convpdfdirpc0=conwindirtovwsldir(convpdfdirpc)
                        print("convertpdf2jpginwsl="+pdfdir)
                        ##pdfpage=subprocess.getoutput("wsl pdfinfo \""+pdfdir0+"/"+pdfname+"\" | grep Pages: | awk '{print $2}'")
                        #ppmcommand="wsl pdftoppm \""+pdfdir0+"/"+pdfname+"\" \""+convpdfdirpc0+"/"+convpname+"\" -jpeg -f "+str(page)+" -singlefile"
                        imgdir=convpdfdirpc+os.path.sep+convpname+".jpg"
                pdfpage0=subprocess.getoutput(pdfinfocommand+" \""+pdfdir+os.path.sep+pdfname+"\"")
                #print("pp0="+pdfpage0)
                #https://stackoverflow.com/questions/15422144/how-to-read-a-long-multiline-string-line-by-line-in-python
                for line in pdfpage0.splitlines():
                        #print(line)
                        #lineResult = libLAPFF.parseLine(line)
                        lineResult=line
                        pdfpage1=lineResult
                        #print("pp1="+pdfpage1)
                        if re.search(r"Pages:",str(line)):
                                pdfpage1=line
                                #print("pp1="+pdfpage1)
                                pdfpage2 = re.sub(r"(Pages:)([ ])*", '', pdfpage1)
                                #print("pp2="+pdfpage2)
                                pdfpage=int(pdfpage2)
        print("totalp="+str(pdfpage))
        return pdftoppmcommand,pdfpage
def convertpdf2jpg2(pdfdir,pdfname,quality,page,convpdfdirpc,ver):
        ##for i in range(int(pagestart),int(pageend)):
        #ppmcommand2="convert -verbose -density "+str(quality)+" -trim "+pdfdir+os.path.sep+pdfname+"["+str(page)+"] -quality 100 -flatten -sharpen 0x1.0 "+convpdfdirpc+os.path.sep+convpname
        ossep=os.path.sep
        if not os.path.exists(convpdfdirpc):
            os.makedirs(convpdfdirpc)
        pdftoppmcommand,pdfpage=getpdfinfo(pdfdir,pdfname,"")
        if page<0:
            page=1
        if page<=pdfpage:
            pagez=str(page).zfill(4)
        if page>pdfpage:
            pagez=str(pdfpage).zfill(4)
        #convpname="conv"+pagez
        convpname=namethis()
        convpname=re.sub(".jpg","",convpname)
        img0=convpdfdirpc+os.path.sep+convpname
        if noconversion:
            img0=curattachdirpc+os.path.sep+convpname
        imgdir=img0+".jpg"
        #imgdir=img0
        if not os.path.exists(imgdir):
            ppmcommand=pdftoppmcommand+" \""+pdfdir+os.path.sep+pdfname+"\" \""+img0+"\" -jpeg -f "+str(page)+" -singlefile"
            #ppmcommand=pdftoppmcommand+" \""+pdfdir+os.path.sep+pdfname+"\" \""+img0+"\" -png -f "+str(page)+" -singlefile"
            print(ppmcommand)
            subprocess.call(ppmcommand,shell=True)
            #time.sleep(5)
        while True:
            if os.path.exists(imgdir):
                print(imgdir)
                break
        return convpname,imgdir

def conwindirtovwsldir(windir):
    checkdir="C:\\\\Windows"
    wsldir=""
    #if os.path.exists(checkdir):
        #userid=subprocess.getoutput("awk -F: '!/root/ && /(\\/bin\\/bash)/ {print $1}' /etc/passwd")
        #userid=subprocess.getoutput("echo \\"%USERNAME%\\"")
    print("wd="+windir)
    wsldir=re.sub(r"C:","/mnt/c",windir)
    wsldir=re.sub(r"\\\\","/",wsldir)
    print("ad="+wsldir)
    return wsldir

def convertjpg2note(folderlocation,column,newdir1,objno2,wledposdir,rectcoordlist,append):
    global curattachdirpc, batchpdf, batchpdfstart,batchpdfend
    print("runengine")
    objno2re=objno2
    folderlocation=curattachdirpc
    allfnpicdir=os.listdir(folderlocation)
    copytowin=True
    copytoand=False
    wsl=False
    if copytowin and not copytoand and not wsl:
        copycommand="copy"
        copytohere=curattachdirpc
        pass
    if copytoand and not copytowin:
        copycommand="cp"
        copytohere=fnnotesdirandint
        pass
    #for i in range(0,len(allfnpicdir)):
    #if not column:
    #    column=1
    if fnnotesdirandint:
        attachfnanddir=fnnotesdirandint+"/"+newdir1+".notz"+"/"+"attach"
        print(attachfnanddir)
    """
    if len(rectcoordlist)==0:
        if objno2<=1:
            w, h=imgsize(picdirnew)
            appendnewpic(w,h,picname,newdir1,objno2re,"nearlatest;;firstcolumn;;firstline")
        else:
            appendnewpic(w,h,picname,newdir1,objno2re,"nearlatest;;firstcolumn;;nextline")
        return objno2re
    """
    for i in range(0,len(rectcoordlist)):
        ##Time=strftime("%Y%m%d%H%M%S")
        ##objno2rez=str(objno2re).zfill(6)
        ##picname=Time+'abcdefghi'+objno2rez+'.jpg'
        #objno2rez=str(objno2re).zfill(2)
        #lpicname=Time+'abcdefghijklm'+objno2rez+'.jpg'
        #print(picname)
        if rectcoordlist[i][4] in allfnpicdir:
            allfnpicdir.remove(rectcoordlist[i][4])
            pass
        picdir=folderlocation+ os.path.sep +  rectcoordlist[i][4]
        if noconversion:
            picdir=curattachdirpc+ os.path.sep +  rectcoordlist[i][4]
        if objno2re>=0 and os.path.getsize(picdir)>0:
            ###print(rectcoordlist[i][4])                    
            ##picdir=folderlocation+ os.path.sep +  allfnpicdir[i]
            picname=rectcoordlist[i][4]
            picdir=folderlocation+ os.path.sep +  rectcoordlist[i][4]
            picdirnew=folderlocation + os.path.sep + picname
            #if wledposdir:
                #textori=open(wledposdir)
                #with open(wledposdir,"r") as f:
                #    content=f.read()
                #    textedit=re.sub(allfnpicdir[i],picname,content)
                #    ###appendtext(wledposdir,textedit,"w+")
            print(picdir)
            if curanddevice:
                subprocess.call(copycommand+" \""+picdir+"\" \""+picdirnew+"\"", shell=True)
                os.remove(picdir)
                subprocess.call(copycommand+" \""+picdirnew+"\" \""+curattachdirpc+"\"", shell=True)
            w, h=imgsize(picdirnew)
            #appendnewpic(w,h,picname,newdir1,objno2re,"nearlatest")
            if noconversion:
                if objno2<=1:
                    columntype="slide1"
                if objno2>1:
                    columntype="slidenextline"
            else:
                if objno2<=1:
                    columntype="exactcopy1"
                if objno2>1:
                    columntype="exactcopyrest"
                
            if i==0 and "nearlatest" in columntype and not "slide" in str(type(column)):
                columntype="nearlatest;;firstcolumn;;nextline"
            elif i>0 and "nearlatest" in columntype and not "slide" in str(type(column)):
                prevx=int(rectcoordlist[i-1][0])
                prevy=int(rectcoordlist[i-1][1])
                curx=int(rectcoordlist[i][0])
                cury=int(rectcoordlist[i][1])
                if w>h:
                    prevcorrection=100
                elif h>w:
                    prevcorrection=30
                else:
                    prevcorrection=0
                
                if w>1000 or h>1000:
                    columntype="nearlatest;;nextcolumn;;sameline"
                    ###appendtext(wledposdir,"firstline","a")
                else:
                    if cury in range(prevy-prevcorrection,prevy+prevcorrection) and curx>prevx:
                        columntype="nearlatest;;nextcolumn;;sameline"
                        ###appendtext(wledposdir,"sameline","a")
                    elif not cury in range(prevy-prevcorrection,prevy+prevcorrection):
                        columntype="nearlatest;;firstcolumn;;nextline"
                        ###appendtext(wledposdir,"nextline","a")
                    else:
                        columntype="nearlatest;;firstcolumn;;nextline"
                        ###appendtext(wledposdir,"nextline","a")
            
            if "str" in str(type(column)):
                if "slide1" in column:
                    columntype="nearlatest;;"+column
                elif "slidenextline" in column:
                    columntype="nearlatest;;slidenextline"
                if "exactcopy" in column:
                    if objno2<=1:
                        columntype="exactcopy1"
                    else:
                        columntype=column
            if columntype:
                if not batchpdf:
                    _,_=appendnewpic(w,h,picname,newdir1,objno2re,columntype,rectcoordlist[i],append)
                if batchpdf:
                    _,_,append=appendnewpic(w,h,picname,newdir1,objno2re,columntype,rectcoordlist[i],append)
            if curanddevice:
                runadbcommand("adb push -p \""+picdirnew+"\" \""+attachfnanddir+"\"")
            objno2re+=1
        if curanddevice:
            runadbcommand("adb push \""+curnotefpc+"\" \""+curnotzand+"\"")
    ##print(str(len(allfnpicdir)))
    ##print(allfnpicdir)
    """
    for i in range(0,len(allfnpicdir)):
        Time=strftime("%Y%m%d%H%M%S")
        objno2rez=str(objno2re).zfill(6)
        picname=Time+'abcdefghi'+objno2rez+'.jpg'
        #objno2rez=str(objno2re).zfill(2)
        #picname=Time+'abcdefghijklm'+objno2rez+'.jpg'
        print(picname)
        picdir=folderlocation+ os.path.sep +  allfnpicdir[i]
        picdirnew=folderlocation + os.path.sep + picname
        subprocess.call(copycommand+" \\""+picdir+"\\" \\""+picdirnew+"\\"", shell=True)
        os.remove(picdir)
        subprocess.call(copycommand+" \\""+picdirnew+"\\" \\""+curattachdirpc+"\\"", shell=True)
        w, h=imgsize(picdirnew)
        #appendnewpic(w,h,picname,newdir1,objno2re,"nearlatest;;firstcolumn;;firstline")
        appendnewpic(w,h,picname,newdir1,objno2re,"nearlatest;;nextcolumn;;sameline")
        if attachfnanddir:
            runadbcommand("adb push -p \\""+picdirnew+"\\" \\""+attachfnanddir+"\\"")
        objno2re+=1
    """
    return objno2re,append

usethisnewdir1=""
def restartfn():
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            fiinotew10pcdir=userhomedir+"\\Documents\\Docs\\Automate\\FiiNoteWINE\\FiiNote.exe"
            subprocess.call("taskkill /F /IM FiiNote.exe /T",shell=True)
            subprocess.call("start /MAX \"fiinote\" \""+fiinotew10pcdir+"\"",shell=True)

#LOCATION
def ylochextoint2(sprevycoordinate,eprevycoordinate):
    #print(eprevycoordinate)
    sposypppsuffixint=int(sprevycoordinate[-12:-10],16)         
    sposyppsuffixint=int(sprevycoordinate[-10:-8],16)
    sposypsuffixint=int(sprevycoordinate[-8:-6],16)
    sposysuffixint=int(sprevycoordinate[-6:-4],16)
    sposyint=int(sprevycoordinate[-4:-2],16)
    sposyremint=int(sprevycoordinate[-2:],16)

    eposypppsuffixint=int(eprevycoordinate[-12:-10],16)         
    eposyppsuffixint=int(eprevycoordinate[-10:-8],16)
    eposypsuffixint=int(eprevycoordinate[-8:-6],16)
    eposysuffixint=int(eprevycoordinate[-6:-4],16)
    eposyint=int(eprevycoordinate[-4:-2],16)
    eposyremint=int(eprevycoordinate[-2:],16)
    county=0
    while True:
        if sprevycoordinate.lower()==eprevycoordinate.lower():
            break
        sposyremint+=1
        if sposyremint>191:
            sposyint+=1
            sposyremint=128
        if sposyint>191:
            sposysuffixint+=1
            sposyint=128
        if sposysuffixint>231:
            sposypsuffixint+=1
            sposysuffixint=225
        if sposypsuffixint>191:
            sposyppsuffixint+=1
            sposypsuffixint=128
        if sposyppsuffixint>191:
            sposypppsuffixint+=1
            sposyppsuffixint=128
        
        if sposyremint==eposyremint and sposyint==eposyint and sposysuffixint==eposysuffixint and sposypsuffixint==eposypsuffixint and sposyppsuffixint==eposyppsuffixint and sposypppsuffixint==eposypppsuffixint:
            break
        county+=1
    return county

def ylochextoint(sprevycoordinate,eprevycoordinate):
    county=int(eprevycoordinate,16)
    return county

def modnewylochex(oldyhex,county):
    posypppsuffixint=int(oldyhex[-12:-10],16)         
    posyppsuffixint=int(oldyhex[-10:-8],16)
    posypsuffixint=int(oldyhex[-8:-6],16)
    posysuffixint=int(oldyhex[-6:-4],16)
    posyint=int(oldyhex[-4:-2],16)
    posyremint=int(oldyhex[-2:],16)
    while county>0:
        posyremint+=1
        if posyremint>191:
            posyint+=1
            posyremint=128
        if posyint>191:
            posysuffixint+=1
            posyint=128
        if posysuffixint>231:
            posypsuffixint+=1
            posysuffixint=225
        if posypsuffixint>191:
            posyppsuffixint+=1
            posypsuffixint=128
        if posyppsuffixint>191:
            posypppsuffixint+=1
            posyppsuffixint=128
        county-=1
    posypppsuffixhex=format(posypppsuffixint, 'x')
    posyppsuffixhex=format(posyppsuffixint, 'x')
    posypsuffixhex=format(posypsuffixint, 'x')
    posysuffixhex=format(posysuffixint, 'x')           
    posyhex=format(posyint, 'x')
    posyremhex=format(posyremint, 'x')
    newylochex=posypppsuffixhex+posyppsuffixhex+posypsuffixhex+posysuffixhex+posyhex+posyremhex
    return newylochex
        

#SCALE
def xscalehextoint():
    pass
def yscalehextoint():
    pass
def xscaleinttohex():
    pass
def yscaleinttohex():
    pass

def addylocwscalehex(prevdefyscale,prevendyscale):
    ypresuffixint=int(prevdefyscale[0:2],16)
    ysuffixint=int(prevdefyscale[2:4],16)
    yscalequotint=int(prevdefyscale[4:6],16)
    yscaleremint=int(prevdefyscale[6:],16)
                        
    endypresuffixint=int(prevendyscale[0:2],16)
    endysuffixint=int(prevendyscale[2:4],16)
    endyscalequotint=int(prevendyscale[4:6],16)
    endyscaleremint=int(prevendyscale[6:],16)
    scaledh=0
    while True:
        yscaleremint+=1
        if yscaleremint>191:
            yscalequotint+=1
            yscaleremint=128
        if yscalequotint>191:
            ysuffixint+=1
            yscalequotint=128
        if ysuffixint>231:
            ypresuffixint+=1
            ysuffixint=225
        if ypresuffixint==endypresuffixint and ysuffixint==endysuffixint and yscalequotint==endyscalequotint and yscaleremint==endyscaleremint:
            break
        scaledh+=1
    countingy=scaledh+(64*3)
    return countingy
    pass

#FINDLASTY
"""
chemtbk
joinnotz
math
grokp3
"""
def lastycoordinate(cihx):
    print("Searching for lastycoordinate")
    #l = re.compile(patternpicgen).split(cihx)
    #m.start()
    #l=[m.group(15) for m in re.finditer(patternpicgen, cihx)]
    l=[m.group(7) for m in re.finditer(patternpicgen, cihx)]
    print(len(l))
    yloclst=[]
    countycount=0
    for r in l:
        #picname=bytearray.fromhex(r).decode()
        #print(picname)
        #xlochextoint()
        #yscalehextoint()
        ##print(r)
        countyloc=ylochextoint("E5A5A9E19E81",r)        
        yloclst.append((countyloc,r))
        countycount+=1
        #print(str(countycount)+"  "+str(countyloc))
    
    lastyhex=sorted(yloclst)
    #print(lastyhexlst)
    print(len(lastyhex))
    print("LATESTY="+lastyhex[-1][1])
    #time.sleep(3600)
    return str(lastyhex[-1][1])
    pass
def lastycoordinatelst(currentlasty,lastylst):
    lastylst=[]
    for hexs in lastylst:
        countyloc=ylochextoint(currentlasty,hexs) 
        lastylst.append((countyloc,hexs))
    lastyhex=sorted(yloclst)
    print("LATESTY="+lastyhex[-1][1])
    return str(lastyhex[-1][1])

def allindices(string, sub, listindex=[], offset=0):
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def updateobjno2(objno2,curnotefpc):
    with open(curnotefpc,"rb") as f:
            content=f.read()
            cihx=str(binascii.hexlify(content).decode('utf-8'))
            mo1=re.search(regexnote4,cihx)
            mo2=re.compile(regexnote4)
            #add by 1 twice is correct
            objno2+=1
            objno2+=1
            totalobjhex=""
            if objno2<127:
                totalobjhex=str(format(objno2,'x')).zfill(2)
            if objno2==127:
                totalobjhex="c280"
            if 127<objno2<2048:
                phexint=194+(objno2-128)//64
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((objno2-128)%64)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                totalobjhex=phexd+objno2hexd
            if objno2==2048:
                totalobjhex="e0a080"
            if objno2>2048:
                pphexint=224+((objno2-2048)//(64*(192-160)))
                phexint=160+((objno2-2048)//64)
                #objno2hexint=objno2-(phexint*64)
                objno2hexint=128+((objno2-2048)%64)
                pphexd=str(format(pphexint,'x')).zfill(2)
                phexd=str(format(phexint,'x')).zfill(2)
                objno2hexd=str(format(objno2hexint,'x')).zfill(2)
                totalobjhex=pphexd+phexd+objno2hexd
                pass
            print(mo1)
            #print(mo1.group(6))
            if str(mo1.group(6))=="None":
                ending=""
                repw=mo1.group(1)+totalobjhex+""
            else:
                ending=mo1.group(6)
                repw=mo1.group(1)+totalobjhex+ending
                
            replace1 = re.sub(mo1.group(1)+mo1.group(2), repw, cihx)
            print(mo1.group(1)+mo1.group(2))
            print(repw)
            #print(replace1)
            appendtext(curnotefpc,replace1,"wb")
    pass
def setvarconvpdf():
    global ocvtype,noconversion
    global newdir1, objno2, usethisnewdir1
    testing=False
    continuenote=False
    showpdf=False
    if args.combinenotz:
        cnlst=args.combinenotz.split(";;")
        if len(cnlst)>1:
            delfile(convpdfdirpc)
            newdir1,objno2=newnotz(fnnotesdirpc,fnnotesdirpc)
            newcurnotefpc=curnotefpc
            newcurattachdirpc=curattachdirpc
            notecount=0
            objno2=0
            objno2add=0
            for d in cnlst:
                if sys.platform in ['Windows', 'win32', 'cygwin']:
                    sep=os.path.sep+os.path.sep
                    dlst=d.split(sep)
                elif sys.platform in ['linux', 'linux2']:
                    dlst=d.split(os.path.sep)
                combnewdir1=dlst[-1]
                CN=checknotz(combnewdir1)
                newdir1=CN[0]
                objno2=CN[1]
                objno2add+=objno2
                combcurnotefpc=curnotefpc
                combcurattachdirpc=curattachdirpc
                print(newcurnotefpc,combcurnotefpc)
                copytree(combcurattachdirpc, newcurattachdirpc)
                #time.sleep(3600)
                with open(newcurnotefpc, 'rb') as text:
                    content = text.read()
                    newcihx=str(binascii.hexlify(content).decode('utf-8'))
                with open(combcurnotefpc, 'rb') as text:
                    content = text.read()
                    cihx=str(binascii.hexlify(content).decode('utf-8'))
                    if notecount==0:
                        print("Note1")
                        appendthis=cihx
                        appendtext(newcurnotefpc,appendthis,"wb")
                        print("ON1="+str(objno2add))
                    elif notecount>0:
                        print("Note2")
                        mo=re.search(beginningpart,cihx)
                        addthis=re.sub(mo.group(1),"",cihx)
                        cihx=addthis
                        print("ON2="+str(objno2add))
                        if notecount==1:
                            lastyhex=lastycoordinate(newcihx)
                        elif notecount>1:
                            lastyhex=lastycoordinatelst(currentlasty,lastylst)
                        print(lastyhex)
                        county=ylochextoint2("E5A5A9E19E81",lastyhex)
                        print(county)
                        #ylochex,scalesstart,scaleend
                        oldyhexlst=[ (m.group(0),m.group(7)) for m in re.finditer(patternpicgen, cihx)]
                        #oldyhexlst=[ (m) for m in re.finditer(patternpicgen, cihx)]
                        #oldyhexlst=[(m.group(7),m.group(12),m.group(13)) for m in re.finditer(patternpicgen, cihx)]
                        #oldyscalestart=[m.group(12) for m in re.finditer(patternpicgen, cihx)]
                        #oldyscaleend=[m.group(13) for m in re.finditer(patternpicgen, cihx)]
                        lastylst=[]
                        for hexs in oldyhexlst:
                            print(hexs)
                            ##oldyhex+lastyhex+(64*3)
                            oldyhex=hexs[1]
                            newyhex=modnewylochex(oldyhex,county+(64*3))
                            oldpic=hexs[0]
                            newpic=re.sub(oldyhex,newyhex,oldpic)
                            lastylst.append(newyhex)
                            print("Report="+"\n\n"+
                                  oldyhex+"\n\n"+
                                  newyhex+"\n\n"+
                                  oldpic+"\n\n"+
                                  newpic)
                            #time.sleep(3600)
                            cihx=re.sub(oldpic,newpic,cihx)
                        print(newcurnotefpc,combcurnotefpc)
                        #print(addthis)
                        appendthis+=cihx
                        #print(appendthis)
                        appendtext(newcurnotefpc,appendthis,"wb")
                        updateobjno2(objno2add,newcurnotefpc)
                        currentlasty=lastyhex
                    #time.sleep(3600)
                notecount+=1
        else:
            print("need more notz")
        return True
    
    if args.altcpdir:
        global convpdfdirpcname,convpdfdirpc,curnotelocpc
        convpdfdirpcname=args.altcpdir
        convpdfdirpc=dir0+os.path.sep+convpdfdirpcname
        curnotelocpc=fnnotesdirpc+os.path.sep+convpdfdirpcname+".txt"
    
    if args.notename:
        #CN=checknotz(args.notename)
        #newdir1=CN[0]
        #objno2=CN[1]
        usethisnewdir1=args.notename
            
    if args.testing:
        testing=True
    if args.continuenote :
        continuenote=True
    if args.pdfdir:
        pdfdir=args.pdfdir
    else:
        pdfdir=dir0
        #print("Slide=100")
        #print("Tbook=300")
        #print("Work=300/Adobe")
        
    if args.multiplepage:
        multiplepage=int(args.multiplepage)
    else:
        multiplepage=""
    
    if args.pdfname:
        checkdir(convpdfdirpc,"")
        #pdfname=args.pdfname
        #pfulldir=args.pdfname.split(os.path.sep)
        if "file:///" in args.pdfname:
            pdir=re.sub("file:///","",args.pdfname)
            pdir=re.sub("%20"," ",pdir)
            pdir=re.sub("/",os.path.sep+os.path.sep,pdir)
            print(pdir)
            """
            time.sleep(3600)
            pfulldir=args.pdfname.split(os.path.sep)
            pfulldir=pdir.split("/")
            pdir=os.path.sep.join(pfulldir)
            print(pdir)
            time.sleep(3600)
            """
            pfulldir=pdir.split(os.path.sep)
            print(pfulldir)
        else:
            pfulldir=args.pdfname.split(os.path.sep)
        if len(pfulldir)==1:
            pdfdir=dir0
            pdfname=pfulldir[0]
        else:
            pdfdir=os.path.sep.join(pfulldir[:-1:])
            pdfname=pfulldir[-1]
        print(pdfdir, pdfname)
        if os.path.exists(convpdfdirpc):
            shutil.rmtree(convpdfdirpc)
        
        if args.density :
            quality=int(args.density)
        """
        if args.pagestart :
            pagestart=int(args.pagestart)
        else:
            pagestart=1
        if args.pageend :
            pageend=int(args.pageend)
            pageend=pageend
        else:
            pdftoppmcommand,pdfpage=getpdfinfo(pdfdir,pdfname,"")
            #pdfpage=subprocess.getoutput("pdfinfo \\""+pdfdir+os.path.sep+pdfname+"\\" | grep Pages: | awk '{print $2}'")
            pageend=int(pdfpage)
        """
                
        if args.singlepage:
            pagestart=int(args.singlepage)
            pageend=int(args.singlepage)
        #if args.type.isdigit():
        #    ocvtype=int(args.type)
        ocvtype=str(args.type)
        
        if args.noconversion=="1":
            noconversion=True
        #print("PDFDir="+pdfdir+os.path.sep+pdfname+" Page="+str(pagestart)+" to "+str(pageend))
        #print("ocvt"+str(ocvtype))
        if args.showpdf:
            runshowpdf(convpdfdirpc,pdfdir,pdfname,pagestart,pageend,ocvtype,continuenote)
        if not args.showpdf:
            if not testing:
                testing=""
            if testing:
                continuenote=False
            if args.pagestart:
                pageslst=args.pagestart.split(";;")
                print(pageslst)
                for pages in pageslst:
                    if pages:
                        eachpages=pages.split("-")
                        addpages=args.pagestart.split("+")[1:]
                        try:
                            pagestart=int(eachpages[0])
                        except:
                            pagestart=1
                        try:
                            pageend=int(eachpages[1])
                        except:
                            pdftoppmcommand,pdfpage=getpdfinfo(pdfdir,pdfname,"")
                            #pdfpage=subprocess.getoutput("pdfinfo \\""+pdfdir+os.path.sep+pdfname+"\\" | grep Pages: | awk '{print $2}'")
                            pageend=int(pdfpage)
                        print(pages, eachpages)
                        if pages==pageslst[1]:
                            print(pagestart,pageend)
                            #time.sleep(3600)
                        #if not pagestart:
                        #    pagestart=0
                        #if not pageend:
                        #    pdftoppmcommand,pdfpage=getpdfinfo(pdfdir,pdfname,"")
                            #pdfpage=subprocess.getoutput("pdfinfo \\""+pdfdir+os.path.sep+pdfname+"\\" | grep Pages: | awk '{print $2}'")
                        #    pageend=int(pdfpage)
                        pagelst=list(range(pagestart,pageend+1))
                        for i in addpages:
                            pagelst.append(i)
                        rectcoordlist=""
                        rectcoordlist,wledposdir=runpdftonote(convpdfdirpc,pdfdir,pdfname,pagelst,ocvtype,continuenote,testing,multiplepage)
                    os.remove(curnotelocpc)
            if not args.pagestart and not args.singlepage:
                pagestart=1
                if not args.pageend:
                    pdftoppmcommand,pdfpage=getpdfinfo(pdfdir,pdfname,"")
                    #pdfpage=subprocess.getoutput("pdfinfo \\""+pdfdir+os.path.sep+pdfname+"\\" | grep Pages: | awk '{print $2}'")
                    pageend=int(pdfpage)
                pagelst=list(range(pagestart,pageend+1))
                rectcoordlist,wledposdir=runpdftonote(convpdfdirpc,pdfdir,pdfname,pagelst,ocvtype,continuenote,testing,multiplepage)
            if args.singlepage:
                pagestart=int(args.singlepage)
                pageend=int(args.singlepage)
                pagelst=list(range(pagestart,pageend+1))
                rectcoordlist,wledposdir=runpdftonote(convpdfdirpc,pdfdir,pdfname,pagelst,ocvtype,continuenote,testing,multiplepage)
        if rectcoordlist and os.path.exists(wledposdir):
            #print(rectcoordlist)
            for f in rectcoordlist:
                appendthis=""
                for i in range(0,len(f)):
                    appendthis=appendthis+str(f[i])+" "
                ###appendtext(wledposdir,str(appendthis),"a")
        os.remove(curnotelocpc)
        #restartfn()
    return True
args = parse_args()
setvarconvpdf()
#convertcolour(convpdfdirpc,".jpg","green")
#convertcolour("/home/user/Pictures","Screenshot from 2018-07-05 20-04-46.png","green")
