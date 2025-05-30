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
    "Ball_Yellow": {"cover": "bowtie_cover.png", "folder": "Ball_Yellow"},
    "bunny": {"cover": "bunny_cover.png", "folder": "bunny"},
    "pinkgirl": {"cover": "pinkgirl_cover.png", "folder": "pinkgirl"},
    "Raccoon": {"cover": "raccoon_cover.png", "folder": "Raccoon"}
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

def get_random_background():
    files = [f for f in os.listdir(SCENE_FOLDER) if f.endswith(".png")]
    bg = pygame.image.load(os.path.join(SCENE_FOLDER, random.choice(files))).convert()
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))

def layout_items(items, start_x, y, size, gap):
    positions = {}
    x = start_x
    for key in items:
        positions[key] = pygame.Rect(x, y, *size)
        x += size[0] + gap
    return positions

def load_character_images():
    images = {}
    for name, data in CHARACTERS.items():
        path = os.path.join(CHARACTER_FOLDER, data["folder"], data["cover"])
        image = pygame.image.load(path).convert_alpha()
        images[name] = pygame.transform.scale(image, CHARACTER_SIZE)
    return images

def load_scene_images():
    images = {}
    for name, filename in SCENES.items():
        path = os.path.join(SCENE_FOLDER, filename)
        image = pygame.image.load(path).convert_alpha()
        images[name] = pygame.transform.scale(image, SCENE_SIZE)
    return images

def draw_button(rect, color, hover_color, text, mouse_pos):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (rect.centerx - text_surface.get_width() // 2,
                               rect.centery - text_surface.get_height() // 2))

def show_loading_screen():
    screen.fill((0, 0, 0))
    loading_text = font.render("Loading...", True, (255, 255, 255))
    screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2,
                               HEIGHT // 2 - loading_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

# --- Initialization ---
char_images = load_character_images()
scene_images = load_scene_images()

char_positions = layout_items(CHARACTERS, 90, 100, CHARACTER_SIZE, 50)
scene_positions = layout_items(SCENES, 60, 310, SCENE_SIZE, 30)
start_button_rect = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

bg_cover = get_random_background()
selected_character = None
selected_scene = None

def draw(mouse_pos):
    screen.blit(bg_cover, (0, 0))

    title = font.render("Select Your Character", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    title2 = font.render("Choose Scene", True, (0, 0, 0))
    screen.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 250))

    for name, rect in char_positions.items():
        screen.blit(char_images[name], rect)
        if name == selected_character:
            pygame.draw.rect(screen, (255, 100, 100), rect, 5)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 200, 200), rect, 3)

        label = small_font.render(name.replace("_", " ").capitalize(), True, (0, 0, 0))
        screen.blit(label, (rect.x, rect.bottom + 5))

    for name, rect in scene_positions.items():
        screen.blit(scene_images[name], rect)
        if name == selected_scene:
            pygame.draw.rect(screen, (100, 150, 255), rect, 5)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (180, 220, 255), rect, 3)

        label = small_font.render(name.capitalize(), True, (0, 0, 0))
        screen.blit(label, (rect.x, rect.bottom + 5))

    if selected_character and selected_scene:
        draw_button(start_button_rect, (0, 180, 0), (0, 220, 0), "Start Game", mouse_pos)
    else:
        draw_button(start_button_rect, (100, 100, 100), (150, 150, 150), "Start Game", mouse_pos)

def main():
    global selected_character, selected_scene
    while True:
        mouse_pos = pygame.mouse.get_pos()
        draw(mouse_pos)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in char_positions.items():
                    if rect.collidepoint(event.pos):
                        selected_character = name

                for name, rect in scene_positions.items():
                    if rect.collidepoint(event.pos):
                        selected_scene = name

                if (start_button_rect.collidepoint(event.pos)
                        and selected_character and selected_scene):
                    show_loading_screen()
                    return selected_character, selected_scene

if __name__ == "__main__":
    while True:
        char, scene = main()
        import play_level
        result = play_level.main(char, scene)
        if result == "back_to_menu":
            selected_character = None
            selected_scene = None
        elif result == "quit":
            break
