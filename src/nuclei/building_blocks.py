import pygame
import pymunk
import colorsys
import numpy as np
import pymunk.pygame_util

'''
1.) Agregate at the edges.
2.) image generation for input.
rasterizing

reverse ray tracing.

map the outline
balls bounce
onlooker will draw on screen/picture
image in the middle spinning,
build shape from that bouncing


idea:
have a button that is clickable after drawing thats (done), another button that says (try again)... and also (restart)

wow i really need to rearrange this code lol

marbles bounce off, track angle (try different angles to find hit point) map point -- biggest problem optimizing..

if marble goes straight, we can get rid of it because it didnt hit on object
'''
# Global Variables
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
marbles = []
frozen_marbles = []
x = width/2
y = height/2

def main():
    screen=pygame.display.set_mode((width, height))
    clock=pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 00,00
    '''
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x,y)
    middle_shape = pymunk.Circle(body, 100)
    middle_shape.collision_type = 1
    space.add(body, middle_shape)
    '''
    curr_points = []
    drawn_section = []

    running = True
    #draw_options = pymunk.pygame_util.DrawOptions(screen)
    #space.on_collision(2, 1, begin=on_hit)
    

    ticks_until_next_marble = 0
    counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                '''
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    curr_points = [event.pos]
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    curr_points.append(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.type == 1 and drawing:
                    drawing = False

                    for i in range(len(curr_points -1)):
                        segment = pymunk.Segment(space.static_body, curr_points[i], curr_points[i+1], 10)
                        
                        space.add(segment)
                        '''
        screen.fill((0, 0, 0))


        '''
            This segment of code is the drawing mechanic.
        '''
        if pygame.mouse.get_pressed()[0]:
            points.append(pygame.mouse.get_pos())
        else:
            points.clear()
        for i in range(len(points) - 1):
            segment = pymunk.Segment(space.static_body, points[i], points[i+1], 50)
            space.add(segment)
            pygame.draw.line(screen, (255, 0, 0, 255), points[i], points[i+1], 50)
        

        '''
            This segment is the marbles..
        '''
        if counter <= 10000:
            ticks_until_next_marble -= 1
            if ticks_until_next_marble <= 0:
                how_many_marbles(space, counter, ticks_until_next_marble)
                ticks_until_next_marble = 0
                counter+=1

        #space.debug_draw(draw_options)


        '''
        switch it to pygame draw 

        check if object passes [segment] points/coordinate, then backtrack to have it bounce off..
        '''

        space.step(1/60)

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
    circle=pymunk.Circle(body2, 4)
    circle.color = get_color(counter, ticks)
    circle.mass = 100
    circle.collision_type = 2
    circle.elasticity = 0
    circle.friction = 0.1
    #circle.group = 1
    
    # Make each marble go towards the center
    
    '''
    dist = (dx ** 2 + dy ** 2) ** 0.5
    body2.velocity= (dx / dist * 250, dy / dist * 250)



    if it hits, then 
    '''


    body2.velocity = calculate_velocity(body2.position.x, body2.position.y)
    space.add(body2, circle)
    marbles.append(circle)
    '''
def calculate_velocity(self, x, y):
    if y==0:
        dist = self.
   '''
def calculate_velocity(x, y):
    '''
    if marble spawns at (x,0) equals top, then you want velocity to map to (x, height)..
    if marble spawns at (0, y) equals LHS, then you want to map velocity to (width, y)..
    '''
    if y == 0:
        #if Top
        dist = height
        return (x/dist, dist / 2)
    if x == 0:
        #if Left
        dist = width
        return (dist /2, y/dist)
    if x == width:
        #if Right
        dist = -width
        return (dist /2, y/dist)
    if y == height:
        #if Bottom
        dist = -height
        return (x/dist, dist/2)

def draw_marbles(screen, marbles):
    '''
    Draws marbles...
    '''
    for marble in marbles:
        pos = (int(marble.body.position.x), int(marble.body.position.y))
        pygame.draw.circle(screen, marble.color, pos, 4)

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

