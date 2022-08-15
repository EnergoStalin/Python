#!/usr/bin/env python
#Writed by EnergoStalin aka AlexVip

import os, sys, tkinter
from tkinter import messagebox
from threading import Timer

#Settings
timerDelay = 2 #Sec
hostsPath = "C:\\Windows\\System32\\drivers\\etc\\hosts" #Path
ErrorCode = {1: "EACCESS", 2: "EDIR", 3: "ENOTFOUND", 4: "EEEEERRR"} #Exit codes

#Pre defining window
root = 0

#After time destroy callback with timer
def destroy():
    root.destroy()
timer = Timer(timerDelay,destroy)

#Key Handler
def keydown(e):
    if e.keycode == 13:
        root.destroy()

#Window Managment
root = tkinter.Tk()
root.bind("<KeyPress>",keydown)

#Creating text label
label = tkinter.Label(root,text="", font="Arial 24", justify=tkinter.LEFT)

#Some Styles
root.title("Notice")
root.overrideredirect(1)

#Strings to toggle
terms = [
    "144.217.254.156	osu.ppy.sh\n",
    "144.217.254.156	a.ppy.sh\n",
    "144.217.254.156	i.ppy.sh\n",
    "144.217.254.156	ce.ppy.sh\n",
    "144.217.254.156	c4.ppy.sh\n",
    "144.217.254.156	c5.ppy.sh\n",
    "144.217.254.156	c6.ppy.sh\n"
]

if("-kurikku" in sys.argv):
    terms = [
        "136.243.80.59 delta.ppy.sh\n",
        "136.243.80.59 osu.ppy.sh\n",
        "136.243.80.59 c.ppy.sh\n",
        "136.243.80.59 c1.ppy.sh\n",
        "136.243.80.59 c2.ppy.sh\n",
        "136.243.80.59 c3.ppy.sh\n",
        "136.243.80.59 c4.ppy.sh\n",
        "136.243.80.59 c5.ppy.sh\n",
        "136.243.80.59 c6.ppy.sh\n",
        "136.243.80.59 ce.ppy.sh\n",
        "136.243.80.59 a.ppy.sh\n",
        "136.243.80.59 s.ppy.sh\n",
        "136.243.80.59 i.ppy.sh\n",
        "136.243.80.59 bm6.ppy.sh\n",
    ]

#Networking off
# terms = [
# 	"127.0.0.1 osu.ppy.sh\n",
# 	"127.0.0.1 i.ppy.sh\n",
# 	"127.0.0.1 ce.ppy.sh\n"
# 	"127.0.0.1 c4.ppy.sh\n",
# 	"127.0.0.1 c5.ppy.sh\n",
# 	"127.0.0.1 c6.ppy.sh\n"
# ]

#Work with file
f = 0
try:
    f = open(hostsPath, "r+")
except FileNotFoundError:
    messagebox.showerror(title="It happens...",message="File or directory dont exists." + hostsPath)
    os._exit(ErrorCode["ENOTFOUND"])
except PermissionError:
    messagebox.showerror(title="Can not open file.",message="No access to file. Try change file permissions. " + hostsPath)
    os._exit(ErrorCode["EACCESS"])
except IsADirectoryError:
    messagebox.showerror(title="Hey!!!",message="This is directory you a fucking kidding me. " + hostsPath)
    os._exit(ErrorCode["EDIR"])
except Exception:
    messagebox.showerror(title="Nani!!!",message="Unhandled error please report to devoper.")
    os._exit(ErrorCode["EEEEERRR"])
    
#Reading whole file into list
lines = f.readlines()
new_content = ""

#Trincating content
f.seek(0)
f.truncate()    

#Toggle algorythm
block = False
akatsuki = False
for l in lines:
    for c in terms:
        if(l == c):
            block = True
            akatsuki = True
            break
        else:
            block = False
    if(not(block)):
            new_content += l

#Need off or on
if(not(akatsuki)):
    for i in terms:
        new_content += i
    #Some GUI code
    label.config(text="Akatsuki server on.")
    label.config(foreground="green")
else:
    label.config(text="Akatsuki server off.")
    label.config(foreground="red")
label.pack()

#Center window on screen
root.geometry("+{}+{}".format(
    int(root.winfo_screenwidth()/2 - label.winfo_reqwidth()/2),
    int(root.winfo_screenheight()/2 - root.winfo_reqheight()/2)
))

#Writing new content and closing descriptor
f.write(new_content)
f.close()

#Start message processing loop with destroy timer
timer.start()
root.mainloop()
timer.cancel()