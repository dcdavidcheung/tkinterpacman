'''
Team Sadbois
David Cheung, Jason Mei

Project: PacCircle

Description: Grossly simplified pacman concept
Control a yellow circle that avoids the other moving circles
Aim to rid the screen of stationary circles
'''

from tkinter import *
import random

def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)

def definePelletLocations(width, height):
    locations = set()
    for a in range(25, width, 25):
        locations.add((a, 25))
        locations.add((a, height-25))
    for b in range(25, width, 25):
        locations.add((25, b))
        locations.add((width-25, b))
    return locations

class Characters(object):
    def __init__(self, speed, color, spawnX, spawnY, currX, currY, rad, xDir=-1, yDir=0):
        self.speed = speed
        self.xDir = xDir
        self.yDir = yDir
        self.color = color
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.currX = currX
        self.currY = currY
        self.rad = rad
        
    def move(self):
        self.currX += self.xDir * self.speed
        self.currY += self.yDir * self.speed
    
    def draw(self, canvas):
        canvas.create_oval(self.currX - self.rad, self.currY - self.rad, self.currX + self.rad, self.currY + self.rad, fill = self.color)
        
    def isOffScreen(self, data):
        if self.currX <= self.rad or self.currY <= self.rad or self.currX >= data.width - self.rad or self.currY >= data.height - self.rad:
            return True
        return False

class Ghosts(Characters):
    def __init__(self, speed, color, spawnX, spawnY, currX, currY, rad):
        super().__init__(speed, color, spawnX, spawnY, currX, currY, rad)
        direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.xDir = direction[0]
        self.yDir = direction[1]
        
    def offScreenAction(self, data):
        direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.xDir = direction[0]
        self.yDir = direction[1]
        if self.currX <= self.rad:
            self.currX = self.rad + 1
        elif self.currX >= data.width - self.rad:
            self.currX = data.width - self.rad - 1
        elif self.currY <= self.rad:
            self.currY = self.rad + 1
        else:
            self.currY = data.height - self.rad - 1
        
class PacMan(Characters):
    def __init__(self, speed, color, spawnX, spawnY, currX, currY, rad, powered, lives, xDir=-1, yDir=0):
        super().__init__(speed, color, spawnX, spawnY, currX, currY, rad, xDir, yDir)
        self.powered = powered
        self.lives = lives
        
    def offScreenAction(self, data):
        if self.currX <= self.rad:
            self.currX = self.rad + 1
        elif self.currX >= data.width - self.rad:
            self.currX = data.width - self.rad - 1
        elif self.currY <= self.rad:
            self.currY = self.rad + 1
        else:
            self.currY = data.height - self.rad - 1
    
    def collideWithGhost(self, ghost):
        if dist(self.currX, self.currY, ghost.currX, ghost.currY) <= 2 * self.rad:
            return True
        return False
    
    def collideWithGhostAction(self):
        self.lives -= 1
        self.currX = self.spawnX
        self.currY = self.spawnY
        
    def lifeCheatCode(self):
        self.lives += 1
    
    def speedCheatCode(self):
        self.speed += 5
        
    def revertCheats(self):
        self.lives = 3
        self.speed = 5

class Edibles(object):
    def __init__(self, x, y, size, color='black', isEaten='False'):
        self.x = x
        self.y = y
        self.size = size
        self.color = 'black'
        self.isEaten = False
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size,
                            self.y + self.size, fill=self.color)
                            
    def eatenByPacMan(self, pacMan):
        if dist(self.x, self.y, pacMan.currX, pacMan.currY) <= pacMan.rad - self.size:
            self.isEaten = True

class Pellet(Edibles):
    def __init__(self, x, y, isEaten):
        super().__init__(x, y, isEaten)
        self.size = 5
        self.color = 'white'
    
class Fruit(Edibles):
    def __init__(self, x, y, isEaten):
        super().__init__(x, y, isEaten)
        self.size = 10
        self.color = random.choice(['red', 'yellow', 'green'])

def init(data):
    data.won = False
    data.isGameOver = False
    data.isPaused = False
    data.timerDelay = 50
    pelletCoor = definePelletLocations(data.width, data.height)
    data.pellets = set()
    for coord in pelletCoor:
        data.pellets.add(Pellet(coord[0], coord[1], False))
    data.totalScore = len(data.pellets)
    data.score = 0
    fruit1 = Fruit(30, 30, False)
    fruit2 = Fruit(30, data.width - 30, False)
    fruit3 = Fruit(data.height - 30, data.width - 30, False)
    fruit4 = Fruit(data.height - 30, 30, False)
    data.fruits = {fruit1, fruit2, fruit3, fruit4}
    data.pacMan = PacMan(5, "yellow", data.width / 2, data.height / 2,
                            data.width / 2, data.height / 2, 20, False, 3)
    data.ghostColors = ['red', 'pink', 'blue', 'orange']
    data.blinky = Ghosts(10, data.ghostColors[0], data.width / 2 - 150,
                        data.height / 2 - 50, data.width / 2 - 150,
                        data.height / 2 - 50, 20)
    data.pinky = Ghosts(10, data.ghostColors[1], data.width / 2 - 50,
                        data.height / 2 - 50, data.width / 2 - 50,
                        data.height / 2 - 50, 20)
    data.inky = Ghosts(10, data.ghostColors[2], data.width / 2 + 50,
                        data.height / 2 - 50, data.width / 2 + 50,
                        data.height / 2 - 50, 20)
    data.clyde = Ghosts(10, data.ghostColors[3], data.width / 2 + 150,
                        data.height / 2 - 50, data.width / 2 + 150,
                        data.height / 2 - 50, 20)

def mousePressed(event, data):
    data.isPaused = True

def keyPressed(event, data):
    if event.keysym == 'r':
        init(data)
    elif event.keysym == 'Up':
        data.pacMan.xDir = 0
        data.pacMan.yDir = -1
    elif event.keysym == 'Left':
        data.pacMan.xDir = -1
        data.pacMan.yDir = 0
    elif event.keysym == 'Right':
        data.pacMan.xDir = 1
        data.pacMan.yDir = 0
    elif event.keysym == 'Down':
        data.pacMan.xDir = 0
        data.pacMan.yDir = 1
    elif event.keysym == 'p':
        data.isPaused = not data.isPaused
    elif event.keysym == 'd':
        data.pacMan.lifeCheatCode()
    elif event.keysym == 'c':
        data.pacMan.speedCheatCode()
    elif event.keysym == 'space':
        data.pacMan.revertCheats()
    else:
        data.isPaused = True

def timerFired(data):
    if not data.isPaused and not data.isGameOver:
        if data.score < 88:
            initSize = len(data.pellets)
            stillAlivePellets = set()
            for pellet in data.pellets:
                pellet.eatenByPacMan(data.pacMan)
                if not pellet.isEaten:
                    stillAlivePellets.add(pellet)
            data.pellets = stillAlivePellets
            finSize = len(data.pellets)
            data.score += (initSize - finSize)
        else:
            if len(data.fruits) > 0:
                initSize = len(data.fruits)
                stillAliveFruits = set()
                for fruit in data.fruits:
                    fruit.eatenByPacMan(data.pacMan)
                    if not fruit.isEaten:
                        stillAliveFruits.add(fruit)
                data.fruits = stillAliveFruits
                finSize = len(data.fruits)
                data.score += 100 * (initSize - finSize)
                data.blinky.speed += 5 * (initSize - finSize)
                data.pinky.speed += 5 * (initSize - finSize)
                data.inky.speed += 5 * (initSize - finSize)
                data.clyde.speed += 5 * (initSize - finSize)
            else:
                data.won = True
                data.isGameOver = True
        if data.pacMan.collideWithGhost(data.blinky):
            data.pacMan.collideWithGhostAction()
        elif data.pacMan.collideWithGhost(data.pinky):
            data.pacMan.collideWithGhostAction()
        elif data.pacMan.collideWithGhost(data.inky):
            data.pacMan.collideWithGhostAction()
        elif data.pacMan.collideWithGhost(data.clyde):
            data.pacMan.collideWithGhostAction()
        if not data.pacMan.isOffScreen(data):
            data.pacMan.move()
        else:
            data.pacMan.offScreenAction(data)
            data.pacMan.move()
        if not data.blinky.isOffScreen(data):
            data.blinky.move()
        else:
            data.blinky.offScreenAction(data)
            data.blinky.move()
        if not data.pinky.isOffScreen(data):
            data.pinky.move()
        else:
            data.pinky.offScreenAction(data)
            data.pinky.move()
        if not data.inky.isOffScreen(data):
            data.inky.move()
        else:
            data.inky.offScreenAction(data)
            data.inky.move()
        if not data.clyde.isOffScreen(data):
            data.clyde.move()
        else:
            data.clyde.offScreenAction(data)
            data.clyde.move()
    if data.pacMan.lives < 1:
        data.isGameOver = True

def redrawAll(canvas, data):
    if data.isPaused:
        canvas.create_text(data.width/2, data.height/2, text="Press p to continue", fill='white')
    elif data.won:
        canvas.create_text(data.width/2, data.height/2, text="Congratulations!\n\nYou Won! :)\n\nFinal Score: %d \n\nPress r to play again" % data.score, fill='white')
    elif data.isGameOver:
        canvas.create_text(data.width/2, data.height/2, text="Game Over! :(\n\nPress r to play again", fill='white')
    else:
        if data.score < 88:
            canvas.create_text(data.width/2, data.height/2, text="Navigate with the arrow keys.\n\nAvoid the circular entities and\neat all the white pellets to win.\n\nLives Left: %d \nScore: %d" % (data.pacMan.lives, data.score), fill='white')
            for pellet in data.pellets:
                pellet.draw(canvas)
        else:
            for fruit in data.fruits:
                canvas.create_text(data.width/2, data.height/2, text="Just Kidding!\n\n You didn't win just yet!\n\nGo eat the colorful pellets. Be careful though...\n\nLives Left: %d \nScore: %d" % (data.pacMan.lives, data.score), fill='white')
                fruit.draw(canvas)
        data.pacMan.draw(canvas)
        data.blinky.draw(canvas)
        data.pinky.draw(canvas)
        data.inky.draw(canvas)
        data.clyde.draw(canvas)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)