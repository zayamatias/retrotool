iconfile = ""   # File that while show in the window icon
logoimage = "Tool_Logo.png"  #Image to show after opening the app
appxsize = 800   #Width of the main window
appysize = 600   #Height of the main window
tooltitle = "Retro Tool"  #title of the app
transcolor = ('0','0','0') #RGB for color to consider transparent
msxcolordivider = [32,32,32] # Number to use as divider to go from 16bit palette to 7bit msx palette [R,G,B]
msxpalette = [(-1,-1,-1),
(0,0,0),
(int(62/msxcolordivider[0]), int(184/msxcolordivider[1]),int(73/msxcolordivider[2])),
(int(116/msxcolordivider[0]),int(208/msxcolordivider[1]),int(125/msxcolordivider[2])),
(int(89/msxcolordivider[0]),int(85/msxcolordivider[1]),int(224/msxcolordivider[2])),
(int(128/msxcolordivider[0]),int(118/msxcolordivider[1]),int(241/msxcolordivider[2])),
(int(185/msxcolordivider[0]),int(94/msxcolordivider[1]),int(81/msxcolordivider[2])),
(int(101/msxcolordivider[0]),int(219/msxcolordivider[1]),int(239/msxcolordivider[2])),
(int(219/msxcolordivider[0]),int(101/msxcolordivider[1]),int(89/msxcolordivider[2])),
(int(255/msxcolordivider[0]),int(137/msxcolordivider[1]),int(125/msxcolordivider[2])),
(int(204/msxcolordivider[0]),int(195/msxcolordivider[1]),int(94/msxcolordivider[2])),
(int(222/msxcolordivider[0]),int(208/msxcolordivider[1]),int(135/msxcolordivider[2])),
(int(58/msxcolordivider[0]),int(162/msxcolordivider[1]),int(65/msxcolordivider[2])),
(int(183/msxcolordivider[0]),int(102/msxcolordivider[1]),int(181/msxcolordivider[2])),
(int(204/msxcolordivider[0]),int(204/msxcolordivider[1]),int(204/msxcolordivider[2])),
(int(255/msxcolordivider[0]),int(255/msxcolordivider[1]),int(255/msxcolordivider[2]))
] # Msx palette in MSX values
#Neo Geo Palette
neopalette = msxpalette
#Below will hold palettes for different systems
palettes = [("MSX",msxcolordivider,msxpalette),
            ("MSX",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,[(-1,-1,-1),(0,0,0),(0,0,0),(0,0,0)]),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",[32,32,64],[(-1,-1,-1)]),
            ("MSX2+",[16,16,16],msxpalette),
            ("MSX2+",[2.72,2.72,2.18],msxpalette),
            ("MSX2+",[1,1,1],msxpalette),
            ("NeoGeo",[1,1,1],neopalette)]
#Systems of choice, maybe beyond MSX one day?
activeSystems = [0,1,2,3,4,5,6,7,8,9,10]
defaultSystem = 10
systems = ["MSX - Screen 2",
           "MSX - Screen 3",
           "MSX2 - Screen 4",
           "MSX2 - Screen 5",
           "MSX2 - Screen 6",
           "MSX2 - Screen 7",
           "MSX2 - Screen 8",
           "MSX2+ - Screen 10",
           "MSX2+ - Screen 11",
           "MSX2+ - Screen 12",
           "NeoGeo"]
#System Limits =>
#[0]System name
#[1]max colors per sprite
#[2]max colors of image to load
#[3]can add colors to palette
#[4] Can change colors of palette
#[5] override tile width (if not 0, value to use)
#[6] override tile height (if not 0, value to use)

syslimits = [("MSX",1,256,False,False,0,0),
             ("MSX",1,256,False,True,2,2),
             ("MSX2",3,256,False,True,0,0),
             ("MSX2",3,256,False,True,0,0),
             ("MSX2",3,4,False,True,4,1),
             ("MSX2",3,256,True,True,0,0),
             ("MSX2",3,1000000,True,True,0,0),
             ("MSX2+",3,1000000,True,True,0,0),
             ("MSX2+",3,1000000,True,True,0,0),
             ("MSX2+",3,1000000,True,True,0,0),
             ("NeoGeo",15,65536,True,True,8,8)]

extensions = ["SC2","SC3","SC4","SC5","SC6","SC7","SC8","S10","S11","S12"]

preferencesWxSize = 400
preferencesWySize = 400
animWxSize = 400
animWySize = 400
default_filename = ""
paletteWxSize = 256 # Width of the palette window
paletteColorBoxSize= 64 #size x&y of the box of the color in the palettes



## The parameters below should be updatabe via "preferences"
pixelsize = 4 #pixel size on screen for editing purposes (value will be multiplied x & y)
spriteeditorbgcolor = "white" #BG color for the sprite editor.
spritexsize = 16 # default sprite width
spriteysize = 16 #default sprite height
tilexsize = 8 # default sprite width
tileysize = 8 #default sprite height
newSprites = 2 # Number of sprites for new project
tilesPerRow = 10 #int(256/tilexsize)
# Animation Section

animCols = 3 # Number of columns for the sprite animation
animRows = 4 # Number of rows for the sprite animation
animArray = [14,15,16]  # "character" list to show in animation

ROMWidth = 256
tiled_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><map version=\"1.0\" orientation=\"orthogonal\" renderorder=\"right-down\" width=\"__TILESX__\" height=\"__TILESY__\" tilewidth=\"__TILEXSIZE__\" tileheight=\"__TILEYSIZE__\" nextobjectid=\"__NUMTILES__\" backgroundcolor=\"#000000\"> <tileset firstgid=\"1\" name=\"map00_1\" tilewidth=\"__TILEXSIZE__\" tileheight=\"__TILEYSIZE__\" tilecount=\"__NUMTILES__\">  <image source=\"__FILENAME__\" width=\"__IMGWIDTH__\" height=\"__IMGHEIGHT__\"/></tileset> <layer name=\"background\" width=\"__TILESX__\" height=\"__TILESY__\"><data encoding=\"csv\">__TILEMAP__</data></layer></map>"

#Neo geo C ROM max size (in KB)
neoCROMMaxSize = 8
