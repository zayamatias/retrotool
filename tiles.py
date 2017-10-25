import tkinter as tk
import config
import math
from tkinter import *
import retrofunctions


def showTiles (app):
    #display the sprites grid, initializing everything first
    if hasattr(app.img,'filename'):
        if app.img.filename == config.logoimage :
            messagebox.showinfo("Error","Please, load an image or start a new project first")
            return 1
    if set(app.bgcolor) == set((-1,-1,-1)):
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    createTempTiles(app)
    if (app.tilwindow!=None):
        if (app.tilesCanvas != None) and (app.tilwindow.winfo_exists()!=0):    
            for child in app.tilwindow.winfo_children():
                child.destroy()
                app.tileCanvas = None
        else:
            createTilesWindow(app)
            #displayPalette(app)
    else:
        createTilesWindow(app)
            
    app.tilwindow.deiconify()
    numTiles = len(app.Tiles)
    if (app.imgwidth!=0):
       app.tilesPerRow = config.tilesPerRow
    app.tilesPerCol = int(math.ceil(numTiles/app.tilesPerRow))
    xsize = (app.tilexsize)*app.pixelsize
    ysize = (app.tileysize)*app.pixelsize
    spacing = 4
    canvasWidth = app.tilesPerRow *(xsize+spacing)
    canvasHeight = app.tilesPerCol*(ysize+spacing)
    shownTiles = 0
    app.tilesCanvas = Canvas (app.tilwindow,width=canvasWidth,height=canvasHeight,scrollregion=(0, 0, canvasWidth, canvasHeight))
    # Mous click actions left-> Put pixel, Right-> Remove pixel
    app.tilesCanvas.bind('<Button-1>', lambda x:updateTilePixel(app.tilesCanvas,True,app))
    #app.spritesCanvas.bind("<B1-Motion>",lambda event: moveSpriteCanvas(app.spritesCanvas,x = event.x,y = event.y))
    app.tilesCanvas.bind('<Button-3>', lambda x:selectTile(app.tilesCanvas,app))
    # Canvas by default does not get focus, so this means that if this is not set
    # key binding will not work!
    app.tilesCanvas.bind('<Key>', lambda event:moveTiles(event,app.tilesCanvas,app))

    if canvasWidth>config.appxsize:
        #add horizontal scroll
        xscrollbar = Scrollbar(app.tilwindow,orient=HORIZONTAL)
        xscrollbar.pack (side=BOTTOM, fill=X)
        app.tilesCanvas.config(xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=app.tilesCanvas.xview)
    if canvasHeight>config.appysize:
        #add vertical scroll
        yscrollbar = Scrollbar(app.tilwindow)
        yscrollbar.pack (side=RIGHT, fill=Y)
        app.tilesCanvas.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=app.tilesCanvas.yview)

    #Add scroll commands:

    app.tilesCanvas.pack()
    app.tilesCanvas.focus_set()
    currX = 1
    currY = 1
    currentTile = 0
    for row in range (0,numTiles):
        destX = currX + (xsize)
        destY = currY + (ysize)
        app.tilesCanvas.create_rectangle(currX,currY,destX,destY,width=(spacing/2),tags="tile,til"+str(currentTile)+"canvas")
        #draw each "boxel" of the sprite
        retrofunctions.drawboxel (app,app.tilesCanvas,app.Tiles[currentTile],currX,currY,currentTile,app.tilexsize)
        currX = currX+(xsize+spacing)
        currentTile = currentTile + 1
        shownTiles = shownTiles + 1
        if shownTiles == app.tilesPerRow:
            currX = 1
            currY = currY + (ysize+spacing)
            shownTiles=0

def createTempTiles(app):
    #Goal is to go trhough pixels in tilex*tiley and extract tiles
    #find duplicate tiles and skip them so at the end you only have the minimum needed tiles
    app.Tiles = []
    app.tilesPerRow = int(app.imgwidth/app.tilexsize)
    app.tilesPerCol = int(app.imgheight/app.tileysize)
    for tiley in range (0,app.tilesPerCol):
        for tilex in range (0,app.tilesPerRow):
            thistile = []
            for py in range (0,app.tileysize):
                thiscolors = []   #Background is a must have as color
                srow ="" # Holds the scanned row of each tile
                         # Since color can be more than 1, we need a color indicator
                for px in range (0,app.tilexsize):
                    position = ((tilex*app.tilexsize)+px)+((app.tileysize*app.imgwidth*tiley)+(py*app.imgwidth))
                    imgRow = int ((position)/app.imgwidth)+1
                    extraRowUpper = imgRow+int(app.sprImgOffset/app.imgwidth)
                    extraRowLower = imgRow+int(app.sprImgOffset/app.imgwidth)-1
                    upperlimit = (app.imgwidth)*extraRowUpper
                    lowerlimit = (app.imgwidth)*extraRowLower
                    position = position + app.tileImgOffset
                    ### We need to calculate the offset
                    if ((position < len(app.pixels)) and (position >= 0) and (position < upperlimit) and (position >= lowerlimit)):
                        color = str(app.pixels[position])
                    else:
                        color = "0"
                    if (color not in thiscolors) and (int(color) != 0):
                        thiscolors.append (color)
                    srow = srow + "%" + color
                thistile.append(srow)
            if not isTileExisting (thistile,app.Tiles):
                app.Tiles.append(thistile)
#    print ("Finsihed creating tiles, found a total of "+str(len(app.Tiles)))           

def isTileExisting (tile,tiles): # Check if te tile is already in the tileset
    for tileb in tiles:
        if compareTiles (tile,tileb):
            return True
    return False
def compareTiles(tilea,tileb): # check if tilea is the same as tileb
    for x in range (0,len(tilea)):
        if tilea[x] != tileb[x]:
            return False
    return True

def createTilesWindow(app):
    #window to show the sprites in
    app.tilwindow =  tk.Toplevel(app.root)
    app.tilwindow.title("Tiles Overview")
    app.tilwindow.iconbitmap(config.iconfile)
    app.tilwindow.geometry(str(config.appxsize)+"x"+str(config.appysize))
    app.tilwindow.protocol("WM_DELETE_WINDOW", lambda:closeTilesWindow(app))
    app.tilwindow.withdraw()

def closeTilesWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.tilwindow.destroy()
