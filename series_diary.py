import json, re, tkinter
from tkinter import *
from PIL import Image, ImageTk

ENTRIES = {}
LOCKED = {}
FILENAME = "series.json"

def loadSeriesData(filename):
    global ENTRIES
    json_data = {}
    if filename:
        with open(filename, 'r') as f:
            json_data = json.load(f)
    json_keys = list(json_data.keys())
    for i in range(len(json_data)):
        ENTRIES[i] = json_data[json_keys[i]]

def saveSeriesData(filename):
    global ENTRIES
    with open(filename, 'w') as f:
        json.dump(ENTRIES, f)

class Entry(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        global ENTRIES, LOCKED

        self.BUTTONS = []
        self.LABELS = []

        self.addColor = "green"
        self.substractColor = "red"
        self.lockColor = "gray"
        self.unlockColor = "yellow"

        img_0 = Image.open("lock.png")
        img_0 = img_0.resize((40, 40), Image.ANTIALIAS)
        self.lockImage = ImageTk.PhotoImage(img_0)

        img_1 = Image.open("unlock.png")
        img_1 = img_1.resize((40, 40), Image.ANTIALIAS)
        self.unlockImage = ImageTk.PhotoImage(img_1)

        for i in range(len(ENTRIES)):
            LOCKED[i] = True
            Label(self, text=ENTRIES[i]["title"]).grid(row=i, sticky=W)

            btnLock = Button(self, image=self.lockImage, bg=self.lockColor)
            btnLock.grid(row=i, column=1)
            btnLock.bind("<ButtonPress>", self.onClick)
            self.BUTTONS.append(btnLock)

            Label(self, text="S:").grid(row=i, column=2)
            seasonLabel = Label(self, text=ENTRIES[i]["season"])
            seasonLabel.grid(row=i, column=3, sticky=E)
            self.LABELS.append(seasonLabel)

            btnAddS = Button(self, text="+", bg=self.lockColor)
            btnAddS.grid(row=i, column=4)
            btnAddS.bind("<ButtonPress>", self.onClick)
            self.BUTTONS.append(btnAddS)

            btnSubS = Button(self, text="-", bg=self.lockColor)
            btnSubS.grid(row=i, column=5)
            btnSubS.bind("<ButtonPress>", self.onClick)
            self.BUTTONS.append(btnSubS)

            Label(self, text="E:").grid(row=i, column=6)
            episodeLabel = Label(self, text=ENTRIES[i]["episode"])
            episodeLabel.grid(row=i, column=7, sticky=E)
            self.LABELS.append(episodeLabel)

            btnAddE = Button(self, text="+", bg=self.lockColor)
            btnAddE.grid(row=i, column=8)
            btnAddE.bind("<ButtonPress>", self.onClick)
            self.BUTTONS.append(btnAddE)

            btnSubE = Button(self, text="-", bg=self.lockColor)
            btnSubE.grid(row=i, column=9)
            btnSubE.bind("<ButtonPress>", self.onClick)
            self.BUTTONS.append(btnSubE)

    def onClick(self, event):
        btnString = str(event.widget)
        try:
            num = int(re.search('(\d+)$', btnString).group(0))
        except:
            num = 1
        btn = num % 5
        entryNum = num // 5
        if btn == 0:
            entryNum -= 1
        if btn == 1:
            self.lockEntry(entryNum, num)
        elif not LOCKED[entryNum]:
            if btn == 2:
                self.addSeason(entryNum)
            elif btn == 3:
                self.subSeason(entryNum)
            elif btn == 4:
                self.addEpisode(entryNum)
            elif btn == 0:
                self.subEpisode(entryNum)

    def lockEntry(self, entry, btn):
        global LOCKED, FILENAME
        if LOCKED[entry]:
            LOCKED[entry] = False
            self.BUTTONS[btn - 1].config(bg=self.unlockColor, image=self.unlockImage)
            self.BUTTONS[btn].config(bg=self.addColor, fg="white")
            self.BUTTONS[btn + 1].config(bg=self.substractColor, fg="white")
            self.BUTTONS[btn + 2].config(bg=self.addColor, fg="white")
            self.BUTTONS[btn + 3].config(bg=self.substractColor, fg="white")
        else:
            LOCKED[entry] = True
            self.BUTTONS[btn - 1].config(bg=self.lockColor, image=self.lockImage)
            self.BUTTONS[btn].config(bg=self.lockColor, fg="black")
            self.BUTTONS[btn + 1].config(bg=self.lockColor, fg="black")
            self.BUTTONS[btn + 2].config(bg=self.lockColor, fg="black")
            self.BUTTONS[btn + 3].config(bg=self.lockColor, fg="black")
            saveSeriesData(FILENAME)

    def addSeason(self, entry):
        global ENTRIES
        ENTRIES[entry]["season"] += 1
        self.LABELS[entry * 2].config(text=ENTRIES[entry]["season"])

    def subSeason(self, entry):
        global ENTRIES
        ENTRIES[entry]["season"] -= 1
        self.LABELS[entry * 2].config(text=ENTRIES[entry]["season"])
    
    def addEpisode(self, entry):
        global ENTRIES
        ENTRIES[entry]["episode"] += 1
        self.LABELS[(entry * 2) + 1].config(text=ENTRIES[entry]["episode"])

    def subEpisode(self, entry):
        global ENTRIES
        ENTRIES[entry]["episode"] -= 1
        self.LABELS[(entry * 2) + 1].config(text=ENTRIES[entry]["episode"])

def setupTopFrame(master):
    topFrame = Frame(master)
    imgDiary = Image.open("diary.png")
    imgDiary = imgDiary.resize((200, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(imgDiary)
    topLabel = Label(topFrame, image=img)
    topLabel.image = img
    topLabel.pack()
    topFrame.pack(side=TOP)

if __name__ == "__main__":
    loadSeriesData(FILENAME)
    root = Tk()
    root.option_add('*font', ('verdana', 15, 'bold'))
    root.title("Series Diary")
    setupTopFrame(root)
    Entry(root).pack(side=TOP)
    root.mainloop()