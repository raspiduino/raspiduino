'''
Github profile's Readme minesweeper game
Copyright @raspiduino 2021
Date created 30/1/2021
'''

import random
from github import Github # PyGithub
import os

# Get the access token
myaccesstoken = os.environ['MYACCESSTOKEN']

alpha = ['a','b','c','d','e','f','g','h']

# Read the game state file
gamestatefile = open("minesweeper_readme/gamedata.txt", "r")
gamedata = gamestatefile.read()
gamestatefile.close()

gamedata = gamedata.split("\n") # Split lines

# Read the action file
gameactionfile = open("minesweeper_readme/action.txt", "r")
gameaction = gameactionfile.read()
gameactionfile.close()

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

# Read the 'Readme' file

readmefile = open("raspiduino/README.md", "r")
readme = readmefile.read()
readmefile.close()

readme = readme.split('\n')

def displaygametable(gametable, x, y, usegametable=True, img=None, gameactiontable=None):
    global readme
    displayline = readme[8+x].split("|")

    before = displayline[:2+y]
    after = displayline[3+y:]
    
    orglink = "https://raw.githubusercontent.com/raspiduino/raspiduino/main/images/"
    imglink = ""

    if usegametable == True:
        cell = gametable[x][y]
        action = gameactiontable[x][y]

        if action == "P":
            # Flagged
            imglink = "flagged"

        elif cell == "o":
            # Mine!
            imglink = "bomb"

        else:
            # Any other cell type
            imglink = cell

    else:
        # Manually
        imglink = img

    orgissuelink = "https://github.com/raspiduino/raspiduino/issues/new?title=minesweeper%3A{}%3A{}&body=Just+click+%27Submit+new+issue%27.+Thanks+for+playing+my+game!"

    data = "|<a href='" + orgissuelink.format("click", str(x) + alpha[y]) + "'>![](" + orglink + imglink + ".png)</a><a href='" + orgissuelink.format("flag", str(x) + alpha[y]) + "'>🚩</a>|"

    readmefile = open("raspiduino/README.md", "w")
    for line in readme[:8+x]:
        readmefile.write(line + "\n")

    readmefile.write("|".join(before) + data + "|".join(after) + "\n")

    for line in readme[9+x:]:
        readmefile.write(line + "\n")

    # Re update the readme content
    readmefile = open("raspiduino/README.md", "r")
    readme = readmefile.read()
    readmefile.close()

    readme = readme.split('\n')

def writegameactiontable(gameactiontable):
    # Write to gameaction.txt
    gameactionfile = open("minesweeper_readme/action.txt", "w")
    # Write table
    for line in gameactiontable:
        gameactionfile.write(str(line)+"\n")
    gameactionfile.close()

def checkifwon(gametable, gameactiontable):
    gameactionfile = open("minesweeper_readme/action.txt", "r")
    gameaction = gameactionfile.read()
    gameactionfile.close()

    if not "0" in gameaction:
        # You win!
        print("You win!")

        # Display all things
        for x in range(8):
            for y in range(8):
                displaygametable(gametable, x, y, gameactiontable=gameactiontable)

        readmefile = open("raspiduino/README.md", "r")
        readme = readmefile.read()
        readmefile.close()

        readme = readme.split('\n')
        readme[17] == "<br>You win! Wanted to play again? Click <a href='https://github.com/raspiduino/raspiduino/issues/new?title=minesweeper%3Aplayagain&body=Just+push+%27Submit+new+issue%27+to+play+again.+You+don%27t+need+to+do+anything+else.'>here</a>"

        readmefile = open("raspiduino/README.md", "w")
        readmefile.write('\n'.join(readme))
        readmefile.close()

def leaderboard():
    gamestatefile = open("minesweeper_readme/gamedata.txt", "r")
    gamedata = gamestatefile.read().split("\n")
    gamestatefile.close()

    readmefile = open("raspiduino/README.md", "r")
    readme = readmefile.read().split('\n')
    readmefile.close()

    leaderboardlist = gamedata[11].split(',')

    newplayer = gamedata[10].split(',')[-1].split('|')
    
    userexisted = False

    for i in leaderboardlist:
        if newplayer[0] in i:
            userexisted = True
            userindex = leaderboardlist.index(i)
            break

    if userexisted:
        leaderboardlist[userindex] = str(int(leaderboardlist[userindex].split('|')[0]) + 1) + '|' + newplayer[0] + '|' + newplayer[1]

    else:
        leaderboardlist.append('1|' + newplayer[0] + '|' + newplayer[1])

    leaderboardlist.sort()
    
    #print(leaderboardlist)

    if len(leaderboardlist) > 20:
        leaderboardlist.pop(0)

    i = 31
    for leaduser in leaderboardlist:
        leadusercontent = leaduser.split('|')
        readme[i] = "| " + leadusercontent[0] + " | <a href='" + leadusercontent[2] + "'>" + leadusercontent[1] + "</a>|"
        i += 1
    
    readmefile = open("raspiduino/README.md", "w")
    readmefile.write('\n'.join(readme))
    readmefile.close()

    gamedata[11] = ','.join(leaderboardlist)
    
    gamestatefile = open("minesweeper_readme/gamedata.txt", "w")
    gamestatefile.write('\n'.join(gamedata))
    gamestatefile.close()

def lastplay(currentissue, action, x, y):
    gamestatefile = open("minesweeper_readme/gamedata.txt", "r")
    gamedata = gamestatefile.read().split("\n")
    gamestatefile.close()

    readmefile = open("raspiduino/README.md", "r")
    readme = readmefile.read().split("\n")
    readmefile.close()

    lastplayboard = gamedata[10].split(",")
    lastplayboard.append(currentissue.user.name + "|" + currentissue.user.html_url + "|" + action + "|" + str(x) + "|" + alpha[y])

    if len(lastplayboard) > 5:
        lastplayboard.pop(0) # Remove one

    gamedata[10] = str(','.join(lastplayboard))

    # Display the board
    i = 0

    for item in lastplayboard[::-1]:
        iteminfo = item.split('|')
        readme[22 + i] = "| " + iteminfo[2] + " " + iteminfo[3] + iteminfo[4] + " | <a href='" + iteminfo[1] + "'>" + iteminfo[0] + "</a>"
        i += 1

    # Save things back
    readmefile = open("raspiduino/README.md", "w")
    readmefile.write('\n'.join(readme))
    readmefile.close()

    gamestatefile = open("minesweeper_readme/gamedata.txt", "w")
    gamestatefile.write('\n'.join(gamedata))
    gamestatefile.close()

    leaderboard()

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

    writegameactiontable(gametable)
    
    # Create mines: 10 mines
    print("Creating mines...")
    for i in range(10):
        mineloc = random.randint(0,63)
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
                        if gametable[1][0]     == "o":
                            numberofmines += 1
                        if gametable[1][1]     == "o":
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

                    elif y == 0:
                        if gametable[6][0]     == "o":
                            numberofmines += 1
                        if gametable[6][1]     == "o":
                            numberofmines += 1
                        if gametable[7][1]     == "o":
                            numberofmines += 1

                    elif y == 7:
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

    # Create blank board

    for x in range(8):
        for y in range(8):
            displaygametable(gametable, x, y, False, "facingDown")

    readmefile = open("raspiduino/README.md", "r")
    readme = readmefile.read()
    readmefile.close()

    readme = readme.split('\n')
    readme[17] = ""

    readmefile = open("raspiduino/README.md", "w")
    readmefile.write('\n'.join(readme))
    readmefile.close()
    
if gamedata[8] == "True":
    # Use once and ONLY when this game first start.
    re_generate()

else:
    # Convert the gamedata.txt content to a game table
    gametable = []
    i = 0

    for x in gamedata[:8]:
        gametable.append([])
        for y in x[1:-1].split(', '):
            if "'" in y:
                gametable[i].append(y[1:-1])
            else:
                gametable[i].append(y)
        i += 1

    # Convert the gameaction.txt content to a game action table
    gameactiontable = []
    i = 0

    gameactionfile = open("minesweeper_readme/action.txt", "r")
    gameaction = gameactionfile.read()
    gameactionfile.close()

    gameaction = gameaction.split('\n')

    for x in gameaction:
        gameactiontable.append([])
        for y in x[1:-1].split(', '):
            if "'" in y:
                gameactiontable[i].append(y[1:-1])
            else:
                gameactiontable[i].append(y)
        i += 1

    #print(gametable)

    # Pick one issue =) (one request)
    g = Github(myaccesstoken) # Login using token
    repo = g.get_repo("raspiduino/raspiduino")
    currentissue = repo.get_issues(state='open')[0]
    request_title = currentissue.title # Pick one of the request and get its title
    request_title = request_title.split(":") # Split the request by ':'
    if request_title[1] == "click":
        # One of three things may happen:
        # - Click to one normal cell -> Show its number
        # - Click to 0 cell          -> Show all nearby 0 cell and other cell until have a number
        #       different than 0
        # - Click to bomb cell       -> You die -> Reset game

        #print(int(request_title[2][0]))
        #print(alpha.index(request_title[2][1]))
        cellx = int(request_title[2][0])
        celly = alpha.index(request_title[2][1])

        if gametable[cellx][celly] == "o":
            print("You dead!")
            currentissue.create_comment("You dead, but don't worry, you can always play again!")
            currentissue.edit(state='closed') # Close that issue

            # Write to gamedata.txt
            gamestatefile = open("minesweeper_readme/gamedata.txt", "w")
            # Write table
            for line in gametable:
                gamestatefile.write(str(line)+"\n")
            
            gamestatefile.write("False\n")
            gamestatefile.write("True\n")
            gamestatefile.write(gamedata[10]+"\n"+gamedata[11])
            gamestatefile.close()

            # Show the full game table
            for x in range(8):
                for y in range(8):
                    displaygametable(gametable, x, y, gameactiontable=gameactiontable)

            readmefile = open("raspiduino/README.md", "r")
            readme = readmefile.read()
            readmefile.close()

            readme = readme.split('\n')
            readme[17] = "<br>You lost! Wanna to play again? Click <a href='https://github.com/raspiduino/raspiduino/issues/new?title=minesweeper%3Aplayagain&body=Just+push+%27Submit+new+issue%27+to+play+again.+You+don%27t+need+to+do+anything+else.'>here</a>"

            readmefile = open("raspiduino/README.md", "w")
            readmefile.write('\n'.join(readme))
            readmefile.close()
            lastplay(currentissue, "Click", cellx, celly)

        else:
            # Any other number -> Display that number
            displaygametable(gametable, cellx, celly, gameactiontable=gameactiontable)
            currentissue.create_comment("Done! You can check again at https://github.com/raspiduino")
            currentissue.edit(state='closed') # Close that issue
            lastplay(currentissue, "Click", cellx, celly)
            gameactiontable[cellx][celly] = "X"
            writegameactiontable(gameactiontable)
            checkifwon(gametable, gameactiontable)

    elif request_title[1] == "flag":
        # Flag a cell
        cellx = int(request_title[2][0])
        celly = alpha.index(request_title[2][1])
        if gameactiontable[cellx][celly] == "P":
            # Remove flag if existed
            gameactiontable[cellx][celly] = gameactiontable[cellx][celly][:1]

        else:
            # Add a flag
            gameactiontable[cellx][celly] = "P"
        displaygametable(gametable, cellx, celly, False, 'flagged')
        currentissue.create_comment("Done! You can check again at https://github.com/raspiduino")
        currentissue.edit(state='closed') # Close that issue
        #displaylastplaytable(currentissue)
        writegameactiontable(gameactiontable)
        checkifwon(gametable, gameactiontable)
        lastplay(currentissue, "Flag", cellx, celly)

    elif request_title[1] == "playagain":
        re_generate()
        currentissue.create_comment("Ok! You can play again now at https://github.com/raspiduino")
        currentissue.edit(state='closed') # Close that issue
