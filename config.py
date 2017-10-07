iconfile = "MSX.ICO"   # File that while show in the window icon
logoimage = "MSX-Logo.png"  #Image to show after opening the app
appxsize = 800   #Width of the main window
appysize = 600   #Height of the main window
tooltitle = "MSX Retro Tool"  #title of the app
transcolor = ('0','0','0') #RGB for color to consider transparent
msxcolordivider = 32 # Number to use as divider to go from 16bit palette to 7bit msx palette
msxpalette = [(62/msxcolordivider, 184/msxcolordivider,73/msxcolordivider),
(116/msxcolordivider,208/msxcolordivider,125/msxcolordivider),
(89/msxcolordivider,85/msxcolordivider,224/msxcolordivider),
(128/msxcolordivider,118/msxcolordivider,241/msxcolordivider),
(185/msxcolordivider,94/msxcolordivider,81/msxcolordivider),
(101/msxcolordivider,219/msxcolordivider,239/msxcolordivider),
(219/msxcolordivider,101/msxcolordivider,89/msxcolordivider),
(255/msxcolordivider,137/msxcolordivider,125/msxcolordivider),
(204/msxcolordivider,195/msxcolordivider,94/msxcolordivider),
(222/msxcolordivider,208/msxcolordivider,135/msxcolordivider),
(58/msxcolordivider,162/msxcolordivider,65/msxcolordivider),
(183/msxcolordivider,102/msxcolordivider,181/msxcolordivider),
(204/msxcolordivider,204/msxcolordivider,204/msxcolordivider),
(255/msxcolordivider,255/msxcolordivider,255/msxcolordivider)] # Msx palette in MSX values
#Below will hold palettes for different systems
palettes = [("MSX",msxcolordivider,[msxpalette]),("MSX2",msxcolordivider,[msxpalette]),("MSX2+",msxcolordivider,[msxpalette])]
#Systems of choice, maybe beyond MSX one day?
systems = ["MSX","MSX2","MSX2+"]
#System Limits => System name, max colors per sprite
syslimits = [("MSX",1,16),("MSX2",3,16),("MSX2+",3,16)]
pixelsize = 8 #pixel size on screen for editing purposes (value will be multiplied x & y)
spritesperrow= 4 # How many sprites to show per row by default
                 # application will calculate according to screen size
default_filename ="C:\\Users\\Matias\\Documents\\MSX\\sprites\\ebike.png" # set it to a default file or leave it blank to have dialog opened
spriteeditorbgcolor = "white" #BG color for the sprite editor.
spritexsize = 16 # default sprite width
spriteysize = 16 #default sprite height