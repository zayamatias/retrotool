import retrofunctions
import config
import tkinter as tk


def NeoSprites (app,filename):
    # the NeoGeo sprites have 4 8x8 pixel blocks, each pixel has 4 bits
    evenbytes = []
    oddbytes = []
    for sprite in app.usprites:
        tiles = [[],[],[],[]]
        # Create Tiles for sprites [3-1 && 4-2]
        ypos = 0;
        for row in sprite:
            pixpattern = row.split("%")
            pixpattern.remove('')
            xpos = 0
            for col in range (0,app.spritexsize):
                if xpos < 8 and ypos <8:
                    tiles[2].append(pixpattern[col])
                if xpos < 8 and ypos >7:
                    tiles[0].append(pixpattern[col])
                if xpos < 8 and ypos >7:
                    tiles[3].append(pixpattern[col])
                if xpos >7 and ypos >7:
                    tiles[1].append(pixpattern[col])
                xpos = xpos + 1
            xpos = 0
            ypos = ypos + 1
        for tile in tiles:
            tpos = 0
            for row in range (0,8):
                bitplane0 = 0
                bitplane1 = 0
                bitplane2 = 0
                bitplane3 = 0
                for col in range (0,8):
                    bitplane0 = bitplane0 << 1
                    bitplane1 = bitplane1 << 1
                    bitplane2 = bitplane2 << 1
                    bitplane3 = bitplane3 << 1
                    color = int(tile[col+tpos])
                    bp0 = color & 1
                    bp1 = (color & 2) >> 1
                    bp2 = (color & 4) >> 2
                    bp3 = (color & 8) >> 3
                    bitplane0 = bitplane0 | bp0
                    bitplane1 = bitplane1 | bp1
                    bitplane2 = bitplane2 | bp2
                    bitplane3 = bitplane3 | bp3
                tpos = tpos + 8 
                evenbytes.append(bitplane0)
                evenbytes.append(bitplane1)
                oddbytes.append(bitplane2)
                oddbytes.append(bitplane3)
        print (len(evenbytes))
        f = open(filename, 'wb')

    
def NeoFixed (app,file,filename):

    # Below the order in which the columns should be stored
    # Check https://wiki.neogeodev.org/index.php?title=Fix_graphics_format
    colSwap = [2,3,0,1]
    bytecount = 0;
    filebytes =bytearray()
    for tile in app.Tiles:
        tileInBytes =[[],[],[],[]]
        pixpos = 0;
        for row in range(0,app.tileysize):
            pixpattern = tile[row].split("%")
            pixpattern.remove('')
            #So logic here:
            #if the pixel we're checking is even > 2 then we have to store the byte
            #otherwise we just shift to the proper position
            pixpos = 0 # The pixle in te row
            currentCol = 0
            byte = 0
            for col in range(0,app.tilexsize):
                if pixpos % 2 == 0:
                    #even number
                    byte = int(pixpattern[pixpos])
                else:
                    #odd number
                    byte = byte | (int(pixpattern[pixpos]) <<4)
                    tileInBytes[colSwap[currentCol]].append(byte)
                    byte = 0
                    bytecount = bytecount + 1
                    currentCol = currentCol + 1
                pixpos = pixpos + 1
        #In tilebytes we now have the complete tyle, we can now save it to the binaryfile, splitted in 4 columns
        for n in range (0,len(tileInBytes)):
            for byte in tileInBytes[n]:
                filebytes.append(byte)
    file.write(filebytes)

def Screen2 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,55,0,0]
        #header = header + ([0]*249)
        headerbytes = bytearray(header)
        errors = False
        file.write(headerbytes)
    filebytes = bytearray()
    writtenbytes = 0
    colorbytes = bytearray()
    for tile in app.Tiles:
        for row in range(0,app.tileysize):
            cpattern = tile[row].split("%")
            if cpattern [0] == "":
                del cpattern[0]
            tilecols = list(set(cpattern))
            if len(tilecols)==1:
                tilecols.append(tilecols[0])
                tilecols[0]=0
            if len(tilecols)>2:
                errors = True
            if len(tilecols)==0:
                tilecols.append(0)
                tilecols.append(0)
            byte =""    
            colorbyte = (int(tilecols[1])<<4) | int(tilecols[0])
            for col in range (0,app.tilexsize):
                if int(cpattern[col])==int(tilecols[0]):
                    byte = byte+"0"
                else:
                    byte = byte+"1"
            filebytes.append(int(byte,2))
            colorbytes.append(colorbyte)
    for x in range (0,3):
        file.write(filebytes)
        for wbyte in range (2048-len(filebytes)):
            file.write(bytearray([0]))
    for x in range (0,768):
        try:
            file.write(bytearray([app.TileMap[x]]))
        except:
            file.write(bytearray(0))
    for wbyte in range (writtenbytes,1280):
        file.write(bytearray([0]))
    for x in range (0,3):
        file.write(colorbytes)
        for wbyte in range (len(colorbytes),2048):
            file.write(bytearray([0]))
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    print ("10 SCREEN 2:COLOR 15,"+bgcolor+","+bgcolor)
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("20 BLOAD \""+filename+"\",S")
    print ("30 GOTO 30")
    if errors:
        tk.messagebox.showinfo("Warning","Some lines of patterns in your image contained more than 2 colors, results might not be what you expect!")
        return 1        

 
def Screen5 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,105,0,0]  
    else:
        header = []
    filebytes = bytearray(header)
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
    file.write(filebytes)
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
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
    print ("\n40 FOR C=0 TO ",len(app.palette)-1,":READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")
    
def Screen3 (app,file,filename,wHeader=True):
    # In this case we know taht the tiles are 2 by 2, each tile will end up being something like:
    # 4bits-> Color A + 4bits -> Color B
    # 4bits-> Color C + 4bits -> Color D
    
    if wHeader:
        header = [254,0,0,255,7,0,0]  
    else:
        header = []
    filebytes = bytearray(header)
    memorypos = 0
    offset = 0
    for blocks in range(6):
        for col in range (0,32):
            for row in range (0,4):
                tileID = (row*32)+col+offset
                tile = app.Tiles[app.TileMap[tileID]]
                b1pattern = tile[0].split("%")
                if b1pattern[0] == "":
                        del b1pattern[0]
                b2pattern = tile[1].split("%")
                if b2pattern[0] == "":
                        del b2pattern[0]
                byte = (int(b1pattern[0])<<4) | int(b1pattern[1])
                filebytes.append(byte)
                byte = (int(b2pattern[0])<<4) | int(b2pattern[1])
                filebytes.append(byte)
                memorypos = memorypos+2
        offset = offset + (128)
    file.write(filebytes)
    for wbyte in range (2048-len(filebytes)):
        file.write(bytearray([0]))
        memorypos = memorypos+1
    for wbyte in range (2048-memorypos):
        file.write(bytearray([0]))
        memorypos = memorypos+1
    for x in range (0,768):
        try:
            file.write(bytearray([app.TileMap[x]]))
            memorypos = memorypos+1
        except:
            file.write(bytearray(0))
    for wbyte in range (16384-memorypos):
        file.write(bytearray([0]))
        memorypos = memorypos+1
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    print ("10 SCREEN 3:COLOR 15,"+bgcolor+","+bgcolor)
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
    print ("\n40 FOR C=0 TO ",len(app.palette)-1,":READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")
    
    
def Screen4 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,55,0,0]
    else:
        header = []
    #header = header + ([0]*249)
    headerbytes = bytearray(header)
    errors = False
    file.write(headerbytes)
    filebytes = bytearray()
    writtenbytes = 0
    colorbytes = bytearray()
    for tile in app.Tiles:
        for row in range(0,app.tileysize):
            cpattern = tile[row].split("%")
            if cpattern [0] == "":
                del cpattern[0]
            tilecols = list(set(cpattern))
            if len(tilecols)==1:
                tilecols.append(tilecols[0])
                tilecols[0]=0
            if len(tilecols)>2:
                errors = True
            if len(tilecols)==0:
                tilecols.append(0)
                tilecols.append(0)
            byte =""    
            colorbyte = (int(tilecols[1])<<4) | int(tilecols[0])
            for col in range (0,app.tilexsize):
                if int(cpattern[col])==int(tilecols[0]):
                    byte = byte+"0"
                else:
                    byte = byte+"1"
            filebytes.append(int(byte,2))
            colorbytes.append(colorbyte)
    for x in range (0,3):
        file.write(filebytes)
        for wbyte in range (2048-len(filebytes)):
            file.write(bytearray([0]))
    for x in range (0,768):
        try:
            file.write(bytearray([app.TileMap[x]]))
        except:
            file.write(bytearray(0))
    for wbyte in range (writtenbytes,1280):
        file.write(bytearray([0]))
    for x in range (0,3):
        file.write(colorbytes)
        for wbyte in range (len(colorbytes),2048):
            file.write(bytearray([0]))
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    print ("10 SCREEN 4:COLOR 15,"+bgcolor+","+bgcolor)
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
    print ("\n40 FOR C=0 TO ",len(app.palette)-1,":READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")
    
def Screen6 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,105,0,0]
    else:
        header = []
    #header = header + ([0]*249)
    headerbytes = bytearray(header)
    file.write(headerbytes)
    filebytes = bytearray()
    for tile in app.TileMap:
        for row in range(0,app.tileysize):
            cpattern = app.Tiles[tile][row].split("%")
            if cpattern [0] == "":
                del cpattern[0]
            tilecols = cpattern
            colorbyte = (int(tilecols[0])<<6) |(int(tilecols[1])<<4) |(int(tilecols[2])<<2) | int(tilecols[3])
            filebytes.append(colorbyte)
    file.write(filebytes)
    for wbyte in range ((16*1024)-len(filebytes)):
        file.write(bytearray([0]))
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    print ("10 SCREEN 6:COLOR 15,"+bgcolor+","+bgcolor)
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
    print ("\n40 FOR C=0 TO ",len(app.palette)-1,":READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")

def Screen7 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,211,0,0]
    else:
        header=[]
    filebytes = bytearray(header)
    cols = 64
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
    file.write(filebytes)
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    print ("10 SCREEN 7:COLOR 15,"+bgcolor+","+bgcolor)
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
    print ("\n40 FOR C=0 TO ",len(app.palette)-1,":READ R,G,B:COLOR=(C,R,G,B):NEXT")
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("50 BLOAD \""+filename+"\",S")
    print ("60 GOTO 60")

def Screen8 (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,211,0,0]
    else:
        header =[]
    filebytes = bytearray(header)
    cols = 32
    rows = 27
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
                        color = app.palette[int(bit)]
                        if set(color)==set((-1,-1,-1)):
                            color = app.bgcolor
                        byte = color[1]<<5 | color[0]<<2 | color[2]
                        if (byte != 0 and byte != 255):
                            print (color,byte)                        
                        filebytes.append(byte)
                            
    file.write(filebytes)
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("10 SCREEN 8:COLOR 15,"+bgcolor+","+bgcolor)
    print ("20 BLOAD \""+filename+"\",S")
    print ("30 GOTO 30")

def Screen10plus (app,file,filename,wHeader=True):
    if wHeader:
        header = [254,0,0,255,211,0,0]  
    else:
        header = []
    filebytes = bytearray(header)
    cols = 32
    rows = 27
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
                # SPecial case for MSX screens, we take the two bytes of the tile and calculate colors
                # according to 4bits
                for byte in range (2): # Take two bytes at a time
                    bits = [cpattern[(byte*4)+0],cpattern[(byte*4)+1],cpattern[(byte*4)+2],cpattern[(byte*4)+3]] 
                    colors = []
                    for idx in range (4):
                        bit =  bits[idx]
                        if bit !="":
                            color = app.palette[int(bit)]
                            if set(color)==set((-1,-1,-1)):
                                color = app.bgcolor
                            colors.append(color)   
                    print (colors)    
                    r = int((colors[0][0]+colors[1][0]+colors[2][0]+colors[3][0])/4)
                    g = int((colors[0][1]+colors[1][1]+colors[2][1]+colors[3][1])/4)
                    b = int((colors[0][2]+colors[1][2]+colors[2][2]+colors[3][2])/4)
                    y =int( b/2 + r/4 + g/8)
                    j = int( r - y)
                    k = int(g - y)
                    y1 = int(colors[0][2]/2 + colors[0][0]/4 + colors[0][1]/8)
                    y2 = int(colors[1][2]/2 + colors[1][0]/4 + colors[1][1]/8)
                    y3 = int(colors[2][2]/2 + colors[2][0]/4 + colors[2][1]/8)
                    y4 = int(colors[3][2]/2 + colors[3][0]/4 + colors[3][1]/8)
                    k = k & 63
                    kh = k >> 3
                    kl = k & 7
                    j = j & 63
                    jh = j >> 3
                    jl = j & 7
                    byte1 = y1 << 4 | kl 
                    byte2 = y2 << 4 | kh 
                    byte3 = y3 << 4 | jl 
                    byte4 = y4 << 4 | jh 
                    """#FOr some reason sometimes the calculations go below 0
                    if byte1 < 0:
                        byte1 = 0
                    if byte2 < 0:
                        byte2 = 0
                    if byte3 < 0:
                        byte3 = 0
                    if byte4 < 0:
                        byte4 = 0
                    """
                    try:
                        filebytes.append(byte1)
                        filebytes.append(byte2)
                        filebytes.append(byte3)
                        filebytes.append(byte4)
                    except:
                        print (byte1,byte2,byte3,byte4)
                        exit
    file.write(filebytes)
    ## Output palette to console in BASIC mode for testing purposes
    bgcolor = str(retrofunctions.findColor (app.bgcolor,app.palette,config.syslimits[app.targetSystem.get()][4]))
    if bgcolor == "-1":
        bgcolor = "0"
    filesplit = filename.split("/")
    filename = filesplit[len(filesplit)-1]
    print ("10 SCREEN 8:COLOR 15,"+bgcolor+","+bgcolor)
    print ("20 BLOAD \""+filename+"\",S")
    print ("30 GOTO 30")
 