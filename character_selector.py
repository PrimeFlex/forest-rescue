import pygame
import os
import sys
import random

pygame.init()

# --- Config ---
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Rescue - Choose Character & Scene")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

# --- Paths ---
CHARACTER_FOLDER = "assets/characters"
SCENE_FOLDER = "assets/scenes"

# --- Character Covers ---
CHARACTERS = {
    "Ball_Yellow": "bowtie_cover.png",
    "bunny": "bunny_cover.png",
    "pinkgirl": "pinkgirl_cover.png",
    "Raccoon": "raccoon_cover.png"
}

# --- Scene Thumbnails ---
SCENES = {
    "morning": "morning.png",
    "midday": "midday.png",
    "evening": "evening.png",
    "night": "night.png"
}

CHARACTER_SIZE = (100, 100)
SCENE_SIZE = (180, 100)

# --- Load Random Cover Background ---
def get_random_background():
    files = [f for f in os.listdir(SCENE_FOLDER) if f.endswith(".png")]
    bg = pygame.image.load(os.path.join(SCENE_FOLDER, random.choice(files))).convert()
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))


# --- UI Layout ---
def layout_items(items, start_x, y, size, gap):
    positions = {}
    x = start_x
    for key, image in items.items():
        positions[key] = pygame.Rect(x, y, *size)
        x += size[0] + gap
    return positions


def load_images(folder, items, size):
    return {key: pygame.transform.scale(
        pygame.image.load(os.path.join(folder, filename)), size)
        for key, filename in items.items()}


# --- Draw Screen ---
def draw(bg, char_images, scene_images, selected_char, selected_scene):
    screen.blit(bg, (0, 0))

    # Titles
    title = font.render("Select Your Character", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    title2 = font.render("Choose Scene", True, (0, 0, 0))
    screen.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 250))

    # Characters
    for name, rect in char_positions.items():
        screen.blit(char_images[name], rect)
        if name == selected_char:
            pygame.draw.rect(screen, (255, 100, 100), rect, 5)
        label = small_font.render(name.replace("_", " ").capitalize(), True, (0, 0, 0))
        screen.blit(label, (rect.x, rect.bottom + 5))

    # Scenes
    for name, rect in scene_positions.items():
        screen.blit(scene_images[name], rect)
        if name == selected_scene:
            pygame.draw.rect(screen, (100, 150, 255), rect, 5)
        label = small_font.render(name.capitalize(), True, (0, 0, 0))
        screen.blit(label, (rect.x, rect.bottom + 5))

    # Start button
    if selected_char and selected_scene:
        pygame.draw.rect(screen, (0, 180, 0), start_button_rect)
    else:
        pygame.draw.rect(screen, (120, 120, 120), start_button_rect)

    button_text = font.render("Start Game", True, (255, 255, 255))
    screen.blit(button_text, (start_button_rect.centerx - button_text.get_width() // 2,
                              start_button_rect.centery - button_text.get_height() // 2))


# --- Initialization ---
char_images = load_images(CHARACTER_FOLDER, CHARACTERS, CHARACTER_SIZE)
scene_images = load_images(SCENE_FOLDER, SCENES, SCENE_SIZE)

char_positions = layout_items(CHARACTERS, 90, 100, CHARACTER_SIZE, 50)
scene_positions = layout_items(SCENES, 60, 310, SCENE_SIZE, 30)
start_button_rect = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

bg_cover = get_random_background()

selected_character = None
selected_scene = None

# --- Main Loop ---
def main():
    global selected_character, selected_scene
    running = True
    while running:
        clock.tick(60)
        draw(bg_cover, char_images, scene_images, selected_character, selected_scene)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for name, rect in char_positions.items():
                    if rect.collidepoint(pos):
                        selected_character = name

                for name, rect in scene_positions.items():
                    if rect.collidepoint(pos):
                        selected_scene = name

                if start_button_rect.collidepoint(pos) and selected_character and selected_scene:
                    return selected_character, selected_scene


if __name__ == "__main__":
    char, scene = main()
    import play_level
    play_level.main(char, scene)
