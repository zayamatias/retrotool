import tkinter as tk
import config
import math
import retrofunctions
import retroclasses


def showTilesMap (app):
    if app.TileMap==[]:
         tk.messagebox.showinfo("Error","Please, create some tiles from an image first")
         return 1
    tilesPerRow = int(app.imgwidth/app.tilexsize)
    tilesPerCol = int(len(app.TileMap)/tilesPerRow)
    currX = 0
    currY = 0
    createTilesMapWindow(app)
    app.tilmwindow.deiconify()
    xsize = (app.tilexsize)*app.pixelsize
    ysize = (app.tileysize)*app.pixelsize
    spacing = 4
    canvasWidth = tilesPerRow *(xsize+spacing)
    canvasHeight = tilesPerCol*(ysize+spacing)
    app.tilesMapCanvas = tk.Canvas (app.tilmwindow,width=canvasWidth,height=canvasHeight,scrollregion=(0, 0, canvasWidth, canvasHeight))
    if canvasWidth>config.appxsize:
        #add horizontal scroll
        xscrollbar = tk.Scrollbar(app.tilmwindow,orient=tk.HORIZONTAL)
        xscrollbar.pack (side=tk.BOTTOM, fill=tk.X)
        app.tilesMapCanvas.config(xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=app.tilesMapCanvas.xview)
    if canvasHeight>config.appysize:
        #add vertical scroll
        yscrollbar = tk.Scrollbar(app.tilmwindow)
        yscrollbar.pack (side=tk.RIGHT, fill=tk.Y)
        app.tilesMapCanvas.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=app.tilesMapCanvas.yview)
    shownTiles = 0
    currentTile = 0
    app.tilesMapCanvas.pack()
    app.tilesMapCanvas.focus_set()
    for tile in app.TileMap:
        destX = currX + (xsize)
        destY = currY + (ysize)
        app.tilesMapCanvas.create_rectangle(currX,currY,destX,destY,width=(spacing/2),tags="tile,til"+str(currentTile)+"canvas")
        #draw each "boxel" of the sprite
        retrofunctions.drawboxel (app,app.tilesMapCanvas,app.Tiles[tile],currX,currY,currentTile,app.tilexsize)
        currX = currX+(xsize+spacing)
        currentTile = currentTile + 1
        shownTiles = shownTiles + 1
        if int(shownTiles) == int(tilesPerRow):
            currX = 1
            currY = currY + (ysize+spacing)
            shownTiles=0

def showTiles (app):
    #display the sprites grid, initializing everything first
    if hasattr(app.img,'filename'):
        if app.img.filename == config.logoimage :
            tk.messagebox.showinfo("Error","Please, load an image or start a new project first")
            return 1
    if set(app.bgcolor) == set((-1,-1,-1)):
        tk.messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    retrofunctions.getPixels(app,app.tpixels)
    createTiles(app)
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
    app.tilesCanvas = tk.Canvas (app.tilwindow,width=canvasWidth,height=canvasHeight,scrollregion=(0, 0, canvasWidth, canvasHeight))
    # Mous click actions left-> Put pixel, Right-> Remove pixel
    app.tilesCanvas.bind('<Button-1>', lambda x:updateTilePixel(app.tilesCanvas,True,app))
    #app.spritesCanvas.bind("<B1-Motion>",lambda event: moveSpriteCanvas(app.spritesCanvas,x = event.x,y = event.y))
    app.tilesCanvas.bind('<Button-3>', lambda x:selectTile(app.tilesCanvas,app))
    # Canvas by default does not get focus, so this means that if this is not set
    # key binding will not work!
    app.tilesCanvas.bind('<Key>', lambda event:moveTiles(event,app.tilesCanvas,app))

    if canvasWidth>config.appxsize:
        #add horizontal scroll
        xscrollbar = tk.Scrollbar(app.tilwindow,orient=tk.HORIZONTAL)
        xscrollbar.pack (side=tk.BOTTOM, fill=tk.X)
        app.tilesCanvas.config(xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=app.tilesCanvas.xview)
    if canvasHeight>config.appysize:
        #add vertical scroll
        yscrollbar = tk.Scrollbar(app.tilwindow)
        yscrollbar.pack (side=tk.RIGHT, fill=tk.Y)
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
        if int(shownTiles) == int(app.tilesPerRow):
            currX = 1
            currY = currY + (ysize+spacing)
            shownTiles=0
    retrofunctions.displayPalette(app)
    
def createTiles(app):
    #Goal is to go trhough pixels in tilex*tiley and extract tiles
    #find duplicate tiles and skip them so at the end you only have the minimum needed tiles
    currentTile = 0
    app.TileMap = []
    app.ColorTiles = []
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
                    if ((position < len(app.tpixels)) and (position >= 0) and (position < upperlimit) and (position >= lowerlimit)):
                        color = str(app.tpixels[position])
                    else:
                        color = "0"
                    if (color not in thiscolors) and (int(color) != 0):
                        thiscolors.append (color)
                    srow = srow + "%" + color
                thistile.append(srow)
            tileIndex = getTileIndex(thistile,app.Tiles,currentTile)
            app.TileMap.append(tileIndex)
            app.ColorTiles.append(thistile)
            if int(tileIndex) == int(currentTile):
                currentTile = currentTile +1
                tilepattern = []
                colorpattern = []
                for row in thistile:
                    splitrow = row.split('%')
                    colrow = [-1,-1]
                    binpattern = ""
                    colidx = 0
                    for bit in splitrow:
                        if (bit !="") and (colidx<2) and (bit not in colrow):
                            colrow[colidx]=bit
                            colidx = colidx + 1
                        if (bit!=""):
                            if (bit in colrow):
                                binpattern = binpattern + str(colrow.index(bit))
                            else:
                                binpattern = binpattern + "0"

                    msb = 0 if (int(colrow[1])==-1) else int(colrow[1])
                    lsb = 0 if (int(colrow[0])==-1) else int(colrow[0])
                    msb = msb << 4
                    byte = msb|lsb
                    colorpattern.append(byte)
                    tilepattern.append(binpattern)
                app.FinalTiles.append(retroclasses.tile(tilepattern,colorpattern))
                app.Tiles.append(thistile)
#    print ("Finsihed creating tiles, found a total of "+str(len(app.Tiles)))           

def getTileIndex (tile,tiles,idx): # Check if te tile is already in the tileset
    nidx = 0;
    for tileb in tiles:
        if compareTiles (tile,tileb):
            return nidx
        nidx = nidx + 1
    return idx

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

def createTilesMapWindow(app):
    #window to show the sprites in
    app.tilmwindow =  tk.Toplevel(app.root)
    app.tilmwindow.title("Tiles Map Overview")
    app.tilmwindow.iconbitmap(config.iconfile)
    app.tilmwindow.geometry(str(config.appxsize)+"x"+str(config.appysize))
    app.tilmwindow.protocol("WM_DELETE_WINDOW", lambda:closeTilesMapWindow(app))
    app.tilmwindow.withdraw()

def closeTilesMapWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.tilmwindow.destroy()