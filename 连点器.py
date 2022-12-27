import pyautogui
import tkinter
import os
import sys
import threading
import keyboard
from tkinter import ttk,messagebox
messagebox.showwarning("使用提示","一旦本软件出现任何问题导致点击无法停止时,请将鼠标移至\n屏幕左上角\n程序将会触发错误并强行结束点击")
lock = threading.Lock()
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        #base_path = os.path.abspath(".")
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
mainScreen=tkinter.Tk()
mainScreen.iconbitmap(resource_path(os.path.join("logo.ico")))
mainScreen.title("连点器控制台")
mainScreenInFocus=True
def mainScreenFocusOut(event):
    global mainScreenInFocus
    # print("out")
    mainScreenInFocus=False
def mainScreenFocusIn(event):
    global mainScreenInFocus
    # print("in")
    mainScreenInFocus=True
mainScreen.bind('<FocusOut>',mainScreenFocusOut)
mainScreen.bind('<FocusIn>',mainScreenFocusIn)

leftClickVar=tkinter.IntVar()
doubleClickVar=tkinter.IntVar()
middleClickVar=tkinter.IntVar()
rightClickVar=tkinter.IntVar()

keyList={}
startKeyList={29,56,50}
onClick=False
isNewDown=True

def keyLoad(event):
    global startKeyList,keyList
    if event.event_type=="down" and event.name not in keyList:
        keyList[event.name]=event.scan_code
        focus=mainScreen.focus_get()
        if str(focus)==".!frame2.!entry"and mainScreenInFocus:
            keyShowName=""
            for i in keyList:
                keyShowName+=i+"+"
            startKeyList=set(keyList.values())
            keyChoice.config(state="normal")
            keyChoice.delete(0,tkinter.END)
            keyChoice.insert(0,keyShowName[:-1])
            keyChoice.config(state="readonly")
            
    if event.event_type=="up":
        try:
            del keyList[event.name]
        except:
            pass
    # print(keyList)

buttonChoiceBox=tkinter.Frame()
buttonChoiceBox.grid(row=0,column=0)
tkinter.Label(buttonChoiceBox,text="按键范围",fg="blue").grid(row=0,column=0,sticky="W")
ttk.Checkbutton(buttonChoiceBox,text="左键单击",variable=leftClickVar).grid(row=1,column=0,sticky="W")
ttk.Checkbutton(buttonChoiceBox,text="左键双击",variable=doubleClickVar).grid(row=2,column=0,sticky="W")
ttk.Checkbutton(buttonChoiceBox,text="中键",variable=middleClickVar).grid(row=3,column=0,sticky="W")
ttk.Checkbutton(buttonChoiceBox,text="右键",variable=rightClickVar).grid(row=4,column=0,sticky="W")

keyChoiceBox=tkinter.Frame()
keyChoiceBox.grid(row=1,column=0)
tkinter.Label(keyChoiceBox,text="按键绑定",fg="blue").grid(row=0,column=0,sticky="W")
keyChoice=ttk.Entry(keyChoiceBox)
keyChoice.insert(0,"ctrl+alt+m")
keyChoice.config(state="readonly")
keyChoice.grid(row=0,column=1,sticky="WE")
keyType=tkinter.ttk.Combobox(keyChoiceBox,width=11,font=('microsoft yahei', 10, 'bold'))
keyType["value"] = ("按下","开关")
keyType.config(state="readonly")
keyType.current(0)
keyType.grid(row=0,column=2,sticky="W")

keyboard.hook(lambda x: keyLoad(x))

def clickControl():
    global onClick,isNewDown
    while True:
        mainScreen.update()
        if set(keyList.values())==startKeyList and not mainScreenInFocus:
            if keyType.get()=="按下":
                onClick=True
                onClickShower.config(text="正在点击")
            else:
                if isNewDown:
                    onClick=not onClick
                    if onClick:
                        onClickShower.config(text="正在点击")
                    else:
                        onClickShower.config(text="没有点击")
                    isNewDown=False
        else:
            if keyType.get()=="按下":
                onClick=False
                onClickShower.config(text="没有点击")
            else:
                isNewDown=True
        if onClick:
            if mainScreenInFocus:
                continue
            try:
                if leftClickVar.get()==1:
                    pyautogui.click()
                if doubleClickVar.get()==1:
                    pyautogui.doubleClick()
                if middleClickVar.get()==1:
                    pyautogui.middleClick()
                if rightClickVar.get()==1:
                    pyautogui.rightClick()
            except:
                lock.acquire()
                messagebox.showerror("紧急中断","点击事件触发了错误，我们紧急中断了所有事件,你可以安全的操作鼠标并重启程序")
                os._exit()

class ClickControlT(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID = 0
        self.name = "点击控制"
        self.counter = 0
    def run(self):
        clickControl()
threadingNumber=0
def aboutShower():
    auboutScreen=tkinter.Tk()
    auboutScreen.iconbitmap(resource_path(os.path.join("logo.ico")))
    auboutScreen.title("关于")

    messageBox=tkinter.Frame(auboutScreen)
    messageBox.grid(row=0,column=0)

    createrTitle=tkinter.Label(messageBox,text="作者:")
    createrTitle.grid(row=0,column=0,sticky="W")
    creater=tkinter.Entry(messageBox)
    creater.insert(0,"宽宽")
    creater.config(state="readonly")
    creater.grid(row=0,column=1,sticky="W")

    createrQQTitle=tkinter.Label(messageBox,text="作者QQ:")
    createrQQTitle.grid(row=1,column=0,sticky="W")
    createrQQ=tkinter.Entry(messageBox,fg="blue")
    createrQQ.insert(0,"2163826131")
    def startAddQQ(event):
        os.system("start https://qm.qq.com/cgi-bin/qm/qr?k=7tPR4X-U1ZVL0nPvkrPEJDFZJK1pIF68&noverify=0")
    createrQQ.bind("<Button-1>", startAddQQ)
    createrQQ.config(state="readonly")
    createrQQ.grid(row=1,column=1,sticky="W")
    
    createrUrlTitle=tkinter.Label(messageBox,text="作者主页:")
    createrUrlTitle.grid(row=2,column=0,sticky="W")
    createrUrl=tkinter.Entry(messageBox,fg="blue")
    createrUrl.insert(0,"宽宽2007的小天地")
    def startURL(event):
        os.system("start https://kuankuan2007.gitee.io")
    createrUrl.bind("<Button-1>", startURL)
    createrUrl.config(state="readonly")
    createrUrl.grid(row=2,column=1,sticky="W")

    createrGiteeTitle=tkinter.Label(messageBox,text="作者Gitee:")
    createrGiteeTitle.grid(row=3,column=0,sticky="W")
    createrGitee=tkinter.Entry(messageBox,fg="blue")
    createrGitee.insert(0,"宽宽2007")
    def startGitee(event):
        os.system("start https://gitee.com/kuankuan2007")
    createrGitee.bind("<Button-1>", startGitee)
    createrGitee.config(state="readonly")
    createrGitee.grid(row=3,column=1,sticky="W")

    createrWeiXinPayTitle=tkinter.Label(messageBox,text="赞助作者")
    createrWeiXinPayTitle.grid(row=4,column=0,sticky="W")
    createrWeiXinPay=tkinter.Entry(messageBox,fg="blue")
    createrWeiXinPay.insert(0,"微信支付")
    def startWeiXinPayTitle(event):
        os.system("start https://kuankuan2007.gitee.io/WeiXinPay.png")
    createrWeiXinPay.bind("<Button-1>", startWeiXinPayTitle)
    createrWeiXinPay.config(state="readonly")
    createrWeiXinPay.grid(row=4,column=1,sticky="W")

    ttk.Label(auboutScreen,text="本产品用于日常自动化办公\n不得用于作弊、外挂\n最终解释权归作者所有").grid(row=1,column=0,sticky="W")

    auboutScreen.mainloop()
class AboutShowerT(threading.Thread):
    def __init__(self):
        global threadingNumber
        threading.Thread.__init__(self)
        self.threadID = threadingNumber
        self.name = "关于"
        self.counter = threadingNumber
        threadingNumber+=1
    def run(self):
        aboutShower()

def aboutBooter():
    aboutShowerT=AboutShowerT()
    aboutShowerT.daemon=True
    aboutShowerT.start()

onClickShower=tkinter.Label(mainScreen,text="没有点击",fg="red")
onClickShower.grid(row=2,column=0,sticky="W")

buttonBox=tkinter.Frame()
buttonBox.grid(row=3,column=0,sticky="E")
ttk.Button(buttonBox,text="关于",command=aboutBooter).grid(row=0,column=0,sticky="E")
clickControlT=ClickControlT()
clickControlT.daemon=True
clickControlT.start()

mainScreen.mainloop()