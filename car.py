import pygame
import random
import serial
from pygame import mixer
import sys


class Character:
    def __init__(self, image):
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.generate_random_position()

    def generate_random_position(self):
        self.rect.x = random.randint(156, 640)
        self.rect.y = 0

    def move_down(self):
        self.rect.y += 5


# Replace first argument of serial.Serial with the port of your Arduino
if len(sys.argv) > 0:
    print(sys.argv)
    ser = serial.Serial(sys.argv[0], 9600)
else:
    ser = serial.Serial('COM3', 9600)

pygame.init()
mixer.init()
mixer.music.load("car_acceleration.mp3")
print("Music file loaded")
mixer.music.set_volume(0.5)
print("Music file volume srt")
# Screen dimensions
s_width, s_height = 800, 600
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Car game")

# Load character images and create Character instances
char_img = pygame.image.load("car1.png")
char_semi_img1 = Character(pygame.image.load("motobike1.png"))
char_semi_img2 = Character(pygame.image.load("motorbike2.png"))
char_semi_img = Character(pygame.image.load("car1.png"))

char_img = pygame.transform.scale(char_img, (50, 50))
char_rect = char_img.get_rect()
char_rect.center = (s_width // 2, s_height // 2)

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Game variables
random_char = None
game_over = False


def game_over_screen():
    # Create a white rectangle as the background
    game_over_rect = pygame.Rect(s_width // 4, s_height // 4, s_width // 2, s_height // 2)
    pygame.draw.rect(screen, (255, 255, 255), game_over_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
    text_rect = text.get_rect(center=(s_width // 2, s_height // 2))

    screen.blit(text, text_rect)


bg = pygame.image.load("road.png")
bg = pygame.transform.scale(bg, (800, 600))
score = 0


def score_count(count, score=0):
    score = score + count
    font = pygame.font.Font(None, 36)
    text = font.render(str(score), True, (255, 0, 0))
    text_rect = text.get_rect(center=(50, 18))

    screen.blit(text, text_rect)


score_update_time = pygame.time.get_ticks()  # Store the time when the score was last updated
score_interval = 200  # 1000 milliseconds (1 second)

# Set the game loop
# Set the game loop
running = True
mixer.music.play(loops=1000)
while running:
    joystick_data = ser.readline().decode().strip().split(',')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        game_over = False
        char_rect.center = (s_width // 2, s_height // 2)
        random_char = None
        score = 0  # Reset the score when restarting

    if not game_over:

        if len(joystick_data) == 2:
            joystick_x, joystick_y = map(int, joystick_data)
            if joystick_x != 500 or joystick_y != 500:
                char_rect.x += int((joystick_x - 500) / 10)
                char_rect.y += int((joystick_y - 500) / 10)
                # Limit the car's movement within the screen boundaries
                char_rect.x = max(char_rect.x, 0)
                char_rect.x = min(char_rect.x, s_width - char_rect.width)
                char_rect.y = max(char_rect.y, 0)
                char_rect.y = min(char_rect.y, s_height - char_rect.height)

        if random_char is None or random_char.rect.y >= s_height:
            random_char = random.choice([char_semi_img1, char_semi_img2, char_semi_img])
            random_char.generate_random_position()

        random_char.move_down()

        if char_rect.colliderect(random_char.rect):
            game_over = True

        # Check if it's time to update the score (every second)
        current_time = pygame.time.get_ticks()
        if current_time - score_update_time >= score_interval:
            score += 1
            score_update_time = current_time

    # Update the screen
    screen.blit(bg, (0, 0))
    screen.blit(char_img, char_rect)

    if not game_over:

        screen.blit(random_char.image, random_char.rect)
    else:
        mixer.music.stop()
        game_over_screen()

    # Display the score
    score_count(score)

    pygame.display.flip()

    clock.tick(FPS)

# Quit the game
pygame.quit()
