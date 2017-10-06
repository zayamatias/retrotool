# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:07:29 2017

@author: id087082
"""
import sys
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter.filedialog import askopenfilename
import config
import tkinter as tk

def showSprites (sprites):
    count = len(sprites)
    sprimg = PIL.Image.new()

def findOrColor (csprites):
    numcols = len(csprites)
    if  numcols < 5:
        c=[255,255,255]
        pc=[255,255,255,False]
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
    toor = False;
    for cols in csprites:
        pc=findOrColor (cols)
        if pc[3]:
           toor = True
    return toor

def getSplits(csprites):
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
    spriteCount = 0

    def __init__ (self,pattern,colors,ored):

        self.pattern=pattern
        self.colors=colors
        self.ored = ored
        self.number = sprite.spriteCount
        sprite.spriteCount = sprite.spriteCount+1

    def displayPattern (self):
        rows = self.pattern
        for row in rows:
            print (row)

    def displayColors (self):
        rows = self.colors
        for row in rows:
            print (row)

    def getPattern (self):
        line = ""
        rows = self.pattern
        for row in rows:
            line = line + str(row) + "\n"
        return line

    def getColors (self,ysize):
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
    app.cv.update()
    if config.default_filename == "":
        app.opfile = filedialog.askopenfilename(parent=app.root)
    else:
        app.opfile = config.default_filename
    app.cv.update()
    app.img = PIL.Image.open(app.opfile)
    colok = checkColors (app)
    if not colok:
        return 1

    app.spritephoto=PIL.ImageTk.PhotoImage(app.img)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.scale.set(1)
    app.scale.pack()
    app.root.update()
    # default size for sprites
    #Usprites y Csprites OK
    #Primer color es el transparente (o negro)
    swappedpalette = [(0,(0,0,0))]
    # Despues tengo que ver los posibles swap 3,5,7,9,11,13,y 15
    availableswaps =[3,5,7,9,11,13,15]
    #prepareOrs(app)


def zoomimage(app):
    zoom = app.scale.get()
    myimg = app.img.resize ((app.img.size[0]*zoom,app.img.size[1]*zoom))
    app.spritephoto=PIL.ImageTk.PhotoImage(myimg)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.root.update()

def checkColors(app):
    app.colors = app.img.getcolors()
    numcolors = len(app.colors)
    if numcolors > 15:
        messagebox.showinfo("Error","Max number of colors exceeded ("+str(numcolors)+" instead of "+str(app.maxcolors)+")")
        return False
    else:
        return True 
def getColors(app):
    app.palette =[app.bgcolor]
    for color in app.colors:
        rgb = color[1]
        r=int(int(rgb[0])/config.palettes[app.targetSystem][1])
        g=int(int(rgb[1])/config.palettes[app.targetSystem][1])
        b=int(int(rgb[2])/config.palettes[app.targetSystem][1])
        # make sure we do not add bgcolor
        if set((r,g,b)) != set (app.bgcolor):
           app.palette.append((r,g,b))

def getPixels (app) :   
    #Read all the pixels and colors
    for y in range (0,app.img.size[1]):
        for x in range (0,app.img.size[0]):
            pixel = app.img.getpixel((x,y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            color = (int(r/config.palettes[app.targetSystem][1]),int(g/config.palettes[app.targetSystem][1]),int(b/config.palettes[app.targetSystem][1]))
            if set(color) != set(app.bgcolor): # color chosen by user
                app.pixels.append(app.palette.index(color))
            else:
                app.pixels.append('0')
    # Number of pixels check ok


def createTempSprites (app):
    txsprites = int(app.img.size[0]/app.spritexsize)
    tysprites = int(app.img.size[1]/app.spriteysize)
    print (txsprites,tysprites)
    for spy in range (0,tysprites):
        for spx in range (0,txsprites):
            thissprite = []
            thisspritecolors=[]
            for py in range (0,app.spriteysize):
                thiscolors = []   #Background is a must have as color
                srow ="" # Holds the scanned row of each sprite
                for px in range (0,app.spritexsize):
                    position = ((spx*app.spritexsize)+px)+((app.spriteysize*app.img.size[0]*spy)+(py*app.img.size[0]))
                    color = str(app.pixels[position])
                    if (color not in thiscolors) and (int(color) != 0):
                        thiscolors.append (color)
                    srow = srow + color
                thissprite.append(srow)
                thisspritecolors.append(thiscolors)
            app.usprites.append  (thissprite)
            app.csprites.append (thisspritecolors)
    print (len(app.usprites))

"""
def prepareOrs (app):

    for csprite in app.csprites:
        for row in csprite:
            if ((len(row)>3)):
                #we need a swap candidate
                c=[]
                for col in row:
                    if int(col) != 0:
                        c.append(int(col))
                #find if there is already an or candidate
                if (c[0]|c[1]==c[2]) or (c[0]|c[2]==c[1]) or (c[2]|c[1]==c[0]):
 """

def createFinalSprites(app):
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
                    pcolor = int(row[x])
                    if (pcolor==pc[numsprites]) or (pcolor==oc):
                        trow = trow+"1"
                    else:
                        trow = trow+"0"
                tsprite.append(trow)
                if pc[numsprites]==255:
                    tcolor.append (0)
                else:
                    tcolor.append (pc[numsprites])
            mysprite = sprite (tsprite,tcolor,ored)
            app.finalsprites.append(mysprite)
            if needtoor:
                ored = not ored
        myindex = myindex+1

def writefile(app):
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
        f.write ("\tdb $"+str(hex(int(color[1]))[2:])+str(hex(int(color[2]))[2:])+",$"+str(color[0])+"\n")
        cindex = cindex+1
        # fill in dummy colors

    for dindex in range (cindex,16):
        f.write ("\tdb $77,$7\n")

def savefile(app):
    
        #bgcolor should be the first in the list

    writefile(app)

def udpateTargetSystem(app,chgsystem):
    print (app.targetSystem)
    print (chgsystem)
    app.targetSystem=config.systems.index(chgsystem)
    print (app.targetSystem)
    

def showsprites (app):
    
    getColors(app)
    getPixels(app)
    createTempSprites(app)
    createFinalSprites(app)
    createSpritesWindow(app)
    app.spwindow.deiconify()
    numSprites = len(app.usprites)
    spritesPerRow = config.spritesperrow
    spriteColumns = int(numSprites/config.spritesperrow)
    xsize = (app.spritexsize)*config.pixelsize
    ysize = (app.spriteysize)*config.pixelsize 
    spacing = 4
    canvasWidth = spritesPerRow *(xsize+spacing)
    canvasHeight = spriteColumns*(ysize+spacing)
    print (canvasWidth,canvasHeight)
    shownSprites = 0
    spritesCanvas = Canvas (app.spwindow,width=canvasWidth,height=canvasHeight)
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
        drawboxel (app,spritesCanvas,app.usprites,currentSprite,currX,currY)
        currX = currX+(xsize+spacing)
        currentSprite = currentSprite + 1
        shownSprites = shownSprites + 1
        if shownSprites == spritesPerRow:
            currX = 1
            currY = currY + (ysize+spacing)
            shownSprites=0

            
def updatePixel (canvas,switchon,app):
    fill = ""
    pixelcolor = 0
    tags = canvas.gettags(CURRENT)
    if len(tags)<2:
        return
    print (tags[0])
    if switchon:
      fill = "blue"
      pixelcolor = 1
    if canvas.find_withtag(CURRENT):
      canvas.itemconfig(CURRENT, fill=fill)
      coords = tags[0].split('/')
      app.usprites[coords[0]][coords[1]][coords[2]]=pixelcolor
      canvas.update_idletasks()
        
def drawboxel (app,canvas,sprites,index,x,y):
    startx = x
    sprite = sprites[index]
    py=0
    for row in sprite:
        px=0
        ey = y + config.pixelsize
        for pixel in range (0,app.spritexsize):
            ex = x + config.pixelsize
            if int(row[pixel]) != 0:
                palettecolor = app.palette[int(row[pixel])]
                rgb = (palettecolor[0]*config.msxcolordivider,
                       palettecolor[1]*config.msxcolordivider,
                       palettecolor[2]*config.msxcolordivider)
                color = "#%02x%02x%02x" % rgb
                canvas.create_rectangle (x,y,ex,ey,fill=color,tag=str(index)+"/"+str(px)+"/"+str(py))
                px = px +1
            else:
                canvas.create_rectangle (x,y,ex,ey,tag=str(index)+"/"+str(px)+"/"+str(py))
                
            x = ex
        x = startx
        y=ey
        py = py + 1        

def createSpritesWindow(app):
    app.spwindow =  tk.Toplevel(app.root)
    app.spwindow.title("Sprite List")
    app.spwindow.iconbitmap(config.iconfile)
    app.spwindow.geometry(str(config.appxsize)+"x"+str(config.appysize))
    app.spwindow.withdraw()
    app.spwindow.protocol("WM_DELETE_WINDOW", closeSprites(app))
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')

def closeSprites(app):
    app.spwindow.destroy()

    """
    row = 0
    column = 0
    top_frame = Frame(app.spwindow, bg='cyan', width=64, height=64, pady=3)
    for sprite in app.csprites:
        top_frame.grid(row=row,column=column)
        column=column+1
        if column == 9:
            column = 0
            row = row + 1
    """