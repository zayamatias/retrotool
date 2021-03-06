import sys
import PIL.Image
import PIL.ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import retrofunctions
import config
import tiles
import sprites


class App:
    # the main application ;-)
    def __init__(self):

        self.root = tk.Tk()
        self.targetSystem = tk.IntVar(self.root)
        self.targetSystem.set(config.defaultSystem)
        self.palette=[]
        self.projfile =""
        # Objects to be saved/loaded to/from project file
        self.spixels = []
        self.tpixels = []
        self.finalsprites = []
        self.Tiles=[]
        self.ColorTiles = []
        self.FinalTiles = []
        self.usprites = []
        self.csprites = []
        self.spritescoords=[]
        self.oredcolors = ['3','5','6','7','9','11','12','13','15']
        self.imgwidth = 0
        self.imgheight = 0
        self.pixelsize = config.pixelsize
        self.spriteeditorbgcolor = config.spriteeditorbgcolor
        self.spritexsize = config.spritexsize
        self.spriteysize = config.spriteysize
        self.switchtiletag = ""
        #Use config or overriding tile size
        if config.syslimits[self.targetSystem.get()][5]==0:
            self.tilexsize = config.tilexsize
        else:
            self.tilexsize = config.syslimits[self.targetSystem.get()][5]

        if config.syslimits[self.targetSystem.get()][6]==0:
            self.tileysize = config.tileysize
        else:
            self.tileysize = config.syslimits[self.targetSystem.get()][6]

        self.newSprites = config.newSprites
        self.spritesPerRow = 0
        self.spritesPerCol = 0
        self.animWindow = ""
        self.animCanvas = ""
        self.sprImgOffset = 0
        self.tileImgOffset = 0
        self.TileMap = []
        self.swappedTuples = []
        self.spritesCanvas = None
        self.tilesCanvas = None
        self.paletteCanvas = None
        self.animArray  = config.animArray
        self.animCols = config.animCols
        self.animRows = config.animRows
        self.root.withdraw()
        self.paletteIndex = 1 # We cannot change the "0" colour, ever!
        self.drawColor = 0 # Color selected in the palette
        self.paletteColorBoxes = []
        self.opfile = ""
        self.colors = []
        self.maxcolors = config.syslimits[self.targetSystem.get()][2]
        self.bgcolor = (-1,-1,-1)
        self.root =tk.Toplevel()
        self.root.title (config.tooltitle)
        self.root.geometry(str(config.appxsize)+"x"+str(config.appysize))
        self.root.iconbitmap(config.iconfile)
        self.prcanvas = tk.Canvas(self.root)
        self.progress = ttk.Progressbar(self.prcanvas,orient=tk.HORIZONTAL,length=500,mode='determinate')
        self.progress.pack()
        self.img = PIL.Image.open (config.logoimage)
        self.spritephoto = PIL.ImageTk.PhotoImage(self.img)
        self.cv = tk.Canvas(self.root)
        self.canvas_ref = self.cv.create_image(config.appxsize/2,config.appysize/2, image=self.spritephoto, anchor='center')
        self.cv.bind("<Button-1>", self.click)
        self.cv.pack(side='top', fill='both', expand='yes')
        self.scale = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL, length=800, command=lambda x:retrofunctions.zoomimage(self))
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open Image", command=lambda:retrofunctions.openImageFile(self))
        self.filemenu.add_command(label="Open ROM", command=lambda:retrofunctions.openROMFile(self))
        self.filemenu.add_command(label="Open Project", command=lambda:retrofunctions.loadProject(self))
        self.filemenu.add_command(label="New Project", command=lambda:retrofunctions.newProject(self))
        self.filemenu.add_command(label="Preferences", command=lambda:retrofunctions.showPreferences(self))
        self.filemenu.add_command(label="Export asm", command=lambda:retrofunctions.exportASMFile(self))
        self.filemenu.add_command(label="Export to BASIC", command=lambda:retrofunctions.exportBASICFile(self))
        self.filemenu.add_command(label="Export to Tiled", command=lambda:retrofunctions.exportToTiled(self))
        self.filemenu.add_command(label="Export MSX screen", command=lambda:retrofunctions.exportMSXScreen(self))
        self.filemenu.add_command(label="Export NeoGeo Fixed Tiles (S ROM)", command=lambda:retrofunctions.exportNeoFixed(self))
        self.filemenu.add_command(label="Export NeoGeo Sprites (C ROM)", command=lambda:retrofunctions.exportNeoSprites(self))
        self.filemenu.add_command(label="Export to Binary/Raw", command=lambda:retrofunctions.exportBinary(self))
        self.filemenu.add_command(label="Save Project", command=lambda:retrofunctions.saveProject(self))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)


        idx = 0
        for system in config.systems:
            if idx in config.activeSystems:
                self.filemenu.add_radiobutton(label=system, value=idx, variable=self.targetSystem, state="normal",command=lambda menu=idx:self.updateTargetSystem(menu))
            else:
                self.filemenu.add_radiobutton(label=system, value=idx, variable=self.targetSystem, state="disabled")
            idx = idx + 1
        self.filemenu.invoke(config.defaultSystem)
        self.menubar.add_cascade(label="Target System", menu=self.filemenu)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Sprite Viewer/Editor", command=lambda:sprites.showSprites(self))
        self.filemenu.add_command(label="Tiles Viewer/Editor", command=lambda:tiles.showTiles(self))
        self.filemenu.add_command(label="View Tile Map", command=lambda:tiles.showTilesMap(self))
        self.filemenu.add_command(label="Animate", command=lambda:sprites.animate(self))
        self.menubar.add_cascade(label="Tools", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        # DefineSpriteListWindow
        self.spwindow = None
        self.tilwindow = None
        if config.default_filename != "":
            retrofunctions.openImageFile(self)
        # Nothing gets executed after this statement!
        self.root.mainloop()

    def updateTargetSystem(self,value):
        self.targetSystem.set(value)
        self.palette=config.palettes[value][2]
        #print (self.palette)
        #Use config or overriding tile size
        if config.syslimits[self.targetSystem.get()][5]==0:
            self.tilexsize = config.tilexsize
        else:
            self.tilexsize = config.syslimits[self.targetSystem.get()][5]

        if config.syslimits[self.targetSystem.get()][6]==0:
            self.tileysize = config.tileysize
        else:
            self.tileysize = config.syslimits[self.targetSystem.get()][6]
        self.pixelsize =32/self.tileysize

        self.maxcolors = config.syslimits[self.targetSystem.get()][2]

    def click (self,event):
        # need to consider scale!
        if hasattr(self.img,'filename'):
            if self.img.filename == config.logoimage :
                return 1 #do not allow BG selection on loading screen!
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
                    tk.messagebox.showinfo("Warning","Could not retrieve color properly, please chose another image or convert to another format")
                    return 1
                r=int(int(color[0])/config.palettes[self.targetSystem.get()][1][0])
                g=int(int(color[1])/config.palettes[self.targetSystem.get()][1][1])
                b=int(int(color[2])/config.palettes[self.targetSystem.get()][1][2])
                self.bgcolor = (r,g,b)
                retrofunctions.getColors(self)

    def exit(self):
        self.root.destroy()
        sys.exit()



if __name__ == "__main__":
    myapp = App()
