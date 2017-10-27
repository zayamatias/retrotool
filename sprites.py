import sys
import PIL.Image
import PIL.ImageTk
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import tkinter as tk
import retrofunctions
from functools import partial
import config
import retroclasses
import math

def findOrColor (csprites):
    # This function finds which is the best pixel to or according to the palette colors
    # This is used on MSX2 -> See https://www.msx.org/wiki/The_OR_Color
    numcols = len(csprites)
    c=[-1,-1,-1]
    pc=[-1,-1,-1,False]
    if  numcols < 5:
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
def createTempSprites (app):
    #Creates two arrays, uspritrs, which holds the pattern in colors (1,2,3....)
    #Csprites which holds the colors that are used in each line of the sprite
    retrofunctions.getPixels(app,app.spixels)
    app.usprites = []
    app.csprites = []
    app.spritesPerRow = int(app.imgwidth/app.spritexsize)
    app.spritesPerCol = int(app.imgheight/app.spriteysize)
    for spy in range (0,app.spritesPerCol):
        for spx in range (0,app.spritesPerRow):
            thissprite = []
            thisspritecolors=[]
            for py in range (0,app.spriteysize):
                thiscolors = []   #Background is a must have as color
                srow ="" # Holds the scanned row of each sprite
                         # Since color can be more than 1, we need a color indicator
                for px in range (0,app.spritexsize):

                    #WIP
                    position = ((spx*app.spritexsize)+px)+((app.spriteysize*app.imgwidth*spy)+(py*app.imgwidth))
                    imgRow = int ((position)/app.imgwidth)+1
                    extraRowUpper = imgRow+int(app.sprImgOffset/app.imgwidth)
                    extraRowLower = imgRow+int(app.sprImgOffset/app.imgwidth)-1
                    upperlimit = (app.imgwidth)*extraRowUpper
                    lowerlimit = (app.imgwidth)*extraRowLower
                    position = position + app.sprImgOffset
                    ### We need to calculate the offset
                    if ((position < len(app.spixels)) and (position >= 0) and (position < upperlimit) and (position >= lowerlimit)):
                        color = str(app.spixels[position])
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
            emptySprite = True
            for y in range (0,app.spriteysize):
                pc=findOrColor(app.csprites[myindex][y])
                oc=pc[2]
                trow = "";
                row = usprite[y]
                for x in range (0,app.spritexsize):
                    pcolor = retrofunctions.getTempColor (row,x)
                    if (int(pcolor)==int(pc[numsprites])) or (int(pcolor)==int(oc)):
                        trow = trow+"1"
                        emptySprite = False
                    else:
                        trow = trow+"0"
                tsprite.append(trow)
                if pc[numsprites]==-1:
                    tcolor.append (0)
                else:
                    tcolor.append (pc[numsprites])
            if not emptySprite:
                mysprite = retroclasses.sprite (tsprite,tcolor,ored)
                app.finalsprites.append(mysprite)
            if needtoor:
                ored = not ored
        myindex = myindex+1
def showSprites (app):
    #display the sprites grid, initializing everything first
    if hasattr(app.img,'filename'):
        if app.img.filename == config.logoimage :
            messagebox.showinfo("Error","Please, load an image or start a new project first")
            return 1
    if set(app.bgcolor) == set((-1,-1,-1)):
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    if (app.spwindow!=None):
        if (app.spritesCanvas != None) and (app.spwindow.winfo_exists()!=0):    
            for child in app.spwindow.winfo_children():
                child.destroy()
                app.spritesCanvas = None
        else:
            createSpritesWindow(app)
            retrofunctions.displayPalette(app)
    else:
        createSpritesWindow(app)
            
    createTempSprites(app)
    
    app.spwindow.deiconify()
    numSprites = len(app.usprites)
    if (app.imgwidth!=0):
       app.spritesPerRow = int(math.ceil(app.imgwidth/app.spritexsize))
    app.spritePerCol = int(math.ceil(numSprites/app.spritesPerRow))
    xsize = (app.spritexsize)*app.pixelsize
    ysize = (app.spriteysize)*app.pixelsize
    spacing = 4
    canvasWidth = app.spritesPerRow *(xsize+spacing)
    canvasHeight = app.spritePerCol*(ysize+spacing)
    shownSprites = 0
    app.spritesCanvas = Canvas (app.spwindow,width=canvasWidth,height=canvasHeight,scrollregion=(0, 0, canvasWidth, canvasHeight))
    # Mous click actions left-> Put pixel, Right-> Remove pixel
    app.spritesCanvas.bind('<Button-1>', lambda x:updatePixel(app.spritesCanvas,True,app))
    #app.spritesCanvas.bind("<B1-Motion>",lambda event: moveSpriteCanvas(app.spritesCanvas,x = event.x,y = event.y))
    app.spritesCanvas.bind('<Button-3>', lambda x:selectSprite(app.spritesCanvas,app))
    # Canvas by default does not get focus, so this means that if this is not set
    # key binding will not work!
    app.spritesCanvas.bind('<Key>', lambda event:moveSprites(event,app.spritesCanvas,app))

    if canvasWidth>config.appxsize:
        #add horizontal scroll
        xscrollbar = Scrollbar(app.spwindow,orient=HORIZONTAL)
        xscrollbar.pack (side=BOTTOM, fill=X)
        app.spritesCanvas.config(xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=app.spritesCanvas.xview)
    if canvasHeight>config.appysize:
        #add vertical scroll
        yscrollbar = Scrollbar(app.spwindow)
        yscrollbar.pack (side=RIGHT, fill=Y)
        app.spritesCanvas.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=app.spritesCanvas.yview)

    #Add scroll commands:

    app.spritesCanvas.pack()
    app.spritesCanvas.focus_set()
    currX = 1
    currY = 1
    currentSprite = 0
    for row in range (0,numSprites):
        destX = currX + (xsize)
        destY = currY + (ysize)
        app.spritesCanvas.create_rectangle(currX,currY,destX,destY,width=(spacing/2),tags="sprite,spr"+str(currentSprite)+"canvas")
        #draw each "boxel" of the sprite
        
        
        retrofunctions.drawboxel (app,app.spritesCanvas,app.usprites[currentSprite],currX,currY,currentSprite,app.spritexsize)
        currX = currX+(xsize+spacing)
        currentSprite = currentSprite + 1
        shownSprites = shownSprites + 1
        if shownSprites == app.spritesPerRow:
            currX = 1
            currY = currY + (ysize+spacing)
            shownSprites=0
    retrofunctions.displayPalette(app)
    # If canvas is bigger than screen then show scrollbars

def moveSpriteCanvas(canvas,x,y):
    print ("moving"+str(x)+"//"+str(y))
    
def moveSprites(event,canvas,app):
    """
    Left     37
    Up	    38
    Right    39
    Down     40
    """
    if int(event.keycode) == 38:
        app.sprImgOffset = app.sprImgOffset + app.imgwidth
    if int(event.keycode) == 40:
        app.sprImgOffset = app.sprImgOffset - app.imgwidth
    if int(event.keycode) == 37:
        app.sprImgOffset = app.sprImgOffset +1
    if int(event.keycode) == 39:
        app.sprImgOffset = app.sprImgOffset -1
    app.usprites = []
    app.csprites = []
    createTempSprites (app)
    showSprites(app)
def selectSprite(canvas,app):
    print (canvas.gettags("sprite"))
def updatePixel (canvas,switchon,app):
    fill = app.spriteeditorbgcolor
    pixelcolor = 0
    tags = canvas.gettags(CURRENT)
    if len(tags)<2:
        return
    if (switchon) and (app.drawColor != 0):
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
      
      # Update pixels object
      # need to convert sprite/pixel/pxpy 
      # Tengo el spriteID, y las coordenadas del pixel en el sprite
      position = ((spriteidx*app.spritexsize)+px)+(py*app.imgwidth)
      app.spixels[position]=str(app.drawColor)
      canvas.update_idletasks()

def createSpritesWindow(app):
    #window to show the sprites in
    app.spwindow =  tk.Toplevel(app.root)
    app.spwindow.title("Sprite Overview")
    app.spwindow.iconbitmap(config.iconfile)
    app.spwindow.geometry(str(config.appxsize)+"x"+str(config.appysize))
    app.spwindow.protocol("WM_DELETE_WINDOW", lambda:closeSpritesWindow(app))
    app.spwindow.withdraw()
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')

def chgNbrSprites(value,app):
    app.newSprites = int(value.get())

def chgSprXSize(value,app):
    app.spritexsize = int(value.get())

def chgSprYSize(value,app):
    app.spriteysize = int(value.get())
    
def chgPixelSize(value,app):
    app.pixelsize = int(value.get())
    

def createAnimationWindow (app):
    app.animWindow =  tk.Toplevel(app.root)
    app.animWindow.title("Character Animation")
    app.animWindow.iconbitmap(config.iconfile)
    app.animWindow.geometry(str(config.animWxSize)+"x"+str(config.animWySize))
    app.animWindow.protocol("WM_DELETE_WINDOW", lambda:closeAnimationWindow(app))

    e = Entry(app.animWindow)
    e.insert (0,app.animArray)
    w = Entry(app.animWindow)
    w.insert (0,app.animCols)
    h = Entry(app.animWindow)
    h.insert (0,app.animRows)
    b = tk.Button(app.animWindow, text="update sprites",command = lambda:updateAnimation(app,e,w,h))
    e.pack()
    w.pack()
    h.pack()
    b.pack()
    
    
    
def updateAnimation(app,e,w,h):
        app.animArray = e.get().split(' ')
        app.animCols = int(w.get())
        app.animRows = int(h.get())
        
        animate (app)
        
        
def animate (app):
    if (app.csprites == []):
        messagebox.showinfo("Error","Please, create sprites before trying to animate them ;-)")
        return 1
   
    app.animation = retroclasses.animation()
    
    for ch in app.animArray:
        ch =int(ch)
        character = retroclasses.character (app.animRows,app.animCols)
        for y in range (0,app.animRows):
            for x in range (0,app.animCols):
                #(MOD(ch;(ssr/animcol))*animcol)+(int(ch/(ssr/animcol))*animrows*ssr)+x+(y*ssr)

                idx = ( (ch % int(app.spritesPerRow/app.animCols))*app.animCols)+(int(ch/(app.spritesPerRow/app.animCols))*app.animRows*app.spritesPerRow)+x+(y*app.spritesPerRow)
                character.insertSprite(app.usprites[idx],y,x)
        app.animation.addCharacter(character)
            
    animWxSize = app.spritexsize*app.animCols*config.pixelsize
    animWySize = app.spriteysize*app.animRows*config.pixelsize
        
    if app.animWindow != "":
        app.animWindow.destroy()
    createAnimationWindow (app)
    app.animCanvas = Canvas (app.animWindow,width=animWxSize,height=animWySize)
    app.animCanvas.bind('<Key>', lambda event:animateSprite(event,app))

    app.animCanvas.pack()
    app.animCanvas.focus_set()

    app.frame = 0
    animateSprite(None,app)




def animateSprite (event,app):
    if event != None:
        if int(event.keycode) == 37:
            app.frame = app.frame+1
        if int(event.keycode) == 39:
            app.frame = app.frame -1
        if app.frame >= app.animation.numFrames():   
            app.frame = 0
        if app.frame < 0 :
            app.frame = app.animation.numFrames()-1
    xsize = (app.spritexsize)*app.pixelsize
    ysize = (app.spriteysize)*app.pixelsize
    spacing = 2
    currX = 1
    currY = 1
    app.animCanvas.delete("all")
    for row in range (app.animation.characters[app.frame].rows):
        for col in range (app.animation.characters[app.frame].cols):
            destX = currX + (xsize)
            destY = currY + (ysize)
            app.animCanvas.create_rectangle(currX,currY,destX,destY,width=(spacing/2))
            #draw each "boxel" of the sprite
            drawboxel (app,app.animCanvas,app.animation.characters[app.frame].sprites[row][col],currX,currY,fsdjhfsdfjksd)
            currX = currX+(xsize+spacing)
        currX = 1
        currY = currY + (ysize+spacing)
    app.animWindow.update()
    app.root.update()
        
def closeSpritesWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.spwindow.destroy()
