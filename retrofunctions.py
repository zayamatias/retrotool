import pickle
import PIL.Image
import PIL.ImageTk
import config
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tiles
import math
import sprites
import imageexport

def newProject(app):
    # Create empty array of pixels
    app.imgwidth = app.spritexsize*math.ceil(math.sqrt(app.newSprites))
    app.imgheight = app.spriteysize*math.ceil(math.sqrt(app.newSprites))
    app.pixels = [0]*(app.imgwidth*app.imgheight)
    app.img.filename=""
    sprites.createTempSprites (app)


def writeASMFile(app):
    #crete the aoutput .asm file with the sprite data, colors & palette
    if app.usprites != []:
        sprites.createFinalSprites(app)
    f = open(app.outfile, 'w')
    if len (app.finalsprites)>0:
        f.write ("SPRITE_DATA:\n")
        idx = 0
        for fsprite in app.finalsprites:
            line = fsprite.getAsmPattern(app.spritexsize)
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
    if (len(app.FinalTiles)>0):
        for dindex in range (cindex,16):
            f.write ("\tdb $77,$7\n")
        f.write ("TILE_DATA:\n")
        for tile in app.FinalTiles:
            f.write(tile.getAsmPattern(app.tilexsize)+"\n")
        f.write ("TILE_COLORS:\n")
        for tile in app.FinalTiles:
            f.write(tile.getAsmColors(app.tilexsize)+"\n")
        f.write ("TILE_MAP:\n\tdb ")
        ntiles= 0
        ttiles = 0
        for idx in app.TileMap:
            f.write("$"+"{0:02x}".format(idx))
            ntiles = ntiles +1 #These are the tiles per line (just to keep it tidy)
            ttiles = ttiles + 1 #These are the total tiles
            if (ntiles ==32) and (ttiles < len(app.TileMap)):
                f.write("\n\tdb ")
                ntiles = 0
            elif (ntiles != 32):
                f.write(",")
        f.write ("\n")

def exportToTiled(app):
    if not app.Tiles:
        messagebox.showinfo("Error","Please create some tiles first")
        return 1        
    cols = config.tilesPerRow
    rows = math.ceil(len(app.FinalTiles)/cols)
    img = PIL.Image.new('RGB',(int(cols*app.tilexsize), int(rows*app.tileysize)))
    pixels = img.load()    
    y= 0
    tileidx = 0
    for trow in range (0,rows):
         for row in range (0,app.tileysize):
           x = 0
           for tcol in range (0,cols):
                tileidx = (trow*cols)+tcol
                try:
                    tile = app.Tiles[tileidx]
                except:
                    tile =[]
                    tilex = ""
                    for a in range (0,app.tilexsize):
                        tilex= tilex+"%0"
                    for a in range (0,app.tileysize):
                        tile.append(tilex)
                cpattern = tile[row].split("%")
                if cpattern [0] == "":
                    del cpattern[0]
                for col in range (0,app.tilexsize):
                    pcolor =  int(cpattern[col])
                    
                    if pcolor !="":
                        coltuple = app.palette[pcolor]
                        if pcolor == 0:
                            coltuple = (0,0,0)
                        pixels[x,y]=(coltuple[0]*32,coltuple[1]*32,coltuple[2]*32)#coltuple
                        x = x +1
           y = y + 1
    imgfile = app.opfile[:app.opfile.rindex('.')]
    imgfile = imgfile+"_tiles.png"
    tiledfile = imgfile+".tmx"
    img.save(imgfile)
    tilemap = ""
    for tile in app.TileMap:
        tilemap = tilemap+str(tile+1)+","
    tilemap = tilemap[:-1]
    f = open(tiledfile, 'w')
    output = config.tiled_xml
    output = output.replace("__TILESX__",str(int(app.imgwidth/app.tilexsize)))
    output = output.replace("__TILESY__",str(int(app.imgheight/app.tileysize)))
    output = output.replace("__TILEXSIZE__",str(app.tilexsize))
    output = output.replace("__TILEYSIZE__",str(app.tileysize))
    output = output.replace("__NUMTILES__",str(int(cols*rows)))
    output = output.replace("__IMGWIDTH__",str(int(cols*app.tilexsize)))
    output = output.replace("__IMGHEIGHT__",str(int(rows*app.tileysize)))
    output = output.replace("__NUMTILES__",str(cols*rows))
    output = output.replace("__TILEMAP__",tilemap)
    output = output.replace("__FILENAME__",imgfile)
    f.write(output)

                        
def exportMSXScreen(app):
    if not app.Tiles:
        messagebox.showinfo("Error","Please create some tiles first")
        return 1        
    outfile = filedialog.asksaveasfilename(parent=app.root,filetypes=[("Screen Files",config.extensions[app.targetSystem.get()])])
    extension = outfile[outfile.index('.'):]
    f = open(outfile, 'wb')
    # First write the tiles themselves
    if extension.upper() == ".SC2":
        imageexport.Screen2(app,f,outfile)
    if extension.upper() == ".SC4":
        imageexport.Screen4(app,f,outfile)
    if extension.upper() == ".SC5":
        imageexport.Screen5(app,f,outfile)
    if extension.upper() == ".SC3":
        imageexport.Screen3(app,f,outfile)
    if extension.upper() == ".SC6":
        imageexport.Screen6(app,f,outfile)
    if extension.upper() == ".SC7":
        imageexport.Screen7(app,f,outfile)
    if extension.upper() == ".SC8":
        imageexport.Screen8(app,f,outfile)
    if (extension.upper() == ".S10") or (extension.upper() == ".S11") or (extension.upper() == ".S12"):
        imageexport.Screen10plus(app,f,outfile)
    

def exportASMFile(app):

    #do the actual saving of the file
    """if app.usprites == []:
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    """
    app.outfile = filedialog.asksaveasfilename(parent=app.root)
    writeASMFile(app)


def resetProject(app):
        app.projfile =""
        # Objects to be saved/loaded to/from project file
        app.pixels = []
        app.finalsprites = []
        app.usprites = []
        app.csprites = []
        app.bgcolor = (-1,-1,-1)
        app.palette=config.palettes[app.targetSystem.get()][2]
        app.imgwidth = 0
        app.imgheight = 0
        app.sprImgOffset = 0
        app.tileImgOffset = 0
        app.TileMap = []


def openROMFile(app):
    app.romfile = filedialog.askopenfilename(parent=app.root,filetypes=[("ROM Files","*.rom;*.nes;*.sms;*.sr5")])
    if (app.romfile==""):
        return 1
    resetProject(app)
    with open(app.romfile, mode='rb') as file:
        romContent = file.read()
    app.imgwidth = config.ROMWidth
    cols = 1
    rows = 1
    for byte in romContent:
        binbyte = '{0:08b}'.format(byte)
        #( bin(int(sbyte, 16))[2:] ).zfill(16)
        for bit in range(8):
            cols = cols + 1
            app.spixels.append (binbyte[bit])
            if cols==config.ROMWidth:
                rows = rows+1
                cols = 1

    app.imgheight=rows
    app.bgcolor = (0,0,0)
    sprites.createTempSprites (app)


def openImageFile(app):
    #ask for a file to open
    #to speed up testing, if a file is set in the config it will not ask to open but will open directly this one
    if config.default_filename == "":
        app.opfile = filedialog.askopenfilename(parent=app.root,filetypes=[("Image Files","*.jpg;*.gif;*.png;*.bmp")])
    else:
        app.opfile = config.default_filename
    if (app.opfile==""):
        return 1
    resetProject(app)
    app.cv.update()
    app.img = PIL.Image.open(app.opfile)
    app.img = app.img.convert('RGB')
    #CHeck if the max number of colors accepted by the system is equal or more than the colors of the image
    colok = checkColors (app)
    sizeok = checkSize (app)
    if (not colok) or (not sizeok):
        return 1
    #create the image
    app.imgwidth=app.img.size[0]
    app.imgheight=app.img.size[1]
    app.spritephoto=PIL.ImageTk.PhotoImage(app.img)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.scale.set(1)
    app.scale.pack()
    app.root.update()
    app.bgcolor=(-1,-1,-1) # for some reason color is changed when double ckicking on filename, maybe a canvas thing;...
def saveProject (app):
    if (app.projfile==""):
        if app.opfile!="":
            app.projfile = app.opfile[:len(app.opfile)-3]+"prj"
        else:
            app.projfile = filedialog.asksaveasfilename(parent=app.root,filetypes=[("Project Files","*.prj")])

    with open(app.projfile,"wb") as f:
        pickle.dump ((app.imgwidth,app.imgheight,app.pixels,app.finalsprites,app.usprites,app.csprites,app.palette),f,pickle.HIGHEST_PROTOCOL)

def loadProject (app):
    loadprojfile = filedialog.askopenfilename(parent=app.root,filetypes=[("Project Files","*.prj")])
    if (loadprojfile!=""):
        resetProject(app)
        app.projfile = loadprojfile
        try:
            with open(app.projfile,"rb") as f:
                (app.imgwidth,app.imgheight,app.pixels,app.finalsprites,app.usprites,app.csprites,app.palette)=pickle.load(f)
        except:
            messagebox.showinfo("Error","The file you tried to open is not compatible")

            
def zoomimage(app):
    #function called to zoom the image loaded in or out (according to the selected scale)
    zoom = int(app.scale.get())
    myimg = app.img.resize ((app.imgwidth*zoom,app.imgheight*zoom))
    app.spritephoto=PIL.ImageTk.PhotoImage(myimg)
    app.cv.itemconfig(app.canvas_ref,image = app.spritephoto)
    app.cv.image = app.spritephoto
    app.cv.update()
    app.root.update()

def checkColors(app):
    #check if the colors of the image are within the limits of the system
    app.colors = app.img.getcolors(10000000)
    if (app.colors==None):
        app.colors = [(0,0,0)]*255
    numcolors = len(app.colors)
    if numcolors > app.maxcolors :
        messagebox.showinfo("Error","Max number of colors exceeded ("+str(numcolors)+" instead of "+str(app.maxcolors)+")")
        return False
    else:
        return True

def checkSize(app):
    #check if the colors of the image are within the limits of the system
    width = app.imgwidth
    if (width/app.spritexsize) != int (width/app.spritexsize):
        messagebox.showinfo("Error","Image width is not a multiple of sprite width ( currently set in config to "+str(app.spritexsize)+"px)")
        return False
    else:
        return True
def getColors(app):
    #get the system colors (needs to be generic, not yet done I believe)
    #app.palette =[app.bgcolor]
    #The code below will update (if possible) the palette,
    #it should be modified to run 2 times:
    #1st time get colors without modification (to stick to the original system palette)
    #2nd time, only if possible to modifiy colors, take into account used colors and modify/add when possible
    #Then all this logic should be outside the "getPixels" function!!!!!
    
    usedColors = [0]
    
    #first run : Check existing colors
    for color in app.colors:
        rgb = color[1]
        if not (isinstance( rgb, int )):
            r=int(int(rgb[0])/config.palettes[app.targetSystem.get()][1][0])
            g=int(int(rgb[1])/config.palettes[app.targetSystem.get()][1][1])
            b=int(int(rgb[2])/config.palettes[app.targetSystem.get()][1][2])
            # make sure we do not add bgcolor
            if set((r,g,b)) != set (app.bgcolor):
                # Iscolorin palette last parameters tells if it it must do a strict (FALSE) searrch or an extended (TRUE) search
                idx = findColor((r,g,b),app.palette,False)
                if idx != -1:
                    usedColors.append(idx)
    for color in app.colors:
        rgb = color[1]
        if not (isinstance( rgb, int )):
            r=int(int(rgb[0])/config.palettes[app.targetSystem.get()][1][0])
            g=int(int(rgb[1])/config.palettes[app.targetSystem.get()][1][1])
            b=int(int(rgb[2])/config.palettes[app.targetSystem.get()][1][2])
            # make sure we do not add bgcolor
            if set((r,g,b)) != set (app.bgcolor):
                # Iscolorin palette last parameters tells if it it must do a strict (FALSE) searrch or an extended (TRUE) search
                if findColor((r,g,b),app.palette,not config.syslimits[app.targetSystem.get()][4]) == -1:
                    found = False
                    for idx in range(len(app.palette)):
                        if (idx not in usedColors) and not found:
                            if config.syslimits[app.targetSystem.get()][3]:
                                app.palette[idx]=(r,g,b)
                                found = True
                                usedColors.append(idx)
                    if config.syslimits[app.targetSystem.get()][5] and not found:
                        app.palette.append((r,g,b))
                        found = True
                        usedColors.append(len(app.palette)-1)
                    elif not found:
                            messagebox.showinfo ("Warning","Cannot match / add some of the colors of the image, results may not be as expected")

def getPixels (app,pixelArray):
    #Read all the pixels and colors in the image
    #scan each pixel (Width) in each row (height)
    pixelScale = int(app.imgwidth* app.imgheight/100)
    pixelCount = 1
    if (app.imgwidth/app.spritexsize != int(app.imgwidth/app.spritexsize)):
        extracols = ((math.ceil(app.imgwidth/app.spritexsize))*app.spritexsize)-app.imgwidth
    else:
        extracols = 0
    app.prcanvas.pack()
    for y in range (0,app.imgheight):
        for x in range (0,app.imgwidth):
            pixelCount = pixelCount + 1
            if pixelCount >= pixelScale:
                pixelCount = 0
                app.progress['value']=app.progress['value']+1
                app.root.update_idletasks()
            try:
                pixel = app.img.getpixel((x,y))
            except:
                pixel = (0,0,0)
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            color = (int(r/config.palettes[app.targetSystem.get()][1][0]),int(g/config.palettes[app.targetSystem.get()][1][1]),int(b/config.palettes[app.targetSystem.get()][1][2]))
            error = False
            if set(color) != set(app.bgcolor): # color chosen by user
                index = findColor (color,app.palette,True) # Color must be found rpecisely now the palette is done
                if index != -1:
                    pixelArray.append(index)
                else:
                    pixelArray.append(0) # Cannot find color, then add background
                    error = True
            else:
                pixelArray.append('0')
        for x in range (0,extracols):
                pixelArray.append('0')
    if error:
        messagebox.showinfo ("Warning","Some colors have been discarded due to target system limtations (usually number of colors)")

                    
                
    app.imgwidth= app.imgwidth+extracols
    app.prcanvas.pack_forget()
    app.progress['value']=0



def paletteIndex(app,color):
    return findColor (color,app.palette)


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
    

def udpateTargetSystem(app,chgsystem):
    #Will be used when changing the target system
    print (app.targetSystem.get())
    print (chgsystem)
    app.targetSystem=config.systems.index(chgsystem)
    print (app.targetSystem)


def updateDrawColor (canvas,app):
    tags = canvas.gettags(tk.CURRENT)
    for rectangle in canvas.find_all():
       compare = canvas.itemcget(rectangle,"tags")
       if "current" not in compare :
            canvas.itemconfig (rectangle, outline="black")
       else:
            canvas.itemconfig (rectangle, outline="white")
    canvas.update_idletasks()
    canvas.focus_set()
    if len(tags)<1:
        return
    app.drawColor = int(tags[0])-1

def swapColor (canvas,app):
    if not (config.syslimits[app.targetSystem.get()][4]):
        messagebox.showinfo ("Error","Your target system does not allow for palette changes")
        return 1        
    tags = canvas.gettags(tk.CURRENT)
    if len(tags)<1:
        return
    newColor = int(tags[0])-1
    if (app.drawColor == 0) or (newColor == 0):
        messagebox.showinfo ("Error","Cannot swap with background color '0'")
        return 1
    if (app.drawColor == newColor):
        messagebox.showinfo ("Error","Cannot swap color with itself")
        return 1
    ## Update Pixels
    idx= 0
    for pixel in app.tpixels:
        if str(pixel)== str(app.drawColor):
            app.tpixels[idx]=str(newColor)
        elif str(pixel) == str(newColor):
            app.tpixels[idx]=str(app.drawColor)
        idx = idx + 1
    
    #TODO
    #Update Sprites
    #Update Tiles
    #How should it be done???    
    tiles.createTiles(app)
        
    ## Update Palette
    oldColors = app.palette[app.drawColor]
    newColors = app.palette[newColor]
    app.palette[app.drawColor]=newColors
    app.palette[newColor]=oldColors
    canvas.update_idletasks()
    canvas.itemconfig(app.paletteColorBoxes[app.drawColor], fill=transformColor(app,app.drawColor))
    canvas.itemconfig(app.paletteColorBoxes[newColor], fill=transformColor(app,newColor))

def drawboxel (app,canvas,sprite,x,y,index,width,bgcolor):
    border = 1
    if (app.pixelsize==2):
        border = 0
    startx = x
    py=0
    for row in sprite:
        px=0
        ey = y +app.pixelsize
        for pixel in range (0,width):
            ex = x +app.pixelsize
            pxColor = int(getTempColor(row,pixel))
            if pxColor == 0:
                color = bgcolor
            else:
                color = transformColor (app,pxColor)
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
            canvas.create_rectangle (x,y,ex,ey,fill=color,width=border)
            #else:
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
            #    canvas.create_rectangle (x,y,ex,ey,fill=app.spriteeditorbgcolor,tag=str(index)+"/"+str(px)+"/"+str(py),width=border)

            px = px + 1
            x = ex
        x = startx
        y=ey
        py = py + 1

def transformColor (app,paletteIndex):
    try:
        palettecolor = app.palette[paletteIndex]
    except:
        print ("exception at ",paletteIndex)
    r = palettecolor[0]
    g = palettecolor[1]
    b = palettecolor[2]
   # print (r,g,b)
    if r<0: r = 0        
    if g<0: g = 0        
    if b<0: b = 0        
    rgb = (r*config.palettes[app.targetSystem.get()][1][0],
           g*config.palettes[app.targetSystem.get()][1][1],
           b*config.palettes[app.targetSystem.get()][1][2])
    #print (rgb)
    color = "#%02x%02x%02x" % rgb
    return color


def createPaletteWindow(app,ysize):
    #window to show the sprites in
    app.palwindow =  tk.Toplevel(app.root)
    app.palwindow.title("ColorPalette")
    app.palwindow.iconbitmap(config.iconfile)
    app.palwindow.geometry(str(config.paletteWxSize)+"x"+str(ysize))
    app.palwindow.protocol("WM_DELETE_WINDOW", lambda:closePaletteWindow(app))
    app.palwindow.withdraw()
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')

def createPreferencesWindow(app):
    #window to show the sprites in
    app.prefwindow =  tk.Toplevel(app.root)
    app.prefwindow.title("Preferences")
    app.prefwindow.iconbitmap(config.iconfile)
    app.prefwindow.geometry(str(config.preferencesWxSize)+"x"+str(config.preferencesWySize))
    app.prefwindow.protocol("WM_DELETE_WINDOW", lambda:closePreferencesWindow(app))
    
    pixlabel = tk.Label(app.prefwindow, text="Pixel size in sprite editor")
    pixlabel.grid(row=0, sticky=tk.W)
    pixsizes = tk.StringVar(app.prefwindow)
    pixsizes.set(app.pixelsize) # default value
    pixelsize = tk.OptionMenu(app.prefwindow, pixsizes, 2,4,6,8,10,12,14,16,command= lambda x:chgPixelSize(pixsizes,app))
    pixelsize.grid(row=0, column=1, sticky=tk.W)
  
    sprXSizelabel = tk.Label(app.prefwindow, text="Sprite width in pixels")
    sprXSizelabel.grid(row=1, sticky=tk.W)
    sprXSizes = tk.StringVar(app.prefwindow)
    sprXSizes.set(app.spritexsize) # default value
    sprXSize = tk.OptionMenu(app.prefwindow, sprXSizes, 8,16,command= lambda x:chgSprXSize(sprXSizes,app))
    sprXSize.grid(row=1, column=1, sticky=tk.W)

    sprYSizelabel = tk.Label(app.prefwindow, text="Sprite height in pixels")
    sprYSizelabel.grid(row=2, sticky=tk.W)
    sprYSizes = tk.StringVar(app.prefwindow)
    sprYSizes.set(app.spriteysize) # default value
    sprYSize = tk.OptionMenu(app.prefwindow, sprYSizes, 8,16,command= lambda x:chgSprYSize(sprXSizes,app))
    sprYSize.grid(row=2, column=1, sticky=tk.W)
 
    nbrSpriteslabel = tk.Label(app.prefwindow, text="Number of sprites for new project")
    nbrSpriteslabel.grid(row=3, sticky=tk.W)
    nbrSprites = tk.Entry(app.prefwindow)
    nbrSprites.grid(row=3, column=1, sticky=tk.W)

    #    applybutton = Button (app.prefwindow,"Apply",command= lambda:applyPrefs(app)).grid(row=10)
    
    app.prefwindow.withdraw()
    #scrollbar = tk.Scrollbar(app.spwindow, command=closeSprites(app))
    #scrollbar.pack(side=tk.RIGHT, fill='y')
    
def showPreferences(app):
    createPreferencesWindow(app)   
    app.prefwindow.deiconify()

    
def closePreferencesWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.prefwindow.destroy()


def closePaletteWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.palwindow.destroy()

def closeAnimationWindow(app):
    #Destroy sprite window so next time it is open it is reinitialized
    app.animWindow.destroy()

def isColorInPalette(app,color,extended):
    
    iscolorinpalette = False
    idx = findColor (color,app.palette,extended)
    if idx != -1:
        iscolorinpalette = True
    return iscolorinpalette

    
def displayPalette(app):
    
    skip = False
    if (app.paletteCanvas == None):
        skip = True
    if not skip:
        if app.paletteCanvas.winfo_exists()!=0:
            return 1
    app.paletteColorBoxes = []
    numColors= len(app.palette)
    maxColorsPerRow = int(math.ceil(config.paletteWxSize/config.paletteColorBoxSize))
    numRows = int (math.ceil(numColors/maxColorsPerRow))
    paletteWySize = numRows*config.paletteColorBoxSize
    createPaletteWindow (app,paletteWySize)
    app.paletteCanvas = tk.Canvas (app.palwindow,width=config.paletteWxSize,height=paletteWySize)
    app.paletteCanvas.bind('<Button-1>', lambda x:updateDrawColor(app.paletteCanvas,app))
    app.paletteCanvas.bind('<Button-3>', lambda x:swapColor(app.paletteCanvas,app))
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
                app.paletteColorBoxes.append(app.paletteCanvas.create_rectangle (x,y,dx,dy,fill=boxColor,tag=str(color)))
                x = x + config.paletteColorBoxSize
        x = 1
        y = y + config.paletteColorBoxSize
    app.paletteCanvas.pack()
    app.palwindow.deiconify()

    
def colorCompare(colora,colorb,extended):
    ra=int(colora[0])
    ga=int(colora[1])
    ba=int(colora[2])
    rb=int(colorb[0])
    gb=int(colorb[1])
    bb=int(colorb[2])
    weight = 0
    if (ra==rb) and (ga==gb) and (ba==bb):
        weight = weight + 30
    if extended:
        if (abs(ra-rb)==1) and (ga==gb) and (ba==bb):
            weight = weight + 10
        if (ra==rb) and (abs(ga-gb)==1) and (ba==bb):
            weight = weight + 10
        if (ra==rb) and (abs(ba-bb)==1) and (ga==gb):
            weight = weight + 10
        if abs(ra-rb)==1 and abs(ga-gb)==1 and abs(ba-bb)==1:
            weight = weight+ 20
        if abs(ra-rb)==1 and abs(ga-gb)==1 and (ba==bb):
            weight = weight+ 5
        if abs(ra-rb)==1 and abs(ba-bb)==1 and (ga==gb):
            weight = weight+ 5
        if abs(ga-gb)==1 and abs(ba-bb)==1 and (ra==rb):
            weight = weight+ 2
        if (abs(ra-rb)==2) and (ga==gb) and (ba==bb):
            weight = weight+ 4
        if (ra==rb) and (abs(ga-gb)==2) and (ba==bb):
            weight = weight+ 4
        if (ra==rb) and (abs(ba-bb)==2) and (ga==gb):
            weight = weight+ 4
        if abs(ra-rb)==2 and abs(ga-gb)==2 and abs(ba-bb)==2:
            weight = weight+ 1
        if abs(ra-rb)==2 and abs(ga-gb)==2 and (ba==bb):
            weight = weight+ 1
        if abs(ra-rb)==2 and abs(ba-bb)==2 and (ga==gb):
            weight = weight+ 1
        if abs(ga-gb)==2 and abs(ba-bb)==2 and (ra==rb):
            weight = weight+ 1
        # Special case, if 3 colors are equal to each other then add extra points
        if (rb==gb) and (gb==bb) and (ra==ga) and (ga==ba):
            weight = weight +1 
            
    return weight

def findColor(color,palette,extended):
    idx = 0
    cw = 0
    retcol = -1
    if len(palette)>0:
        for pcolor in palette:
            weight = colorCompare(color,pcolor,extended)
            if weight > cw:
                cw = weight
                retcol = idx
            idx = idx + 1
    return retcol

