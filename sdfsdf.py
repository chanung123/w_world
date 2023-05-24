import pygame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mouse Toggle Example")

# Initialize the toggle state
mouse_toggled = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_toggled = not mouse_toggled  # Toggle the mouse state

    screen.fill((255, 255, 255))  # Clear the screen

    if mouse_toggled:
        # Draw a circle at the current mouse position
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 20)

    pygame.display.flip()