'''
My little Python script for minesweeper
'''

import random
from github import Github # PyGithub
import os

# Get the access token
myaccesstoken = os.environ['MYACCESSTOKEN']

# Read the game state file
gamestatefile = open("minesweeper_readme/gamedata.txt", "r")
gamedata = gamestatefile.read()
gamestatefile.close()

gamedata = gamedata.split("\n") # Split lines

'''
Some thing to note about the gamedata.txt format (note to myself :D):
o: mine
P: Flag

You don't need to care about this, gamedata.txt is just something like (if you want to know):
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
[0,0,0,0,0,0,0,0]
True
False
[]
[]

The reason why it isn't shown here because it has all the information about where is mines, so you will
no it and then...cheating. What about me? Well... :D
'''

def re_generate():
    # Re-generate the game
    print("Re-generating the game table...")
    gametable = []
    
    # Create blank table
    print("Creating game table...")
    for x in range(8):
        gametable.append([]) # Add new row
        for y in range(8):
            gametable[x].append(0) # Add new coloumn
    
    # Create mines: 10 mines
    print("Creating mines...")
    for i in range(10):
        mineloc = random.randint(0,64)
        while gametable[mineloc//8][mineloc%8] == "o":
            # If has a mine on that place -> Re-random a new place
            mineloc = random.randint(0,64)
        # Blank place with no mine
        gametable[mineloc//8][mineloc%8] = "o" # If not have a mine -> put a mine
  
    # Scan neighbours
    print("Scanning neighbours...")
    for x in range(8):
        for y in range(8):
            if gametable[x][y] != "o":
                # Blank cell -> Find neighbours -> Show number
                numberofmines = 0
                if x > 0 and x < 7:
                    # Check (x - 1) row
                    if y > 0 and y < 7:
                        # Check (x - 1) row (y - 1 coloumn)
                        if gametable[x-1][y-1] == "o":
                            numberofmines += 1
                        if gametable[x-1][y]   == "o":
                            numberofmines += 1
                        if gametable[x-1][y+1] == "o":
                            numberofmines += 1
                        if gametable[x][y-1]   == "o":
                            numberofmines += 1
                        if gametable[x][y+1]   == "o":
                            numberofmines += 1
                        if gametable[x+1][y-1] == "o":
                            numberofmines += 1
                        if gametable[x+1][y]   == "o":
                            numberofmines += 1
                        if gametable[x+1][y+1] == "o":
                            numberofmines += 1

                    elif y == 0:
                        if gametable[x-1][0]   == "o":
                            numberofmines += 1
                        if gametable[x-1][1]   == "o":
                            numberofmines += 1
                        if gametable[x][1]     == "o":
                            numberofmines += 1
                        if gametable[x+1][0]   == "o":
                            numberofmines += 1
                        if gametable[x+1][1]   == "o":
                            numberofmines += 1

                    elif y == 7:
                        if gametable[x-1][6]   == "o":
                            numberofmines += 1
                        if gametable[x-1][7]   == "o":
                            numberofmines += 1
                        if gametable[x][6]     == "o":
                            numberofmines += 1
                        if gametable[x+1][6]   == "o":
                            numberofmines += 1
                        if gametable[x+1][7]   == "o":
                            numberofmines += 1
    
                if x == 0:
                    if y > 0 and y < 7:
                        if gametable[0][y-1]   == "o":
                            numberofmines += 1
                        if gametable[0][y+1]   == "o":
                            numberofmines += 1
                        if gametable[1][y-1]   == "o":
                            numberofmines += 1
                        if gametable[1][y]     == "o":
                            numberofmines += 1
                        if gametable[1][y+1]   == "o":
                            numberofmines += 1
                    elif y == 0:
                        if gametable[0][1]     == "o":
                            numberofmines += 1
                        if gametable[1][0]   == "o":
                            numberofmines += 1
                        if gametable[1][1]   == "o":
                            numberofmines += 1

                    elif y == 7:
                        if gametable[0][6]     == "o":
                            numberofmines += 1
                        if gametable[1][6]     == "o":
                            numberofmines += 1
                        if gametable[1][7]     == "o":
                            numberofmines += 1
    
                if x == 7:
                    if y > 0 and y < 7:
                        if gametable[6][y-1]   == "o":
                            numberofmines += 1
                        if gametable[6][y]     == "o":
                            numberofmines += 1
                        if gametable[6][y+1]   == "o":
                            numberofmines += 1
                        if gametable[7][y-1]   == "o":
                            numberofmines += 1
                        if gametable[7][y+1]   == "o":
                            numberofmines += 1

                    if y == 0:
                        if gametable[6][0]     == "o":
                            numberofmines += 1
                        if gametable[6][1]     == "o":
                            numberofmines += 1
                        if gametable[7][1]     == "o":
                            numberofmines += 1

                    if y == 7:
                        if gametable[6][6]     == "o":
                            numberofmines += 1
                        if gametable[6][7]     == "o":
                            numberofmines += 1
                        if gametable[7][6]     == "o":
                            numberofmines += 1
    
                gametable[x][y] = numberofmines # Set number of mines to that cell
    print("Scan completed!")
    # Save back to file
    
    gamestatefile = open("minesweeper_readme/gamedata.txt", "w")
    # Write table
    for line in gametable:
        gamestatefile.write(str(line)+"\n")
    # Begin the game
    gamestatefile.write("False\n")
    gamestatefile.write("False\n")
    gamestatefile.write(gamedata[10]+"\n"+gamedata[11])
    gamestatefile.close()
    
if gamedata[8] == True:
    # Use once and ONLY when this game first start.
    re_generate()

else:
    # Pick one issue =) (one request)
    g = Github(myaccesstoken) # Login using token
    repo = g.get_repo("raspiduino/raspiduino")
    try:
        request_title = repo.get_issues(state='open')[0].title # Pick one of the request and get its title
        request_title = request_title.split(":") # Split the request by ':'
        if request_title[1] == "click":
            # One of three things may happen:
            # - Click to one normal cell -> Show its number
            # - Click to 0 cell          -> Show all nearby 0 cell and other cell until have a number
            #       different than 0
            # - Click to bomb cell       -> You die -> Reset game

            alpha = ['a','b','c','d','e','f','g','h']
            if gametable[int(request_title[2][0])][alpha.index(request_title[2][1])] == "x":
                print("You dead!")
                repo.get_issues(state='open')[0].edit(state='closed') # Close that issue
                # Write to gamedata.txt
                gamestatefile = open("minesweeper_readme/gamedata.txt", "w")
                # Write table
                for line in gametable:
                    gamestatefile.write(str(line)+"\n")
                # Begin the game
                gamestatefile.write("False\n")
                gamestatefile.write("True\n")
                gamestatefile.write(gamedata[10]+"\n"+gamedata[11])
                gamestatefile.close()

            elif gametable[int(request_title[2][0])][alpha.index(request_title[2][1])] == "0":
                pass # Work on this later

            else:
                # Any other number -> Display that number
                pass
        
        elif request_title[1] == "flag":
            # Flag a cell
            pass

    except Exception as e:
        print("Error!")
        print(e)
