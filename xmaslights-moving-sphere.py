import bpy
import os

coordfilename = os.path.join(os.path.dirname(bpy.data.filepath),"coords.txt")

run = 1

def xmaslight():
    # This is the code from my 
    
    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    import board
    import neopixel
    import re
    import math
    
    # You are welcome to add any of these:
    # import random
    # import numpy
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES (please don't break this bit)
    
    
	
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    
    # YOU CAN EDIT FROM HERE DOWN
    
    # I get a list of the heights which is not overly useful here other than to set the max and min altitudes
    heights = []
    for i in coords:
        heights.append(i[2])
    
    min_alt = min(heights)
    max_alt = max(heights)
    
    # VARIOUS SETTINGS
    
    #the centre point of the moving sphere within which the lights will glow
    centre = [0,0,0]

    #the radius of the moving sphere
    rad = 160

    #wether the sphere is moving up or not (in which case it is moving down)
    up = True

    #wether the radius of the sphere is going up or not (in which case it is going down) as signified by a 5 or a -5
    Up = 5

    # pause between cycles (normally zero as it is already quite slow)
    slow = 0
    
    # the two colours in GRB order
    # if you are turning a lot of them on at once, keep their brightness down please
    colourA = [50,50,50] # grey
    colourB = [0,0,0] # off
    



    # yes, I just run which run is true
    while run == 1:
        

        time.sleep(slow)
        
        #this tests if the given led in within the range of the sphere and sets it to either off(colourB) or on with some cycling colour(colourA)
        LED = 0
        while LED < len(coords):
            if rad**2 >= (coords[LED][0]-centre[0])**2 + (coords[LED][1]-centre[1])**2 + (coords[LED][2]-centre[2])**2:
                pixels[LED] = colourA
            else:
                pixels[LED] = colourB
            LED += 1
        

        #this code determines the direction to move the sphere in
        if up == True and centre[2] >= int((0.66 * float(max_alt))+0.5):
            up = False
        elif up == False and centre[2] <= int((0.66 * float(min_alt))+0.5):
            up = True
        
	#this is the code that moves the sphere of lights
        if up == True:
            centre[2] += 10
        else:
            centre[2] -= 10
	
	#this code inflates and shrinks a moving sphere of lights
        rad += Up
        if(rad>=250):
            Up=-5
        elif(rad<=75):
            Up=5

        # here I cycle through the different colours, the  transition is not always smooth but it gets the job done
        colourA[2]+=5
        if(colourA[2]>100):
            colourA[2] = 0
            colourA[1] += 5
            if(colourA[1]>100):
                colourA[1] = 0
                colourA[0] += 5
                if(colourA[0]>100):
                    colourA[0] = 0

        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        pixels.show()
        
        
        
    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()
