import retrofunctions
import config
import tkinter as tk

def Screen2 (app,file,filename):
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

 
def Screen5 (app,file,filename):
    header = [254,0,0,255,105,0,0]  
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
    
def Screen3 (app,file,filename):
    # In this case we know taht the tiles are 2 by 2, each tile will end up being something like:
    # 4bits-> Color A + 4bits -> Color B
    # 4bits-> Color C + 4bits -> Color D
    
    header = [254,0,0,255,7,0,0]  
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
    
    
def Screen4 (app,file,filename):
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
    
def Screen6 (app,file,filename):
    header = [254,0,0,255,105,0,0]
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

def Screen7 (app,file,filename):
    header = [254,0,0,255,211,0,0]  
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
 