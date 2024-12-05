import pygame
import random

pygame.init()
pygame.display.set_caption("Pokemon Aquarium")
pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
objects = []
points = 0

# Temporary item names - counts how much you own of each item
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
total_fish = []

fish_image = pygame.image.load('fish.png').convert_alpha()
fish_size = 50 #THIS SHOULD BE THE SAME SIZE AS YOUR FISH SPRITE (square)

def mainButtonFunction():
    global points
    points += 1

def buyFunction(cost, item):
    global points
    global items_owned
    points -= cost
    items_owned[item] += 1
    fish = spawn_fish()
    total_fish.append(fish)

def spawn_fish():
    fish = Fish()
    fish.x = random.randrange(fish_size, screen.get_width() - fish_size)
    fish.y = random.randrange(fish_size, screen.get_height() - fish_size)
    fish.dx = random.randrange(-5, 5)
    return fish

class Fish():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.direction = self.dx / abs(self.dx)

# MAIN BUTTON YOU WILL BE CLICKING (ex: coral from abyssrium)
class MainButton():
    def __init__(self, pos=((screen.get_width()/2),(screen.get_height()/2)), size=(300,300)):
        self.pos = pos
        self.size = size
        self.image = {
            'normal': pygame.image.load("normal.png").convert_alpha(),
            'hover': pygame.image.load("hover.png").convert_alpha(),
            'pressed': pygame.image.load("pressed.png").convert_alpha(),
        }
        self.buttonSurface = pygame.Surface((self.size[0], self.size[1]))
        self.buttonRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.alreadyPressed = False
        objects.append(self)
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        screen.blit(self.image['normal'], self.buttonRect)
        
        if self.buttonRect.collidepoint(mousePos):
            screen.blit(self.image['hover'], self.buttonRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                screen.blit(self.image['pressed'], self.buttonRect)
                if not self.alreadyPressed:
                    mainButtonFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        

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

        for fish in total_fish:
            if fish.dx > 5 or fish.dx < -5 or fish.dx == 0:
                fish.dx = random.randrange(-5,5)
            fish.x += fish.dx
 
            if fish.x > screen.get_width() + fish_size or fish.x < -(fish_size):
                fish.dx *= -1*(random.uniform(0.5,1.5))
                fish.y = random.randrange(fish_size, screen.get_height() - fish_size)

            fish_image = pygame.image.load('fish.png').convert_alpha()
            if fish.dx < 0:
                fish_image = pygame.transform.flip(fish_image, True, False)
            screen.blit(fish_image, [fish.x, fish.y])

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