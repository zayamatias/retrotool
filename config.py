iconfile = "MSX.ICO"   # File that while show in the window icon
logoimage = "MSX-Logo.png"  #Image to show after opening the app
appxsize = 800   #Width of the main window
appysize = 600   #Height of the main window
tooltitle = "MSX Retro Tool"  #title of the app
transcolor = ('0','0','0') #RGB for color to consider transparent
msxcolordivider = 32 # Number to use as divider to go from 16bit palette to 7bit msx palette
msxpalette = [(-1,-1,-1),
(0,0,0),
(int(62/msxcolordivider), int(184/msxcolordivider),int(73/msxcolordivider)),
(int(116/msxcolordivider),int(208/msxcolordivider),int(125/msxcolordivider)),
(int(89/msxcolordivider),int(85/msxcolordivider),int(224/msxcolordivider)),
(int(128/msxcolordivider),int(118/msxcolordivider),int(241/msxcolordivider)),
(int(185/msxcolordivider),int(94/msxcolordivider),int(81/msxcolordivider)),
(int(101/msxcolordivider),int(219/msxcolordivider),int(239/msxcolordivider)),
(int(219/msxcolordivider),int(101/msxcolordivider),int(89/msxcolordivider)),
(int(255/msxcolordivider),int(137/msxcolordivider),int(125/msxcolordivider)),
(int(204/msxcolordivider),int(195/msxcolordivider),int(94/msxcolordivider)),
(int(222/msxcolordivider),int(208/msxcolordivider),int(135/msxcolordivider)),
(int(58/msxcolordivider),int(162/msxcolordivider),int(65/msxcolordivider)),
(int(183/msxcolordivider),int(102/msxcolordivider),int(181/msxcolordivider)),
(int(204/msxcolordivider),int(204/msxcolordivider),int(204/msxcolordivider)),
(int(255/msxcolordivider),int(255/msxcolordivider),int(255/msxcolordivider))
] # Msx palette in MSX values
#Below will hold palettes for different systems
palettes = [("MSX",msxcolordivider,msxpalette),
            ("MSX",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2",msxcolordivider,msxpalette),
            ("MSX2+",msxcolordivider,msxpalette),
            ("MSX2+",msxcolordivider,msxpalette),
            ("MSX2+",msxcolordivider,msxpalette)]
#Systems of choice, maybe beyond MSX one day?
activeSystems = [3]
defaultSystem = 3
systems = ["MSX - Screen 2",
           "MSX - Screen 3",
           "MSX2 - Screen 4",
           "MSX2 - Screen 5",
           "MSX2 - Screen6",
           "MSX2 - Screen 7",
           "MSX2 - Screen 8",
           "MSX2+ - Screen 10",
           "MSX2+ - Screen 11",
           "MSX2+ - Screen 12"]
#System Limits => System name, max colors per sprite
syslimits = [("MSX",1,256),
             ("MSX",1,256),
             ("MSX2",3,256),
             ("MSX2",3,256),
             ("MSX2",3,256),
             ("MSX2",3,256),
             ("MSX2",3,256),
             ("MSX2+",3,256),
             ("MSX2+",3,256),
             ("MSX2+",3,256)]
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
tilesPerRow = int(256/tilexsize)
# Animation Section

animCols = 3 # Number of columns for the sprite animation
animRows = 4 # Number of rows for the sprite animation
animArray = [14,15,16]  # "character" list to show in animation

ROMWidth = 256
tiled_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><map version=\"1.0\" orientation=\"orthogonal\" renderorder=\"right-down\" width=\"__TILESX__\" height=\"__TILESY__\" tilewidth=\"__TILEXSIZE__\" tileheight=\"__TILEYSIZE__\" nextobjectid=\"__NUMTILES__\" backgroundcolor=\"#000000\"> <tileset firstgid=\"1\" name=\"map00_1\" tilewidth=\"__TILEXSIZE__\" tileheight=\"__TILEYSIZE__\" tilecount=\"__NUMTILES__\">  <image source=\"__FILENAME__\" width=\"__IMGWIDTH__\" height=\"__IMGHEIGHT__\"/></tileset> <layer name=\"background\" width=\"__TILESX__\" height=\"__TILESY__\"><data encoding=\"csv\">__TILEMAP__</data></layer></map>"
