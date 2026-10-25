import pygame
import pymunk
import colorsys
import numpy as np
import pymunk.pygame_util
import cv2
'''
Creates image at the center using inputed image points, uses all points not just perimeter points. no slow noticable,
could change in the future
DISCLIAMER: NO AI USED IN THE CREATION OF CODE
'''
# Global Variables
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
marbles = []
frozen_marbles = []
marbleSize = 2
stick = True
x=width/2
y=height/2
image = cv2.imread('DEEP projects/Images/hat dog.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    print("error")
    exit()

def main():
    screen=pygame.display.set_mode((width, height))
    clock=pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 00,00

    perimeter = getPointsOfImage(image)
    create_figure(space, perimeter, image)
    
    running = True
    #draw_options = pymunk.pygame_util.DrawOptions(screen)
    if(stick):   
        space.on_collision(2, 1, begin=on_hit)
    

    ticks_until_next_marble = 0
    counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        if counter <= 10000:
            ticks_until_next_marble -= 1
            if ticks_until_next_marble <= 0:
                how_many_marbles(space, counter, ticks_until_next_marble)
                ticks_until_next_marble = 0
                counter+=1

        #space.debug_draw(draw_options)


        '''
        switch it to pygame draw 
        '''

        space.step(1 / 60)

        for marble in frozen_marbles:
            marble.body_type = pymunk.Body.STATIC
        frozen_marbles.clear()

        draw_marbles(screen, marbles)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def randomx(width):
    '''
    Randimizes a distance inbetween 0 and width. 
    '''
    rng = np.random.default_rng()
    x = rng.integers(0, width)
    return x

def how_many_marbles(space, counter, ticks):
    '''
    adds marble into arr to be spawned in space() later
    '''
    body2=pymunk.Body()
    body2.position = getrandompoint(width, height)
    circle=pymunk.Circle(body2, marbleSize)
    circle.color = get_color(counter, ticks)
    circle.mass = 100
    circle.collision_type = 2
    circle.elasticity = 0
    circle.friction = 0.1
    #circle.group = 1
    
    # Make each marble go towards the center
    dx = x - body2.position.x
    dy = y - body2.position.y
    dist = (dx ** 2 + dy ** 2) ** 0.5
    body2.velocity= (dx / dist * 250, dy / dist * 250)

    space.add(body2, circle)
    marbles.append(circle)

def create_figure(space, points, image):
    '''
    compares center of image and screen them places physical points at every white point on image
    based on points retrived from getPointsOfImage()
    '''
    center_x = x - image.shape[0]/2
    center_y = y - image.shape[1]/2
    for point in points:
        figBody = pymunk.Body(body_type=pymunk.Body.STATIC)
        figBody.position = (center_x+point[1],center_y+point[0])
        figShape = pymunk.Circle(figBody, radius=1)
        figShape.collision_type = 1
        space.add(figBody, figShape)

def getPointsOfImage(image):
    '''
    gets every white pixel point from Canny and puts them into a set of tuples called perimeter
    '''
    edges = cv2.Canny(image, 100, 20)
    perimeter = set()
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]
    for i in range(imageHeight):
        for j in range(imageWidth):
            if(edges[i,j] == 255):
                perimeter.add(tuple([i,j]))
    return perimeter   

def draw_marbles(screen, marbles):
    '''
    Draws marbles...l ol..
    '''
    for marble in marbles:
        pos = (int(marble.body.position.x), int(marble.body.position.y))
        pygame.draw.circle(screen, marble.color, pos, marbleSize)

def on_hit(collision_marbles, space, data):
    collision_marbles.shapes[0].body.velocity = (0, 0)
    collision_marbles.shapes[0].body.angular_velocity = 0
    collision_marbles.shapes[0].collision_type = 1
    

    frozen_marbles.append(collision_marbles.shapes[0].body)


def get_color(counter, ticks):
    '''
    Uses an oscilating alg to pick the hue of the ball. Every 100 balls it shifts hue.
    '''
    group = counter // 100
    basic_hue = (group * 0.15) % 1.0 
    oscillation = 0.05 * (ticks / 50.0)
    hue = (basic_hue + oscillation) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)    #colorsys module.. converts Hue, Saturaltion, Variation to Red, Green, Blue
    return int(r * 255), int(g * 255), int(b * 255)

def getrandompoint(width, height):
    '''
    Treat perimeter as one continuous line, L=2*(width+height)
    Function cuts each section into strips. Depending on where the random distance lands,
    there will be a correlating section for which the ball spawns. 
    '''
    L=2*(width+height)
    rng = np.random.default_rng()
    random_dist = rng.integers(0, L)
    if random_dist < width:
        #Top
        return random_dist, 0
    elif random_dist < width + height:
        #Right
        return width, random_dist-width
    elif random_dist < 2*width + height:
        #Bottom
        return width - (random_dist - (width+height)), height
    elif random_dist < L:
        #Left
        return 0, height - (random_dist - (2*width + height))

main()



