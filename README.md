# retrotool

Tool to facilitate sprites/grahics manipulation for retro-progarmming on several systems.

Tool should be "runnable" under python in any system supporting "tkinter" library (Win/Linux/MacOS)

(Español mas abajo, Français plus bas)

English
-------

How to:

You have 2 options to work with sprites:

   - Create new project (select number of sprites in preferences firs)
   
   - Open a "sprite sheet" (image with the sprties in it)
	  
	  - Click on the color on the image that will be used as background color (or will be 0 in sprites)
	  - The tool will try to match the colors with the MSX palette or adapt the palette if no close match is found
	  - It will also try to find automatically the OR color for a sprite row with 3 colours
	  
   - Edit sprites:
	  
	  - Open sprite editor window
	  - Select color on palette
	  - Right click on a "boxel" in order to color it (select color 0 to clear boxel)
	  - Use arrow keys on the keyboard to move spritesheet around (for finer placement of original image)
	  
   - Animate Sprites:
   
	  - For the moment you need to edit the config file:
		animCols = 1 # Number of columns for the sprite animation
		animRows = 2 # Number of rows for the sprite animation
		(this will create characters of Cols*Rows for sprite animations)
		animArray = (3,4,3)  # "character" list to show in animation [If you input from an image, it is 0 for the first row first col, then 2 for first row second col and so on...]
		
   - Save projects / load projects allows you to save a complete project and load it again (without loading any image) - changes made to te sprites should also be saved.
   
   - Preferences : Very basic for the moment, check.
   
   - Export asm : Will create an .asm file that will contain (for the moment):
	  
	  - The list of sprites (2 sprites for a character will be created with the ored pixels setted on both)
	  - The colors for each sprite row
	  - The colors for the palette

Español
-------

Prometo traducir pronto


Français
--------

Je promets de faire la traduction bientôt!
