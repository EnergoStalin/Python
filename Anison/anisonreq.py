#!/usr/bin/env python

import json, urllib.request, re, datetime, threading, math, os, webbrowser, datetime, platform

#Common variables
SettingsPath = "settings.json"
SavePath = "Music.sav"
m3upath = "anison.m3u"
SiteURL = 'http://anison.fm/'
req = SiteURL + "status.php?widget=false"
NowPlaying = ''
TimeToNext = 0
timer = 0
unique_programm_path = ""

#Threading
mutex = threading.Lock()

#Osu search settings
OsuMode = 0
OsuMapTag = "hl"

def save():
    global OsuMode, OsuMapTag, SavePath, m3upath,unique_programm_path
    file = open(SettingsPath,"w")
    file.write(json.dumps([OsuMode,OsuMapTag,SavePath,m3upath,unique_programm_path], indent=4))
    file.close()

def load():
    global OsuMode, OsuMapTag, SavePath,m3upath,unique_programm_path
    file = open(SettingsPath,"r")
    [OsuMode,OsuMapTag,SavePath,m3upath,unique_programm_path] = json.loads(file.read())
    file.close()

#HTML tag regex
TAG_RE = re.compile(r'<[^>]+>')

#Removing HTML tags
def remove_tags(text):
    return TAG_RE.sub('', text).replace('&#151;','-')

#Seconds to min:sec
def stomin(s):
    hours = math.floor(s / 3600)
    return (str(hours)+':' if hours >= 1 else '') + str(math.floor((s-(hours*3600)) / 60)).zfill(2) + ':' + str(s%60).zfill(2)

#Get last N lines in file
def lastN(n):
    mutex.acquire()
    file = open(SavePath)
    if(n > 0):
        ls = file.readlines()[-int(n):]
    else:
        ls = file.readlines()
    file.close()
    mutex.release()
    return ls


#Opening last N songs in browser
def OpenLastN(n):
    ls = lastN(n)
    for i in ls:
        print("\rOpening " + i[33:],end='')
        webbrowser.open("https://www.google.com/search?q="+urllib.parse.quote(i[33:].encode('utf8'),safe=''), new=2)

#Searching last N songs in osu
def OpenLastNOsu(n):
    ls = lastN(n)
    for i in ls:
        print("\rOpening " + i[33:],end='')
        webbrowser.open(
            "https://osu.ppy.sh/beatmapsets?m={}&q={}".format(
                OsuMode,
                urllib.parse.quote(
                    i[33:].encode('utf8'),safe=''
                ),
                OsuMapTag
            ) +
            (('&s={}').format(OsuMapTag) if OsuMapTag != "hl" else ''),
            new=2
        )

#Deletes N lines from end
def delflast(n):
    mutex.acquire()
    file = open(SavePath,"r")
    ls = file.readlines()[0:-int(n)]
    file.close()
    file = open(SavePath,"w")
    file.writelines(ls)
    file.close()
    mutex.release()

#Count of records
def count():
    mutex.acquire()
    file = open(SavePath,"r")
    ln = len(file.readlines())-1
    file.close()
    mutex.release()
    return ln

#Input proccessing
def pinput(s):
    global OsuMode, OsuMapTag, NowPlaying, SavePath,unique_programm_path
    error = "\rArgument must be an integer. And less than db size check it by using stat command."
    space = s.find(' ')
    if space == -1:
        if s == "last": #Searching playing track in google
            OpenLastN(1)
        elif s == "osu": #Searching playing track on osu! server
            OpenLastNOsu(1)
        elif s == "open": #Open log file
            os.startfile(SavePath)
        elif s == "save": #Save current session settings
            save()
            print("Current setting saved.")
        elif s == "next":
            print("Next in",stomin((TimeToNext-datetime.datetime.now()).seconds),"\nAt "+TimeToNext.strftime("%H:%M:%S"))
        elif s == "settings": #Open settings in editor
            os.startfile(SettingsPath)
        elif s == "listen": #Listen with m3u link
            os.startfile(m3upath)
        elif s == "site": #Go to radio site
            webbrowser.open(SiteURL, new=2)
        elif(s == "stat"):
            print("Tracks in database:", count())
        elif s == "restart":
            import sys
            print("Restarting.")
            timer.cancel()
            os.execv(sys.executable, ['python'] + sys.argv)
        elif s == "unique":
            import subprocess as sp
            if len(unique_programm_path) != 0:
                try:
                    sp.call([unique_programm_path,SavePath])
                except:
                    print("Error...\n")
            else:
                print("First set programm to unique data in save file.\nYou can do this by typing unique [Programm Path]")
        elif( s == "help"):
            print("Without args:")
            print("\trestart - restarting script\n")
            print("\tlast - opening last track in google search\n")
            print("\tosu - opening last track in osu search\n")
            print("\topen - opening save log file\n")
            print("\tsave - saving current settings in json\n")
            print("\tnext - time to next track\n")
            print("\tsettings - open json in external editor\n")
            print("\tlisten - open m3u radio link in external player\n")
            print("\tsite - go to anison site\n")
            print("\tstat - counting records in current db\n")
            print("\tunique - calling specified unique programm passing it in arguments path to save file\n")
            print("With args:")
            print("\tom [int] - changes default osu play mode in search request\n")
            print("\tomt [string] - changes default osu map tag(e.g. ranked, graveyard) in search request(hl - option for has leaderborded req default value)\n")
            print("\tsp [string] - changes save path also means change current db\n")
            print("\tunique [string] - set path to unique programm\n")
            print("\tDont Forget to save this\n")
            print("\tlast [int] - opens last N records in google search\n")
            print("\tosu [int] - opens last N records in osu search\n")
            print("\tlasti [int] - open i record from last in google search\n")
            print("\tosui [int] - open i record from last in osu search\n")
            print("\tclonedb [string] - clones current db file into specified file\n")
            print("\tshow [int] - print to console last N records\n")
            print("\tdelflast [int] - deletes last N records\n")
            print("\tstomin [int] - converts seconds to format %H:%M:%S simple mini game\n")
        else:
            print("\rUnknown command.")
    else:
        command = s[:space]
        args = s[space+1:]
        if(command == "om"): #Set osu playmode for this session
            try:
                OsuMode = int(args)
                print("\rOsu playmode set to {}.".format(OsuMode))
            except Exception:
                print("\rOsuMode must be integer.")
        elif(command == "omt"): #Set map tag fot THIS session
            OsuMapTag = args
            print("\rOsu map tag set to {}.".format(OsuMapTag))
        elif(command == "sp"): #Set log save path for this session
            SavePath = args
            print("\rSave path now is {}.".format(SavePath))
        elif (command == "unique"):
            unique_programm_path = args;
            print("Now unique programm is", unique_programm_path,"\n")
        elif(command == "last"):
            try:
                OpenLastN(int(args))
            except:
                print(error)
        elif(command == "clonedb"):
            try:
                f = open(args,"w")
                f.writelines(lastN(-1))
                f.close()
            except:
                print("\rError...")
        elif(command == "show"):
            try:
                for i in lastN(int(args) if args != "all" else -1):
                    print(i,end='')
            except:
                print(error)
        elif(command == "delflast"):
            delflast(int(args))
        elif(command == "osu"):
            try:
                OpenLastNOsu(int(args))
            except:
                print(error)
        elif(command == "osui"):
            try:
                webbrowser.open(
                    "https://osu.ppy.sh/beatmapsets?m={}&q={}".format(
                        OsuMode,
                        urllib.parse.quote(
                            lastN(int(args))[-int(args):-(int(args)-1)][0][33:].encode('utf8'),safe=''
                        ),
                        OsuMapTag
                    ) +
                    (('&s={}').format(OsuMapTag) if OsuMapTag != "hl" else ''),
                    new=2
                )
            except:
                print()
        elif(command == "lasti"):
            try:
                webbrowser.open("https://www.google.com/search?q="+urllib.parse.quote(lastN(int(args))[-int(args):-(int(args)-1)][0][33:].encode('utf8'),safe=''), new=2)
            except:
                print(error)
        elif(command == "stomin"):
            try:
                print(stomin(int(args)))
            except:
                print("\rInvalid args.")
        else:
            print("\rUnknown command.")

#Fetching anison data
def fetch():
    responce = urllib.request.urlopen(req)
    data = json.loads(responce.read())

    global NowPlaying
    NowPlaying = remove_tags(data["on_air"])
    str = datetime.datetime.now().strftime("[%d.%m.%Y] [%H:%M:%S] ")+NowPlaying

    global TimeToNext
    TimeToNext = datetime.datetime.now()+datetime.timedelta(seconds=data["duration"])

    #Print to console and file
    print('\r'+str,"\tNext track in",stomin(int(data["duration"])),"min.\n> ",end='')
    mutex.acquire()
    f = open(SavePath,"a+")
    f.write(str+'\n')
    f.close()
    mutex.release()

    #Starting timer
    global timer
    timer = threading.Timer(int(data["duration"]), fetch)
    timer.start()

if(platform.system() == "Windows"):
    import ctypes
    ctypes.windll.kernel32.SetThreadExecutionState(
                0x80000000 | \
                0x00000001)
    del ctypes

try:
    load()
except:
    save()

fetch()
#Main Loop
while True:
    print('\r> ', end='')
    s = str(input()).lower()
    if s == "exit":
        break
    else:
        pinput(s)

timer.cancel()