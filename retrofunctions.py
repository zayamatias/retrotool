import pickle
import PIL.Image
import PIL.ImageTk
import config
import tkinter as tk
import math
import sprites

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

def exportMSXScreen(app):
    header = [254,0,0,255,105,0,0]
    filebytes = bytearray(header)
    outfile = tk.filedialog.asksaveasfilename(parent=app.root,filetypes=[("Screen Files","*.sc2;*.sc5")])
    #extension = outfile[len(app.opfile)-3:]
    f = open(outfile, 'wb')
    # First write the tiles themselves
    """
    for tile in app.TileMap:
        thistile = app.FinalTiles[tile]
        for row in thistile.pattern:
            byte = int(row, 2)
            filebytes.append(byte)
    # Then write the colors
        totalbytes
    nibbc = 0
    for tile in app.TileMap:
        thistile = app.FinalTiles[tile]
        colors = thistile.colors
        pattern = thistile.pattern
        for row in pattern:
            idx = 0
            for bit in row:
                fgcolor = (int(colors[idx]) & 240) >> 4
                bgcolor = int(colors[idx]) & 15
                idx = idx + 1
                if nibbc == 0:
                    if bit == 1:
                        byte = fgcolor
                    else:
                        byte = bgcolor
                    byte = byte << 4
                else:
                    if bit == 1:
                        byte = byte | fgcolor
                    else:
                        byte = byte | bgcolor
                nibbc = nibbc +1 
                if nibbc == 2:
                    filebytes.append(byte)
                    nibbc = 0
                    print (byte)
    
    """
    cols = 32
    rows = 27
    nibbc = 0
    for trow in range (0,rows):
        for row in range (0,app.tileysize):
            for tcol in range (0,cols):
                tileidx =(trow*cols)+tcol
                try:
                    tile = app.ColorTiles[tileidx]
                except:
                    tile = ['0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0','0%0%0%0%0%0%0%0']
                cpattern = tile[row].split("%")
                if cpattern [0] == "":
                    del cpattern[0]
                for col in range (0,app.tilexsize):
                    bit =  cpattern[col]
                    if bit !="":
                        bit =  int(cpattern[col]) & 15
                        msbcolor = bit << 4
                        lsbcolor = bit 
                        if nibbc == 0:
                            byte = msbcolor
                        else:
                            byte = byte | lsbcolor
                        nibbc = nibbc +1 
                        if nibbc == 2:
                            filebytes.append(byte)
                            nibbc = 0
    f.write(filebytes)
    ## Output palette to console in BASIC mode for testing purposes
    idx = 0
    bgcolor = "0"
    for color in app.palette:
        if colorCompare (app.bgcolor,color):
              bgcolor = str(idx)     
        idx = idx +1
    print ("10 SCREEN 5:COLOR 15,"+bgcolor+","+bgcolor)
    line1 = "20 DATA 0,0,0"
    line2 = "\n30 DATA "
    idx = 0
    for color in app.palette:
        if idx == 0:
            print (line1, end="")
        if idx == 8:
            print (line2, end="")
        if idx > 0:
            if idx == 8:
                print (str(color[0])+","+str(color[1])+","+str(color[2]), end="")
            else:
                print (","+str(color[0])+","+str(color[1])+","+str(color[2]), end="")
                
        idx = idx +1
    print ("\n40 FOR C=0 TO 15:READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = outfile.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")

def exportASMFile(app):

    #do the actual saving of the file
    """if app.usprites == []:
        messagebox.showinfo("Error","Please, click on the background color of the image first")
        return 1
    """
    app.outfile = tk.filedialog.asksaveasfilename(parent=app.root)
    writeASMFile(app)

    
def resetProject(app):
        app.projfile =""
        # Objects to be saved/loaded to/from project file
        app.pixels = []
        app.finalsprites = []
        app.usprites = []
        app.csprites = []
        app.bgcolor = (-1,-1,-1)
        app.palette=config.palettes[app.targetSystem][2]
        app.imgwidth = 0
        app.imgheight = 0
        app.sprImgOffset = 0
        app.tileImgOffset = 0
        app.TileMap = []


def openROMFile(app):
    app.romfile = tk.filedialog.askopenfilename(parent=app.root,filetypes=[("ROM Files","*.rom;*.nes;*.sms;*.sr5")])
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
        app.opfile = tk.filedialog.askopenfilename(parent=app.root,filetypes=[("Image Files","*.jpg;*.gif;*.png;*.bmp")])
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
            app.projfile = tk.filedialog.asksaveasfilename(parent=app.root,filetypes=[("Project Files","*.prj")])

    with open(app.projfile,"wb") as f:
        pickle.dump ((app.imgwidth,app.imgheight,app.pixels,app.finalsprites,app.usprites,app.csprites,app.palette),f,pickle.HIGHEST_PROTOCOL)
    
def loadProject (app):
    loadprojfile = tk.filedialog.askopenfilename(parent=app.root,filetypes=[("Project Files","*.prj")])
    if (loadprojfile!=""):
        resetProject(app)
        app.projfile = loadprojfile
        try:
            with open(app.projfile,"rb") as f:
                (app.imgwidth,app.imgheight,app.pixels,app.finalsprites,app.usprites,app.csprites,app.palette)=pickle.load(f)
        except:
            tk.messagebox.showinfo("Error","The file you tried to open is not compatible")

            
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
    app.colors = app.img.getcolors()
    if (app.colors==None):
        app.colors = [(0,0,0)]*255
    numcolors = len(app.colors)
    if numcolors > (config.syslimits[app.targetSystem][2] -1) :
        tk.messagebox.showinfo("Error","Max number of colors exceeded ("+str(numcolors)+" instead of "+str(app.maxcolors)+")")
        return False
    else:
        return True

def checkSize(app):
    #check if the colors of the image are within the limits of the system
    width = app.imgwidth
    if (width/app.spritexsize) != int (width/app.spritexsize):
        tk.messagebox.showinfo("Error","Image width is not a multiple of sprite width ( currently set in config to "+str(app.spritexsize)+"px)")
        return False
    else:
        return True
def getColors(app):
    #get the system colors (needs to be generic, not yet done I believe)
    #app.palette =[app.bgcolor]
    for color in app.colors:
        rgb = color[1]
        if not (isinstance( rgb, int )):
            r=int(int(rgb[0])/config.palettes[app.targetSystem][1])
            g=int(int(rgb[1])/config.palettes[app.targetSystem][1])
            b=int(int(rgb[2])/config.palettes[app.targetSystem][1])
            # make sure we do not add bgcolor
            if set((r,g,b)) != set (app.bgcolor):
               if not isColorInPalette (app,(r,g,b)):
                   if app.paletteIndex>(len(app.palette)-1):
                       app.palette.append((r,g,b))
                   else:  
                       app.palette[app.paletteIndex]=(r,g,b)
            app.paletteIndex = app.paletteIndex + 1
    app.paletteIndex = 0

def getPixels (app,pixelArray):
    #Read all the pixels and colorsin the image
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
            pixel = app.img.getpixel((x,y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            color = (int(r/config.palettes[app.targetSystem][1]),int(g/config.palettes[app.targetSystem][1]),int(b/config.palettes[app.targetSystem][1]))
            if set(color) != set(app.bgcolor): # color chosen by user
                #pattern is created either with a ZERO or the index of the color in the palette (1,2,3,4....max colors of the system)
                index = paletteIndex(app,color)
                if index >= 0:
                    pixelArray.append(index)
                else:
                    if index == -1: #Add color to palette
                        app.palette.append(color)
                        index = paletteIndex(app,color)
                        pixelArray.append(index)
                    else:
                        pixelArray.append('0')
            else:
                    pixelArray.append('0')
        for x in range (0,extracols):
                pixelArray.append('0')
    app.imgwidth= app.imgwidth+extracols
    app.prcanvas.pack_forget()
    app.progress['value']=0
def paletteIndex(app,color):
    index = 0
    for palColor in app.palette:
        if (colorCompare(color,palColor)) and (index != 0):
            return index
        index = index + 1
    return -1


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
    print (app.targetSystem)
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
    if len(tags)<1:
        return
    app.drawColor = int(tags[0])-1

      
def drawboxel (app,canvas,sprite,x,y,index,width):
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
            #if pxColor != 0:
            color = transformColor (app,pxColor)
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
            canvas.create_rectangle (x,y,ex,ey,fill=color,tag=str(index)+"/"+str(px)+"/"+str(py),width=border)
            #else:
                # In the "tag" directive I save the sprite_index/x_coord/y_coord of the "boxel"
            #    canvas.create_rectangle (x,y,ex,ey,fill=app.spriteeditorbgcolor,tag=str(index)+"/"+str(px)+"/"+str(py),width=border)

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

def isColorInPalette(app,color):
    
    iscolorinpalette = False
    for palColor in app.palette:
        if colorCompare (color,palColor):
            iscolorinpalette = True
    return iscolorinpalette
    
    
def displayPalette(app):
    
    skip = False
    if (app.paletteCanvas == None):
        skip = True
    if not skip:
        if app.paletteCanvas.winfo_exists()!=0:
            return 1
    numColors= len(app.palette)
    maxColorsPerRow = int(math.ceil(config.paletteWxSize/config.paletteColorBoxSize))
    numRows = int (math.ceil(numColors/maxColorsPerRow))
    paletteWySize = numRows*config.paletteColorBoxSize
    createPaletteWindow (app,paletteWySize)
    app.paletteCanvas = tk.Canvas (app.palwindow,width=config.paletteWxSize,height=paletteWySize)
    app.paletteCanvas.bind('<Button-1>', lambda x:updateDrawColor(app.paletteCanvas,app))
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
                app.paletteCanvas.create_rectangle (x,y,dx,dy,fill=boxColor,tag=str(color))
                x = x + config.paletteColorBoxSize
        x = 1
        y = y + config.paletteColorBoxSize
    app.paletteCanvas.pack()
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
    if abs(ra-rb)==1 and abs(ga-gb)==1 and abs(ba-bb)==1:
        return True
    if abs(ra-rb)==1 and abs(ga-gb)==1 and (ba==bb):
        return True
    if abs(ra-rb)==1 and abs(ba-bb)==1 and (ga==gb):
        return True
    if abs(ga-gb)==1 and abs(ba-bb)==1 and (ra==rb):
        return True
    return False


