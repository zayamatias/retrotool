class sprite:
    # Sprite class, to make it easier to manipulate afterwards
    spriteCount = 0

    def __init__ (self,pattern,colors,ored,x,y):

        self.pattern=pattern   #binary pattern of the sprite
        self.colors=colors     #colors of the sprite
        self.ored = ored       #does this sprite come from an ored sprite (for palette purposes)
        self.number = sprite.spriteCount   #Sprite index
        self.x = x          #X location of the sprite according to the original image
        self.y = y          #y location of the sprite according to the original image
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

    def getAsmPattern (self,width):
        #get the pattern of a sprite in ASM mode (db %xxxxxxxxxxxxxxxx)
        #attention: for 16bit sprites, msx splits into 2 8x16 patterns
        line = ""
        rows = self.pattern
        pat1 =""
        pat2 =""
        for row in rows:
            pat1=pat1+"\tdb %"+str(row)[:8]+"\n"
            pat2=pat2+"\tdb %"+str(row)[8:]+"\n"
        line = pat1
        if width > 8:
            line = line + pat2
        return line
    
    def getBasicPattern (self,width):
        #get the pattern of a sprite in ASM mode (db %xxxxxxxxxxxxxxxx)
        #attention: for 16bit sprites, msx splits into 2 8x16 patterns
        linel = []
        liner = []
        rows = self.pattern
        for row in rows:
            linel.append(" DATA "+str(row)[:8]+"\n")
            liner.append(" DATA "+str(row)[8:]+"\n")
        return linel+liner

        
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

    def getBASICColors (self,ysize):
        #get the colors of a sprite in ASM mode (db 1,2,3....) each byte represents the # of the color in the palette
        #for ored colors, bit #7 should be set, thus the +64
        line = ""
        rows = self.colors
        count = 1
        for row in rows:
            if self.ored :
                if (row!=0):
                   row = row + 64
            line = line + "CHR$("+str(row)+")"
            if count < ysize :
                count = count + 1
                line = line + "+"
        line = line + "\n"
        return line

class character:
    # defines a character that wil contains a matrix of sprites
    def __init__ (self,rows,cols):
        self.rows = rows 
        self.cols = cols
        self.sprites = [[0 for x in range(cols)] for y in range(rows)]
                         
    def insertSprite (self,sprite,row,col):
        self.sprites[row][col]=sprite
        
class animation:
    # defines a animation, which is a list of characters to be shown one after the other    
    def __init__ (self):
        self.characters = []
    
    def addCharacter(self,character):
        self.characters.append(character)
        
    def numFrames(self):
        return (len(self.characters))
        
class tile:
    # Tile class, to make it easier to manipulate afterwards
    tileCount = 0

    def __init__ (self,pattern,colors):

        self.pattern=pattern   #binary pattern of the sprite
        self.number = tile.tileCount   #Sprite index
        self.colors=colors     #colors of the sprite
        tile.tileCount = tile.tileCount+1 #add one to the index for next sprite

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

    def getAsmPattern (self,width):
        #get the pattern of a tile in ASM mode (db %xxxxxxxxxxxxxxxx)
        #Normally width is always 8, but let's keep it system agnostic
        line = ""
        rows = self.pattern
        line =""
        for row in rows:
            line = line + "\tdb %"+str(row)+"\n"
        return line

    def getAsmColors (self,ysize):
        #get the colors of a tile in ASM mode
        #things get tricky, 2 colors are saved on a single byte
        #bg color is stored in 4 less significant bits (0000XXXX)
        #fg color is stored in 4 most significant bits (XXXX0000)
        #so final byte is $fgbg
        #I could have done it by simply sticking the values together, but shifting is fun!
        rows = self.colors
        line = "\tdb "
        count = 0
        for row in rows:
            line = line + "$"+"{0:02x}".format(row)
            count = count +1 
            if count < len(rows):
                line = line + ","
        return line