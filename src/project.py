import pygame
import random

pygame.init()
pygame.display.set_caption("Pokemon Aquarium")
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
objects = []
points = 0

# Temporary item names - counts how much you own of each item
# You can add or remove as needed
items_owned = {
    "test1": 0,
    "test2": 0,
}
# Temporary item names - defines how many points/second each item gives
# MUST be same list as items_owned
profit = {
    "test1": 5,
    "test2": 10,
}

def mainButtonFunction():
    global points
    points += 1

def buyFunction(cost, item):
    global points
    global items_owned
    points -= cost
    items_owned[item] += 1
    print(items_owned)

# MAIN BUTTON YOU WILL BE CLICKING (ex: coral from abyssrium)
class MainButton():
    def __init__(self, pos=((screen.get_width()/2),(screen.get_height()/2)), size=(300,300)):
        # Adjust position/size above ^^^ 
        # Current position is in the center of screen || Size should be same as sprite
        self.pos = pos
        self.size = size
        # TO-DO: Replace these colors with sprites
        self.fillColors = {
            'normal': (255,255,255),
            'hover': (255,255,0),
            'pressed': (255,0,0),
        }
        self.buttonSurface = pygame.Surface((self.size[0], self.size[1]))
        self.buttonRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.alreadyPressed = False
        objects.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    mainButtonFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        screen.blit(self.buttonSurface, self.buttonRect)

# TEMPLATE FOR ALL OF THE SHOP BUTTONS
class ShopButton():
    global points
    global items_owned

    def __init__(self, pos, item, title, cost):
        self.size = (200,100) # Adjust size of SHOP BUTTONS here
        self.pos = pos
        self.item = str(item)
        self.title = str(title)
        self.cost = cost

        self.font = pygame.font.SysFont('Arial', 20) # Change the font and size for the SHOP BUTTONS here
        self.fontcolor = (0,0,0) # Adjust font color of SHOP BUTTONS here
        # TO-DO: Replace these colors with sprites
        self.fillColors = {
            'normal': (255,255,255),
            'hover': (255,255,0),
            'pressed': (255,0,0),
            'null': (100,100,100),
        }
        self.buttonSurface = pygame.Surface((self.size[0], self.size[1]))
        self.buttonRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.alreadyPressed = False
        objects.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        
        if points < self.cost:
            self.buttonSurface.fill(self.fillColors['null'])
            self.alreadyPressed = False
        else:
            self.buttonSurface.fill(self.fillColors['normal'])
            
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])
                    if not self.alreadyPressed:
                        buyFunction(self.cost, self.item)
                        self.alreadyPressed = True
                else:
                    self.alreadyPressed = False

        textsurface = self.font.render(self.title, True, self.fontcolor)
        self.buttonSurface.blit(textsurface, [
            self.buttonRect.width/2 - textsurface.get_rect().width/2,
            self.buttonRect.height/2 - textsurface.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

MainButton()

# HOW TO MAKE A SHOP BUTTON:
# 1st section is its position | ex: (0,0) <- COORDINATE
# 2nd section is the name of the item based on items_owned | ex: "test1" <- STRING
# 3rd section is what the button will say | ex: "Test - $5" <- STRING
# 4th section is the cost of the item | ex: 5
ShopButton((0,0), "test1", "Test1 - $5", 5)
ShopButton((0,120), "test2", "Test2 - $10", 10)

def main():
    clock = pygame.time.Clock()
    running = True
    dt = 1000
    global points
    global items_owned
    global profit

    ADDPOINTS = pygame.USEREVENT+1
    pygame.time.set_timer(ADDPOINTS, dt)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ADDPOINTS:
                for i in items_owned:
                    if items_owned[i] > 0:
                        points += (items_owned[i]*profit[i])

        # TEMPORARY: FOR TESTING
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_ESCAPE]:
            pygame.QUIT()
            return
        # TEMPORARY CODE ENDS HERE

        screen.fill(pygame.Color(0, 0, 0))

        for object in objects:
            object.process()

        # Change the font and size for the SCORE COUNTER here
        counter_font = pygame.font.SysFont("Broadway", 30)
        # Change position/color/string for counter here
        counter_text = counter_font.render(f"${points}", True, (255, 255, 255))
        screen.blit(counter_text, ((screen.get_width()/2),0))

        # Change the font and size for the SCORE COUNTER here
        items_font = pygame.font.SysFont('Comic Sans MS', 25)
        items_text = items_font.render(f"Test1: {items_owned["test1"]}", True, (255, 255, 255))
        screen.blit(items_text, (0,250))
        items_text = items_font.render(f"Test2: {items_owned["test2"]}", True, (255, 255, 255))
        screen.blit(items_text, (0,280))

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()

if __name__ == "__main__":
    main()