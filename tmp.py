import pygame
import time

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((640, 480))

# Create an object
object = pygame.Rect(100, 100, 100, 100)

# Set the object's speed
x_speed = 10

# Start the main loop
running = True
start_time = time.time()
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If the left mouse button is clicked, move the object to the right
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            object.x += x_speed

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the object
    pygame.draw.rect(screen, (255, 0, 0), object)

    # Update the display
    pygame.display.flip()

    # If the game has been running for 10 seconds, stop the object from moving
    if time.time() - start_time > 10:
        x_speed = 0

# Quit pygame
pygame.quit()