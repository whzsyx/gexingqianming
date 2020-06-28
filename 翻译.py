# http://www.youdao.com/w/查询词
import requests
# import urllib.request
import time
from bs4 import BeautifulSoup
from tkinter import *
import tkinter
root = tkinter.Tk()

try:
    root.iconbitmap('tr.ico')
except:
    print("请在当前目录下放入tr.ico以显示图标")

root.title('在线翻译')

base_url = 'http://www.youdao.com/w/'


def send(event=None):
    word = inputEntry.get()
    url = base_url + word
    print(url)
    html = ''

    success = False
    failCount = 0
    while (not success and failCount < 10):
        try:
            r = requests.get(url)
            # print(r.status_code)    # 获取返回状态
            html = r.text
            '''
            r = urllib.request.urlopen(url)
            html = r.read()
            r.close()
            '''
            success = True
        except:
            print("请求异常,重试中.")
            success = False
            failCount += 1
            time.sleep(0.2)

    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("div", {"class": "trans-container"})
    x = str(result)
   # print(x)

    soup = BeautifulSoup(x, 'html.parser')
    # EN to CH
    transList = list(map(lambda x: x.getText(), soup.findAll("li")))

    # CH to EN
    if (len(transList) == 0):
        transList = list(map(lambda x: x.getText(), soup.findAll("p")))
        if transList[-1] == "论文要发表？专家帮你译！":  # 删除广告
            del transList[-1]

    v.set(transList)
    listBox.pack(fill="x")
    global hidden
    hidden = False
    htext.set("^")


def hideListBox():
    global hidden
    if (hidden):
        listBox.pack(fill="x")
        hidden = False
        htext.set("^")
        #print(hidden)
    else:
        listBox.forget()
        hidden = True
        htext.set("v")
        #print(hidden)


upperFrame = Frame(root)
inputEntry = Entry(upperFrame, width=50,font=("DFKai-SB", 12))
inputEntry.bind('<Return>', send)
sendButton = Button(upperFrame, text="翻译", command=send)
htext = StringVar()
htext.set("v")
hideButton = Button(upperFrame, textvariable=htext, command=hideListBox, width=3)
hidden = True

v = StringVar()
listBox = Listbox(root, listvariable=v, height=6)
inputEntry.pack(side="left", anchor="w", fill="x", padx="2")
hideButton.pack(side="right", anchor="ne", padx='2')
sendButton.pack(side="right", anchor="ne")

upperFrame.pack(fill="x")
root.mainloop()

