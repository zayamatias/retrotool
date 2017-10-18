iconfile = "MSX.ICO"   # File that while show in the window icon
logoimage = "MSX-Logo.png"  #Image to show after opening the app
appxsize = 800   #Width of the main window
appysize = 600   #Height of the main window
tooltitle = "MSX Retro Tool"  #title of the app
transcolor = ('0','0','0') #RGB for color to consider transparent
msxcolordivider = 32 # Number to use as divider to go from 16bit palette to 7bit msx palette
msxpalette = [(-1,-1,-1),
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
(int(255/msxcolordivider),int(255/msxcolordivider),int(255/msxcolordivider)),
(0,0,0)
] # Msx palette in MSX values
#Below will hold palettes for different systems
palettes = [("MSX",msxcolordivider,msxpalette),("MSX2",msxcolordivider,msxpalette),("MSX2+",msxcolordivider,msxpalette)]
#Systems of choice, maybe beyond MSX one day?
systems = ["MSX","MSX2","MSX2+"]
#System Limits => System name, max colors per sprite
syslimits = [("MSX",1,16),("MSX2",3,16),("MSX2+",3,16)]
preferencesWxSize = 400
preferencesWySize = 400
animWxSize = 400
animWySize = 400
default_filename = ""
paletteWxSize = 256 # Width of the palette window
paletteColorBoxSize= 64 #size x&y of the box of the color in the palettes


## The parameters below should be updatabe via "preferences"
pixelsize = 8 #pixel size on screen for editing purposes (value will be multiplied x & y)
spriteeditorbgcolor = "white" #BG color for the sprite editor.
spritexsize = 16 # default sprite width
spriteysize = 16 #default sprite height
newSprites = 2 # Number of sprites for new project
animCols = 1 # Number of columns for the sprite animation
animRows = 2 # Number of rows for the sprite animation
animArray = (3,4,3)  # "character" list to show in animation

