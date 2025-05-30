import pygame
import os
import sys
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Rescue - Adventure")
clock = pygame.time.Clock()
FPS = 60

# Paths
CHARACTER_DIR = "assets/characters"
SCENE_DIR = "assets/scenes"
STAR_IMAGE_PATH = "assets/star.png"
MUSIC_PATH = "assets/music/background.mp3"
SOUND_EFFECT_PATH = "assets/sounds/collect.wav"

# Font
font = pygame.font.SysFont('Arial', 36)

# Load scene background
def load_scene_background(scene_name):
    path = os.path.join(SCENE_DIR, f"{scene_name}.png")
    bg = pygame.image.load(path).convert()
    return pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Load character frames
def load_character_frames(name):
    folder = os.path.join(CHARACTER_DIR, name)
    frames = sorted(
        [f for f in os.listdir(folder) if f.endswith(".png")],
        key=lambda f: int(''.join(filter(str.isdigit, f)) or 0)
    )
    return [pygame.image.load(os.path.join(folder, f)).convert_alpha() for f in frames]

# Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.frames = load_character_frames(name)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 80))
        self.speed = 5
        self.flipped = False

    def update(self, keys):
        moved = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.flipped = True
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.flipped = False
            moved = True

        if moved:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.index = 0
            self.image = self.frames[0]
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)

# Star sprite
class Star(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(STAR_IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center=position)

# Display results screen
def show_results(score):
    screen.fill((0, 0, 0))
    result_text = font.render(f"You collected {score} stars! 🥇", True, (255, 255, 255))
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(5000)

# Main game loop
def main(character_name, scene_name):
    # Load assets
    background = load_scene_background(scene_name)
    player = Player(character_name)
    all_sprites = pygame.sprite.Group(player)
    stars = pygame.sprite.Group()
    for _ in range(10):
        position = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 100))
        star = Star(position)
        stars.add(star)

    # Load sounds
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)
    collect_sound = pygame.mixer.Sound(SOUND_EFFECT_PATH)

    # Timer
    start_ticks = pygame.time.get_ticks()
    total_time = 30  # seconds
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, total_time - int(seconds))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)

        # Check for star collection
        collected = pygame.sprite.spritecollide(player, stars, True)
        if collected:
            collect_sound.play()
            score += len(collected)

        # Draw everything
        screen.blit(background, (0, 0))
        stars.draw(screen)
        all_sprites.draw(screen)

        # Draw timer and score
        timer_text = font.render(f"Time Left: {remaining_time}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        screen.blit(score_text, (10, 50))

        pygame.display.flip()

        if remaining_time == 0:
            running = False

    pygame.mixer.music.stop()
    show_results(score)
    pygame.quit()
    sys.exit()

# Test mode
if __name__ == "__main__":
    main("bunny", "evening")
