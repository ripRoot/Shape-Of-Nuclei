'''
glip glub, everything is getting too complicated. 
would be best to use objects
yay

'''
import numpy as np
import pymunk
import pygame
import colorsys

class Simulation:
    def __init__(self, width, height, space, screen):
        self.width = width
        self.height = height
        self.space = space
        self.screen = screen

        marbles = []
        frozen_marbles = []
        
    
    def randomx(self):
        '''
        Randimizes a distance inbetween 0 and width. 
        '''
        rng = np.random.default_rng()
        x = rng.integers(0, self.width)
        return x

    def how_many_marbles(self, counter, ticks):
        '''
        adds marble into arr to be spawned in space() later
        '''
        body2=pymunk.Body()
        body2.position = self.getrandompoint(self.width, self.height)
        circle=pymunk.Circle(body2, 4)
        circle.color = self.get_color(counter, ticks)
        circle.mass = 100
        circle.collision_type = 2
        circle.elasticity = 0
        circle.friction = 0.1
        #circle.group = 1

        # Make each marble go towards the center
        '''
            needs to be reworked..  keeping for now

            idea: marble spawns at (x, y)

            if marble spawns at top, want to do (x, 0) --> (x, height)
        '''

        dx = body2.position.x
        dy = body2.position.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        body2.velocity= (dx / dist * 250, dy / dist * 250)

        self.space.add(body2, circle)
        self.marbles.append(circle)
    
    def calculate_velocity(self, x, y):
            '''
                if marble spawns at (x,0) equals top, then you want velocity to map to (x, height)..
                if marble spawns at (0, y) equals LHS, then you want to map velocity to (width, y)..
            '''
            if y == 0:
                #if Top
                dist = self.height
                return (x/dist, dist)
            if x == 0:
                #if Left
                dist = self.width
                return (dist, y/dist)
            if x == self.width:
                #if Right
                dist = -self.width
                return (dist, y/dist)
            if y == self.height:
                #if Bottom
                dist = -self.height
                return (x/dist, dist)

    def draw_marbles(self):
        '''
        Draws marbles...
        '''
        for marble in self.marbles:
            pos = (int(marble.body.position.x), int(marble.body.position.y))
            pygame.draw.circle(self.screen, marble.color, pos, 4)

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

    



    def getrandompoint(self):
        '''
        Treat perimeter as one continuous line, L=2*(width+height)
        Function cuts each section into strips. Depending on where the random distance lands,
        there will be a correlating section for which the ball spawns. 
        '''
        L=2*(self.width+self.height)
        rng = np.random.default_rng()
        random_dist = rng.integers(0, L)
        if random_dist < self.width:
        #Top
            return random_dist, 0
        elif random_dist < self.width + self.height:
        #Right
            return self.width, random_dist-self.width
        elif random_dist < 2*self.width + self.height:
        #Bottom
            return self.width - (random_dist - (self.width+self.height)), self.height
        elif random_dist < L:
        #Left
            return 0, self.height - (random_dist - (2*self.width + self.height))

