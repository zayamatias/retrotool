import sys
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter.filedialog import askopenfilename
import config
import tkinter as tk
import math

def findOrColor (csprites):
    # This function finds which is the best pixel to or according to the palette colors
    # This is used on MSX2 -> See https://www.msx.org/wiki/The_OR_Color
    numcols = len(csprites)
    
    if  numcols < 5:
        c=[-1,-1,-1]
        pc=[-1,-1,-1,False]
        # We need to split the sprite
        if numcols > 0:
            c[0]= int(csprites[0])
        if numcols > 1:
            c[1]= int(csprites[1])
        if numcols > 2:
            c[2]= int(csprites[2])
            pc[3] = True
        pc[0] = c[0]
        pc[1] = c[1]
        pc[2] = c[2]

        # find candidate for OR'ed color:
        if (c[0]|c[2]) == c[1]:
            pc[2] = c[1]
            pc[0] = c[0]
            pc[1] = c[2]
        if (c[1]|c[2]) == c[0]:
            pc[2] = c[0]
            pc[0] = c[1]
            pc[1] = c[2]
    return pc

def needToOr(csprites):
    #retruns if there is a need to or the colors or not
    toor = False;
    for cols in csprites:
        pc=findOrColor (cols)
        if pc[3]:
           toor = True
    return toor

def getSplits(csprites):
    #returns the number of sprites that have to be created as a result of the split
    splits = 0
    numcols = 0
    for cols in csprites:
        if numcols < len(cols):
                numcols = len(cols)
        if numcols > 0:
            splits = 1
        if numcols > 1:
            splits = 2
        if numcols > 2:
            splits = 2
    return splits


class sprite:
    # Sprite class, to make it easier to manipulate afterwards
    spriteCount = 0

    def __init__ (self,pattern,colors,ored):

        self.pattern=pattern   #binary pattern of the sprite
        self.colors=colors     #colors of the sprite
        self.ored = ored       #does this sprite come from an ored sprite (for palette purposes)
        self.number = sprite.spriteCount   #Sprite index
        sprite.spriteCount = sprite.spriteCount+1 #add one to the index for next sprite

    def displayPattern (self):
        #for testing purposes, show the pattern on console
        rows = self.pattern
        for row in rows:
            print (row)

    def displayColors (self):
        #for testing purposes, show the color on console
        rows = self.colors
        for row in rows:
            print (row)

    def getPattern (self):
        #retruns the pattern of a sprite
        line = ""
        rows = self.pattern
        for row in rows:
            line = line + str(row) + "\n"
        return line

    def getColors (self,ysize):
        #returns the colors of a sprite
        line = ""
        count = 1
        rows = self.colors
        for row in rows:
            line = line + str(row)
            if count < ysize :
                count = count + 1
                line = line + ","
        return line

    def getAsmPattern (self):
        #get the pattern of a sprite in ASM mode (db %xxxxxxxxxxxxxxxx)
        #attention: for 16bit sprites, msx splits into 2 8x16 patterns
        line = ""
        rows = self.pattern
        pat1 =""
        pat2 =""
        for row in rows:
            pat1=pat1+"\tdb %"+str(row)[:8]+"\n"
            pat2=pat2+"\tdb %"+str(row)[8:]+"\n"
        line = pat1 + pat2
        return line

    def getAsmColors (self,ysize):
        #get the colors of a sprite in ASM mode (db 1,2,3....) each byte represents the # of the color in the palette
        #for ored colors, bit #7 should be set, thus the +64
        line = "\tdb "
        rows = self.colors
        count = 1
        for row in rows:
            if self.ored :
                if (row!=0):
                   row = row + 64
            line = line + str(row)
            if count < ysize :
                count = count + 1
                line = line + ","
        line = line + "\n"
        return line

def openfile(app):
    #ask for a file to open
    app.cv.update()
    #to speed up testing, if a file is set in the config it will not ask to open but will open directly this one
    if config.default_filename == "":
        app.opfile = filedialog.askopenfilename(parent=app.root)
    else:
        app.opfile = config.default_filename
    app.cv.update()
    app.img = PIL.Image.open(app.opfile)
    #CHeck if the max number of colors accepted by the system is equal or more than the colors of the image
    colok = checkColors (app)
    sizeok = checkSize (app)
    if (not colok) or (not sizeok):
        return 1
    #create the image
    app.spritephoto=PIL.ImageTk.PhotoImage(app.img)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.scale.set(1)
    app.scale.pack()
    app.root.update()
    #to be used in the futrue for automatic adjustment of the palette
    swappedpalette = [(0,(0,0,0))]
    #positions that are vailable for swapping:
    # 1 or 2 = 3 etc....
    availableswaps =[3,5,7,9,11,13,15]
    #prepareOrs(app)


def zoomimage(app):
    #function called to zoom the image loaded in or out (according to the selected scale)
    zoom = app.scale.get()
    myimg = app.img.resize ((app.img.size[0]*zoom,app.img.size[1]*zoom))
    app.spritephoto=PIL.ImageTk.PhotoImage(myimg)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.root.update()

def checkColors(app):
    #check if the colors of the image are within the limits of the system
    app.colors = app.img.getcolors()
    numcolors = len(app.colors)
    if numcolors > 15:
        messagebox.showinfo("Error","Max number of colors exceeded ("+str(numcolors)+" instead of "+str(app.maxcolors)+")")
        return False
    else:
        return True

def checkSize(app):
    #check if the colors of the image are within the limits of the system
    width = app.img.size[0]
    if (width/config.spritexsize) != int (width/config.spritexsize):
        messagebox.showinfo("Error","Image width is not a multiple of sprite width ( currently set in config to "+str(config.spritexsize)+"px)")
        return False
    else:
        return True
def getColors(app):
    #get the system colors (needs to be generic, not yet done I believe)
    #app.palette =[app.bgcolor]
    for color in app.colors:
        rgb = color[1]
        r=int(int(rgb[0])/config.palettes[app.targetSystem][1])
        g=int(int(rgb[1])/config.palettes[app.targetSystem][1])
        b=int(int(rgb[2])/config.palettes[app.targetSystem][1])
        # make sure we do not add bgcolor
        if set((r,g,b)) != set (app.bgcolor):
           if not isColorInPalette (app,(r,g,b)):
               app.palette[app.paletteIndex]=(r,g,b)
        app.paletteIndex = app.paletteIndex + 1
    app.paletteIndex = 0

def getPixels (app):
    #Read all the pixels and colorsin the image
    #scan each pixel (Width) in each row (height)
    for y in range (0,app.img.size[1]):
        for x in range (0,app.img.size[0]):
            pixel = app.img.getpixel((x,y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            color = (int(r/config.palettes[app.targetSystem][1]),int(g/config.palettes[app.targetSystem][1]),int(b/config.palettes[app.targetSystem][1]))
            if set(color) != set(app.bgcolor): # color chosen by user
                #pattern is created either with a ZERO or the index of the color in the palette (1,2,3,4....max colors of the system)
                index = paletteIndex(app,color)
                if index >= 0:
                    app.pixels.append(index)
            else:
                app.pixels.append('0')
    
def paletteIndex(app,color):
    index = 0
    for palColor in app.palette:
        if (colorCompare(color,palColor)) and (index != 0):
            return index
        index = index + 1
    return -1

def createTempSprites (app):
    #Creates two arrays, uspritrs, which holds the pattern in colors (1,2,3....)
    #Csprites which holds the colors that are used in each line of the sprite
    txsprites = int(app.img.size[0]/app.spritexsize)
    tysprites = int(app.img.size[1]/app.spriteysize)
    for spy in range (0,tysprites):
        for spx in range (0,txsprites):
            thissprite = []
            thisspritecolors=[]
            for py in range (0,app.spriteysize):
                thiscolors = []   #Background is a must have as color
                srow ="" # Holds the scanned row of each sprite
                         # Since color can be more than 1, we need a color indicator
                for px in range (0,app.spritexsize):
                    position = ((spx*app.spritexsize)+px)+((app.spriteysize*app.img.size[0]*spy)+(py*app.img.size[0]))
                    if (position < len(app.pixels)):
                        color = str(app.pixels[position])
                    else:
                        color = "0"
                    if (color not in thiscolors) and (int(color) != 0):
                        thiscolors.append (color)
                    srow = srow + "%" + color
                thissprite.append(srow)
                thisspritecolors.append(thiscolors)
            app.usprites.append  (thissprite)
            app.csprites.append (thisspritecolors)


def createFinalSprites(app):
    #create the deifnitive sprite patterns (0,1), and splits sprites that need to be ored
    app.finalsprites=[]    
    myindex = 0
    for usprite in app.usprites:
        ored = False
        needtoor = needToOr(app.csprites[myindex])
        spritesplit = getSplits (app.csprites[myindex])
        for numsprites in range (0,spritesplit):
            tsprite =[]
            tcolor = []
            for y in range (0,app.spriteysize):
                pc=findOrColor(app.csprites[myindex][y])
                oc=pc[2]
                trow = "";
                row = usprite[y]
                for x in range (0,app.spritexsize):
                    pcolor = getTempColor (row,x)
                    if (int(pcolor)==int(pc[numsprites])) or (int(pcolor)==int(oc)):
                        trow = trow+"1"
                    else:
                        trow = trow+"0"
                tsprite.append(trow)
                if pc[numsprites]==-1:
                    tcolor.append (0)
                else:
                    tcolor.append (pc[numsprites])
            mysprite = sprite (tsprite,tcolor,ored)
            app.finalsprites.append(mysprite)
            if needtoor:
                ored = not ored
        myindex = myindex+1

def getTempColor (row,position):
    rowSplit = row.split ("%")
    rowSplit.pop (0)
    color = rowSplit[position]
    return color

def updateTempColor (row,position,color):
    
    rowSplit = row.split ("%")
    rowSplit.pop (0)
    rowSplit[position]=color
    returnRow = ""   
    for pixel in rowSplit:
        returnRow = returnRow + "%" + str(pixel)
    return returnRow
    
def writefile(app):
    #crete the aoutput .asm file with the sprite data, colors & palette
    
    createFinalSprites(app)
    app.outfile = app.opfile[:len(app.opfile)-3]+"asm"
    f = open(app.outfile, 'w')
    f.write ("SPRITE_DATA:\n")
    idx = 0
    for fsprite in app.finalsprites:
        line = fsprite.getAsmPattern()
        f.write (";Sprite"+str(idx)+"\n")
        f.write (line)
        idx = idx + 1
    f.write("SPRITE_COLORS:\n")
    idx = 0
    for fsprite in app.finalsprites:
        line = fsprite.getAsmColors(app.spriteysize)
        f.write (";Sprite"+str(idx)+"\n")
        f.write (line)
        idx = idx +1
    f.write ("PALETTE:\n")
    cindex =0;
    for color in app.palette:
        if set(color)==set((-1,-1,-1)):
            color = (0,0,0)
        f.write ("\tdb $"+str(hex(int(color[1]))[2:])+str(hex(int(color[2]))[2:])+",$"+str(color[0])+"\n")
        cindex = cindex+1
        # fill in dummy colors

    for dindex in range (cindex,16):
        f.write ("\tdb $77,$7\n")

def savefile(app):
    #do the actual saving of the file
    if app.usprites == []:
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    writefile(app)

def udpateTargetSystem(app,chgsystem):
    #Will be used when changing the target system
    print (app.targetSystem)
    print (chgsystem)
    app.targetSystem=config.systems.index(chgsystem)
    print (app.targetSystem)


def showsprites (app):
    #display the sprites grid, initializing everything first
    if app.usprites == []:
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    createSpritesWindow(app)
    app.spwindow.deiconify()
    numSprites = len(app.usprites)
    spritesPerRow = int(app.img.size[0]/config.spritexsize)
    if (app.img.size[0]!=0):
       spritesPerRow = int(math.ceil(app.img.size[0]/config.spritexsize))
    spriteColumns = int(math.ceil(numSprites/spritesPerRow))
    xsize = (app.spritexsize)*config.pixelsize
    ysize = (app.spriteysize)*config.pixelsize
    spacing = 4
    canvasWidth = spritesPerRow *(xsize+spacing)
    canvasHeight = spriteColumns*(ysize+spacing)
    shownSprites = 0
    spritesCanvas = Canvas (app.spwindow,width=canvasWidth,height=canvasHeight)
    # Mous click actions left-> Put pixel, Right-> Remove pixel
    spritesCanvas.bind('<Button-1>', lambda x:updatePixel(spritesCanvas,True,app))
    spritesCanvas.bind('<Button-3>', lambda x:updatePixel(spritesCanvas,False,app))
    spritesCanvas.pack()
    currX = 1
    currY = 1
    currentSprite = 0
    for row in range (0,numSprites):
        destX = currX + (xsize)
        destY = currY + (ysize)
        spritesCanvas.create_rectangle(currX,currY,destX,destY,width=(spacing/2),tags="spr"+str(currentSprite)+"canvas")
        #draw each "boxel" of the sprite
        drawboxel (app,spritesCanvas,app.usprites,currentSprite,currX,currY)
        currX = currX+(xsize+spacing)
        currentSprite = currentSprite + 1
        shownSprites = shownSprites + 1
        if shownSprites == spritesPerRow:
            currX = 1
            currY = currY + (ysize+spacing)
            shownSprites=0
    displayPalette(app)

def updatePixel (canvas,switchon,app):
    fill = config.spriteeditorbgcolor
    pixelcolor = 0
    tags = canvas.gettags(CURRENT)
    if len(tags)<2:
        return
    if switchon:
      fill = transformColor(app,app.drawColor)
      pixelcolor = 1
    if canvas.find_withtag(CURRENT):
      canvas.itemconfig(CURRENT, fill=fill)
      coords = tags[0].split('/')
      spriteidx = int(coords[0])
      px = int(coords[1])
      py = int(coords[2])
      sprite = app.usprites[spriteidx]
      row = sprite[py]
      row = updateTempColor (row,px,app.drawColor)
      map(str,row)
      row = ''.join(row)
      sprite[py]=row
      app.usprites[spriteidx]=sprite
      canvas.update_idletasks()

def updateDrawColor (canvas,app):
    tags = canvas.gettags(CURRENT)
    for rectangle in canvas.find_all():
       compare = canvas.itemcget(rectangle,"tags")
       if "current" not in compare :
            canvas.itemconfig (rectangle, outline="black")
       else:
            canvas.itemconfig (rectangle, outline="white")
    canvas.update_idletasks()
    if len(tags)<1:
        return
    app.drawColor = int(tags[0])-1

      
def drawboxel (app,canvas,sprites,index,x,y):
    startx = x
    sprite = sprites[index]
    py=0
    for row in sprite:
        px=0
        ey = y + config.pixelsize
        for pixel in range (0,app.spritexsize):
            ex = x + config.pixelsize
            pxColor = int(getTempColor(row,pixel))
            if pxColor != 0:
                color = transformColor (app,pxColor)
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
                canvas.create_rectangle (x,y,ex,ey,fill=color,tag=str(index)+"/"+str(px)+"/"+str(py))
            else:
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
                canvas.create_rectangle (x,y,ex,ey,fill=config.spriteeditorbgcolor,tag=str(index)+"/"+str(px)+"/"+str(py))

            px = px + 1
            x = ex
        x = startx
        y=ey
        py = py + 1

def transformColor (app,paletteIndex):
    palettecolor = app.palette[paletteIndex]
    r = palettecolor[0]
    g = palettecolor[1]
    b = palettecolor[2]
    if r<0: r = 0        
    if g<0: g = 0        
    if b<0: b = 0        
    rgb = (r*config.msxcolordivider,
           g*config.msxcolordivider,
           b*config.msxcolordivider)
    color = "#%02x%02x%02x" % rgb
    return color

def createSpritesWindow(app):
    #window to show the sprites in
    app.spwindow =  tk.Toplevel(app.root)
    app.spwindow.title("Sprite List")
    app.spwindow.iconbitmap(config.iconfile)
    app.spwindow.geometry(str(config.appxsize)+"x"+str(config.appysize))
    app.spwindow.protocol("WM_DELETE_WINDOW", lambda:closeSpritesWindow(app))
    app.spwindow.withdraw()
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')

def createPaletteWindow(app,ysize):
    #window to show the sprites in
    app.palwindow =  tk.Toplevel(app.spwindow)
    app.palwindow.title("ColorPalette")
    app.palwindow.iconbitmap(config.iconfile)
    app.palwindow.geometry(str(config.paletteWxSize)+"x"+str(ysize))
    app.palwindow.protocol("WM_DELETE_WINDOW", lambda:closePaletteWindow(app))
    app.palwindow.withdraw()
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')

def closeSpritesWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.spwindow.destroy()

def closePaletteWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.palwindow.destroy()

def isColorInPalette(app,color):
    
    iscolorinpalette = False
    for palColor in app.palette:
        if colorCompare (color,palColor):
            iscolorinpalette = True
    return iscolorinpalette
    
    
def displayPalette(app):
    
    numColors= len(app.palette)
    maxColorsPerRow = int(math.ceil(config.paletteWxSize/config.paletteColorBoxSize))
    numRows = int (math.ceil(numColors/maxColorsPerRow))
    paletteWySize = numRows*config.paletteColorBoxSize
    createPaletteWindow (app,paletteWySize)
    paletteCanvas = Canvas (app.palwindow,width=config.paletteWxSize,height=paletteWySize)
    paletteCanvas.bind('<Button-1>', lambda x:updateDrawColor(paletteCanvas,app))
    x=1
    y=1
    color = 0
    for c in range (1,numColors-1):
        for col in range (0,maxColorsPerRow):
            if color<numColors:
                boxColor = transformColor(app,color)
                color = color + 1
                dx = x+config.paletteColorBoxSize
                dy = y+config.paletteColorBoxSize
                paletteCanvas.create_rectangle (x,y,dx,dy,fill=boxColor,tag=str(color))
                x = x + config.paletteColorBoxSize
        x = 1
        y = y + config.paletteColorBoxSize
    paletteCanvas.pack()
    app.palwindow.deiconify()
    
def colorCompare(colora,colorb):
    ra=int(colora[0])
    ga=int(colora[1])
    ba=int(colora[2])
    rb=int(colorb[0])
    gb=int(colorb[1])
    bb=int(colorb[2])
    if (ra==rb) and (ga==gb) and (ba==bb):
        return True
    if (abs(ra-rb)==1) and (ga==gb) and (ba==bb):
        return True
    if (ra==rb) and (abs(ga-gb)==1) and (ba==bb):
        return True
    if (ra==rb) and (abs(ba-bb)==1) and (ga==gb):
        return True
    return False
    
    