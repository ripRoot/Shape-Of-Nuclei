import pygame 
import pymunk
from pymunk import pygame_util
import numpy as np

class Drawing:
    def __init__(self, space, screen):
        self.space = space
        self.screen = screen
        self.points = []
        self.isDrawing = False
        self.segments = []

    def append_points(self, mouse_pressed, mouse_position):
        '''
            if the mouse is pressed it saves it to a arr of points that will be drawn
        '''
        if mouse_pressed:
            self.points.append(mouse_position)
        else:
            self.points.clear()

    def draw_segments(self):
        '''
            Draws segment by mapping first and second points together but also doesnt track if mouse is not pressed
        '''
        for i in range(len(self.points)-1):
            segment = pymunk.Segment(self.space.static_body, self.points[i], self.points[i+1], 5)
            self.segments.append(segment)
            self.space.add(segment)
            pygame.draw.line(self.screen, (255, 0, 0, 255), self.points[i], self.points[i+1], 5)

    def clear_segments(self):
        '''
            clears space of all segments
        '''
        for segment in self.segments:
            self.space.remove(segment)
        self.segments.clear()
