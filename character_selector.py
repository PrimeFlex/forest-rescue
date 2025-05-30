import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choose Your Character")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

# Load images
CHARACTER_OPTIONS = {
    "bowtie": pygame.image.load("assets/ui/cover_characters/bowtie_cover.png"),
    "bunny": pygame.image.load("assets/ui/cover_characters/bunny_cover.png"),
    "pinkgirl": pygame.image.load("assets/ui/cover_characters/pinkgirl_cover.png"),
    "raccoon": pygame.image.load("assets/ui/cover_characters/raccoon_cover.png"),
}

# Resize for display
CHARACTER_SIZE = (100, 100)
for key in CHARACTER_OPTIONS:
    CHARACTER_OPTIONS[key] = pygame.transform.scale(CHARACTER_OPTIONS[key], CHARACTER_SIZE)

# Layout
character_positions = {
    "bowtie": (100, 200),
    "bunny": (250, 200),
    "pinkgirl": (400, 200),
    "raccoon": (550, 200),
}
selected_character = None

# Button
start_button_rect = pygame.Rect((WIDTH // 2 - 100, 450, 200, 50))


def draw():
    screen.fill((200, 240, 255))

    # Title
    title_text = font.render("Select Your Character", True, (50, 50, 50))
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 80))

    # Draw characters
    for name, pos in character_positions.items():
        img = CHARACTER_OPTIONS[name]
        screen.blit(img, pos)

        # Outline if selected
        if name == selected_character:
            pygame.draw.rect(screen, (255, 100, 100), (*pos, *CHARACTER_SIZE), 5)

        # Label
        label = small_font.render(name.capitalize(), True, (0, 0, 0))
        screen.blit(label, (pos[0] + 10, pos[1] + 110))

    # Draw start button
    if selected_character:
        pygame.draw.rect(screen, (0, 200, 0), start_button_rect)
    else:
        pygame.draw.rect(screen, (100, 100, 100), start_button_rect)

    button_text = font.render("Start Game", True, (255, 255, 255))
    screen.blit(button_text, (start_button_rect.centerx - button_text.get_width() // 2,
                              start_button_rect.centery - button_text.get_height() // 2))


def get_clicked_character(mouse_pos):
    for name, pos in character_positions.items():
        char_rect = pygame.Rect(*pos, *CHARACTER_SIZE)
        if char_rect.collidepoint(mouse_pos):
            return name
    return None


def main():
    global selected_character

    running = True
    while running:
        clock.tick(60)
        draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                clicked = get_clicked_character(mouse_pos)
                if clicked:
                    selected_character = clicked

                if start_button_rect.collidepoint(mouse_pos) and selected_character:
                    print(f"Starting game with: {selected_character}")
                    return selected_character  # Pass into main game


# Entry point
if __name__ == "__main__":
    selected = main()
    # Load the main game here, e.g.:
    # import game
    # game.run(selected)
