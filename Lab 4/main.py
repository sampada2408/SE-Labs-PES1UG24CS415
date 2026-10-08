import pygame
from game.game_engine import GameEngine

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer - Pygame Version")
clock = pygame.time.Clock()

engine = GameEngine(WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      # window X button AND the ESC key
            running = False
        engine.handle_event(event)         # every event goes to the engine

    engine.handle_input()
    engine.update()

    screen.fill((100, 160, 220))           # sky blue background
    engine.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()