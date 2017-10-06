iconfile = "MSX.ICO"
logoimage = "MSX-Logo.png"
appxsize = 800
appysize = 600
tooltitle = "MSX Retro Tool"
transcolor = ('0','0','0')
msxcolordivider = 32
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
(255/msxcolordivider,255/msxcolordivider,255/msxcolordivider)]
palettes = [("MSX",msxcolordivider,[msxpalette]),("MSX2",msxcolordivider,[msxpalette]),("MSX2+",msxcolordivider,[msxpalette])]
systems = ["MSX","MSX2","MSX2+"]
#syslimits => System name, max colors per sprite
syslimits = [("MSX",1,16),("MSX2",3,16),("MSX2+",3,16)]
pixelsize = 8
spritesperrow= 6
default_filename ="C:\\Users\\id087082\\Downloads\\kv2.png" # set it to a default file or leave it blank to have dialog opened
spriteeditorbgcolor = "white"