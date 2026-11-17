import pygame
import pymunk
from src.nuclei import simulation
from src.nuclei import drawing

def main():

    pygame.init()

    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h

    screen=pygame.display.set_mode((width, height))
    clock=pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 00,00

    marbles_handler = simulation(width, height, space, screen)
    drawing_handler = drawing(space, screen)
    
    running = True
    
    '''
    ticks_until_next_marble = 0
    counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))


        
        
        
        if pygame.mouse.get_pressed()[0]:
            points.append(pygame.mouse.get_pos())
        else:
            points.clear()
        for i in range(len(points) - 1):
            segment = pymunk.Segment(space.static_body, points[i], points[i+1], 5)
            space.add(segment)
            pygame.draw.line(screen, (255, 0, 0, 255), points[i], points[i+1], 5)
        

        
        if counter <= 10000:
            ticks_until_next_marble -= 1
            if ticks_until_next_marble <= 0:
                how_many_marbles(space, counter, ticks_until_next_marble)
                ticks_until_next_marble = 0
                counter+=1

        #space.debug_draw(draw_options)


       

        space.step(1 / 60)

        for marble in frozen_marbles:
            marble.body_type = pymunk.Body.STATIC
        frozen_marbles.clear()

        draw_marbles(screen, marbles)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
'''
main()