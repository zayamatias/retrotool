import sys
import PIL.Image
import PIL.ImageTk
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter.filedialog import askopenfilename
import tkinter as tk
import retrofunctions
from functools import partial
import config


class App:
    # the main application ;-)
    def __init__(self):
        self.root = Tk()
        self.targetSystem = 0
        self.root.withdraw()
        self.paletteIndex = 0
        self.drawColor = 0 # Color selected in the palette
        self.pixels = []
        self.finalsprites = []
        self.usprites = []
        self.csprites = []
        self.spritexsize = config.spritexsize
        self.spriteysize = config.spriteysize
        self.opfile = ""
        self.palette=config.palettes[self.targetSystem][2]
        self.colors = []
        self.maxcolors = 16
        self.bgcolor = (7,7,7)
        self.root =Toplevel()
        self.root.title (config.tooltitle)
        self.root.geometry(str(config.appxsize)+"x"+str(config.appysize))
        self.root.iconbitmap(config.iconfile)
        self.img = PIL.Image.open (config.logoimage)
        self.spritephoto = PIL.ImageTk.PhotoImage(self.img)
        self.cv = Canvas(self.root)
        self.canvas_ref = self.cv.create_image(config.appxsize/2,config.appysize/2, image=self.spritephoto, anchor='center')
        self.cv.bind("<Button-1>", self.click)
        self.cv.pack(side='top', fill='both', expand='yes')
        self.scale = Scale(self.root, from_=1, to=20, orient=HORIZONTAL, length=800, command=lambda x:retrofunctions.zoomimage(self))
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=lambda:retrofunctions.openfile(self))
        self.filemenu.add_command(label="Save", command=lambda:retrofunctions.savefile(self))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu = Menu(self.menubar, tearoff=0)
        for system in config.systems:
            self.filemenu.add_checkbutton(label=system, onvalue=config.systems.index(system), offvalue=False, variable=self.targetSystem)
        self.menubar.add_cascade(label="Target System", menu=self.filemenu)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Show Sprites", command=lambda:retrofunctions.showsprites(self))
        self.filemenu.add_command(label="Sprite Editor", command=lambda:retrofunctions.spriteditor(self))
        self.menubar.add_cascade(label="Tools", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        

        # DefineSpriteListWindow
         

        if config.default_filename != "":
            retrofunctions.openfile(self)

       # Nothing gets executed after this statement!
        self.root.mainloop()

    def click (self,event):
        # need to consider scale!
        if self.spritephoto != "":
            zoom = self.scale.get() 
            width, height = self.img.size
            width = width * zoom
            height = height * zoom
            x = int(int(event.x - ((config.appxsize - width)/2))/zoom)
            y = int(int(event.y - ((config.appysize - height)/2))/zoom)
            if (x>0 and x<(width+1)) and (y>0 and y<(height+1)):
                color = self.img.getpixel ((x,y))
                r=int(int(color[0])/config.msxcolordivider)
                g=int(int(color[1])/config.msxcolordivider)
                b=int(int(color[2])/config.msxcolordivider)
                self.bgcolor = (r,g,b)
                retrofunctions.getColors(self)
                retrofunctions.getPixels(self)
                retrofunctions.createTempSprites(self)

    def exit(self):
        self.root.destroy()
        sys.exit()

    
            
if __name__ == "__main__":
    myapp = App()
    