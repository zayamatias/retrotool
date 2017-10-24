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
import retroclasses


class App:
    # the main application ;-)
    def __init__(self):

        self.targetSystem = 0
        self.projfile =""
        # Objects to be saved/loaded to/from project file
        self.pixels = []
        self.finalsprites = []
        self.usprites = []
        self.csprites = []
        self.palette=config.palettes[self.targetSystem][2]
        self.imgwidth = 0
        self.imgheight = 0
        self.pixelsize = config.pixelsize
        self.spriteeditorbgcolor = config.spriteeditorbgcolor
        self.spritexsize = config.spritexsize
        self.spriteysize = config.spriteysize
        self.newSprites = config.newSprites
        self.spritesPerRow = 0
        self.spritesPerCol = 0
        self.animWindow = ""
        self.animCanvas = ""
        self.root = Tk()
        self.sprImgOffset = 0
        self.spritesCanvas = None
        self.paletteCanvas = None
        self.animArray  = config.animArray
        self.animCols = config.animCols
        self.animRows = config.animRows
        self.root.withdraw()
        self.paletteIndex = 1 # We cannot change the "0" colour, ever!
        self.drawColor = 0 # Color selected in the palette
        self.opfile = ""
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
        self.filemenu.add_command(label="Open Image", command=lambda:retrofunctions.openImageFile(self))
        self.filemenu.add_command(label="Open ROM", command=lambda:retrofunctions.openROMFile(self))
        self.filemenu.add_command(label="Open Project", command=lambda:retrofunctions.loadProject(self))
        self.filemenu.add_command(label="New Project", command=lambda:retrofunctions.newProject(self))
        self.filemenu.add_command(label="Preferences", command=lambda:retrofunctions.showPreferences(self))
        self.filemenu.add_command(label="Export asm", command=lambda:retrofunctions.exportASMFile(self))
        self.filemenu.add_command(label="Save Project", command=lambda:retrofunctions.saveProject(self))


        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu = Menu(self.menubar, tearoff=0)
        for system in config.systems:
            self.filemenu.add_checkbutton(label=system, onvalue=config.systems.index(system), offvalue=False, variable=self.targetSystem)
        self.menubar.add_cascade(label="Target System", menu=self.filemenu)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Sprite Editor", command=lambda:retrofunctions.showSprites(self))
        self.filemenu.add_command(label="Animate", command=lambda:retrofunctions.animate(self))
        self.menubar.add_cascade(label="Tools", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        

        # DefineSpriteListWindow
        self.spwindow = None

        if config.default_filename != "":
            retrofunctions.openImageFile(self)

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
                if isinstance(color,int):
                    messagebox.showinfo("Warning","Could not retrieve color properly, please chose another image or convert to another format")
                    return 1
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
    