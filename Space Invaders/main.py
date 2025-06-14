import pygame
import sys
import random
import math
import os # Import the os module for path manipulation
from pygame import mixer

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define the folder paths for your assets
# IMPORTANT: Make sure these paths correctly point to your "images" and "sounds" folders
# within the newly renamed "Space Invaders" directory.
# Example on Windows: "C:\\Users\\mathe\\Desktop\\Space Invaders\\images"
# Example on macOS/Linux: "/Users/mathe/Desktop/Space Invaders/images"
image_folder = "C:\\Users\\mathe\\Desktop\\Space Invaders\\images" # <--- UPDATED PATH
sound_folder = "C:\\Users\\mathe\\Desktop\\Space Invaders\\sounds" # <--- UPDATED PATH

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Global image variables (will be loaded or set to fallback surfaces)
player_img = None
enemy_img1 = None
enemy_img2 = None
enemy_img3 = None
boss_img = None
bullet_img = None
enemy_bullet_img = None
double_bullet_img = None
speed_boost_img = None
background = None

# Global sound variables (will be loaded or left as None if error)
laser_sound = None
explosion_sound = None
powerup_sound = None
background_music_loaded = False # Flag to check if background music loaded successfully

# Load images with proper error handling
try:
    # Player spaceship
    player_img = pygame.image.load(os.path.join(image_folder, "player_ship.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (50, 40))

    # Enemy images
    enemy_img1 = pygame.image.load(os.path.join(image_folder, "enemy1.png")).convert_alpha()
    enemy_img1 = pygame.transform.scale(enemy_img1, (40, 40))

    enemy_img2 = pygame.image.load(os.path.join(image_folder, "enemy2.png")).convert_alpha()
    enemy_img2 = pygame.transform.scale(enemy_img2, (40, 40))

    enemy_img3 = pygame.image.load(os.path.join(image_folder, "enemy3.png")).convert_alpha()
    enemy_img3 = pygame.transform.scale(enemy_img3, (40, 40))

    # Boss enemy
    boss_img = pygame.image.load(os.path.join(image_folder, "boss.png")).convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (80, 60))

    # Bullet - increased size
    bullet_width = 10
    bullet_height = 20
    bullet_img = pygame.image.load(os.path.join(image_folder, "bullet.png")).convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (bullet_width, bullet_height))

    # Enemy bullet - increased size
    enemy_bullet_img = pygame.image.load(os.path.join(image_folder, "enemy_bullet.png")).convert_alpha()
    enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (bullet_width, bullet_height))

    # Power-ups
    double_bullet_img = pygame.image.load(os.path.join(image_folder, "double_bullet_powerup.png")).convert_alpha()
    double_bullet_img = pygame.transform.scale(double_bullet_img, (20, 20))

    speed_boost_img = pygame.image.load(os.path.join(image_folder, "speed_boost_powerup.png")).convert_alpha()
    speed_boost_img = pygame.transform.scale(speed_boost_img, (20, 20))

    # Background
    background = pygame.image.load(os.path.join(image_folder, "background.png")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

except Exception as e:
    print(f"Error loading images: {e}")
    print("Falling back to colored shapes for assets.")
    # Fall back to colored shapes if image loading fails
    player_img = pygame.Surface((50, 40))
    player_img.fill(GREEN)

    enemy_img1 = pygame.Surface((40, 40))
    enemy_img1.fill(RED)
    enemy_img2 = pygame.Surface((40, 40))
    enemy_img2.fill(BLUE)
    enemy_img3 = pygame.Surface((40, 40))
    enemy_img3.fill(YELLOW)

    boss_img = pygame.Surface((80, 60))
    boss_img.fill(PURPLE)

    bullet_width = 10
    bullet_height = 20
    bullet_img = pygame.Surface((bullet_width, bullet_height))
    bullet_img.fill(WHITE)

    enemy_bullet_img = pygame.Surface((bullet_width, bullet_height))
    enemy_bullet_img.fill(RED)

    double_bullet_img = pygame.Surface((20, 20))
    double_bullet_img.fill(CYAN)
    speed_boost_img = pygame.Surface((20, 20))
    speed_boost_img.fill(ORANGE)

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

# Load sounds
try:
    # Background music
    mixer.music.load(os.path.join(sound_folder, "background.wav")) # <--- UPDATED
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
    background_music_loaded = True

    # Sound effects
    laser_sound = mixer.Sound(os.path.join(sound_folder, "laser.wav")) # <--- UPDATED
    explosion_sound = mixer.Sound(os.path.join(sound_folder, "explosion.wav")) # <--- UPDATED
    powerup_sound = mixer.Sound(os.path.join(sound_folder, "powerup.wav")) # <--- UPDATED

    # Set volume for sound effects
    laser_sound.set_volume(0.4)
    explosion_sound.set_volume(0.6)
    powerup_sound.set_volume(0.5)
except Exception as e:
    print(f"Error loading sounds: {e}")
    print("Continuing without sound effects and background music.")
    # Set sound objects to None if loading fails, so we can check before playing
    laser_sound = None
    explosion_sound = None
    powerup_sound = None
    background_music_loaded = False


# Game variables
clock = pygame.time.Clock()
FPS = 60

# Player
class Player:
    def __init__(self):
        self.img = player_img
        self.width = 50
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.double_bullet = False
        self.speed_boost_timer = 0 # Frames remaining for speed boost
        self.double_bullet_timer = 0 # Frames remaining for double bullet
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0 # Frames remaining for invincibility

    def draw(self):
        # Blinking effect when invincible
        if not self.invincible or pygame.time.get_ticks() % 200 < 100:
            screen.blit(self.img, (self.x, self.y))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def update(self):
        # Update power-up timers
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = 5  # Reset speed

        if self.double_bullet_timer > 0:
            self.double_bullet_timer -= 1
            if self.double_bullet_timer == 0:
                self.double_bullet = False

        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False

# Enemy
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.enemy_type = enemy_type
        if enemy_type == 1:
            self.img = enemy_img1
            self.points = 10
        elif enemy_type == 2:
            self.img = enemy_img2
            self.points = 20
        else: # enemy_type == 3
            self.img = enemy_img3
            self.points = 30

        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = 1  # 1 for right, -1 for left

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.speed * self.direction

    def descend(self):
        self.y += 20 # Amount to descend when hitting screen edge

# Boss Enemy
class BossEnemy:
    def __init__(self):
        self.img = boss_img
        self.width = 80
        self.height = 60
        # Start the boss in a visible position
        self.x = WIDTH // 2 - self.width // 2
        self.y = 50
        self.speed = 2
        self.health = 10
        self.direction = 1 # 1 for right, -1 for left
        self.shoot_timer = 0
        self.reset_shoot_timer() # Initialize first shoot timer

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.direction *= -1 # Reverse direction

        # Random vertical movement (keeps boss more dynamic)
        self.y += random.choice([-1, 0, 1])
        if self.y < 30: # Prevent going too high
            self.y = 30
        if self.y > 150: # Prevent going too low
            self.y = 150

    def update(self):
        self.move()
        self.shoot_timer -= 1
        # Return True if it's time to shoot
        return self.shoot_timer <= 0

    def reset_shoot_timer(self):
        self.shoot_timer = random.randint(30, 60) # Shoot every 0.5 to 1 second

# Bullet
class Bullet:
    def __init__(self, x, y, direction=-1, is_enemy=False):
        # Use the global image variables
        self.img = enemy_bullet_img if is_enemy else bullet_img
        self.width = bullet_width
        self.height = bullet_height
        # Adjust x to center bullet on object that shot it
        self.x = x - self.width // 2
        self.y = y
        self.speed = 7
        self.direction = direction  # -1 for up (player), 1 for down (enemy)
        self.is_enemy = is_enemy

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.speed * self.direction

    def off_screen(self):
        return self.y < -self.height or self.y > HEIGHT + self.height

# Shield Block
class ShieldBlock:
    def __init__(self, x, y):
        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.health = 3
        self.colors = [RED, YELLOW, GREEN] # Colors from low (1) to high (3) health

    def draw(self):
        # Index into colors based on remaining health (health-1 for 0-2 index)
        pygame.draw.rect(screen, self.colors[self.health - 1], (self.x, self.y, self.width, self.height))

    def hit(self):
        self.health -= 1
        return self.health <= 0

# Power-up
class PowerUp:
    def __init__(self, x, y, power_type):
        self.power_type = power_type  # 0 for double bullet, 1 for speed boost
        self.img = double_bullet_img if power_type == 0 else speed_boost_img
        self.width = 20
        self.height = 20
        self.x = x - self.width // 2 # Center power-up
        self.y = y
        self.speed = 2

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > HEIGHT

# Button class for menu
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 36)
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click # mouse_click usually refers to event.button == 1 (left click)

# Game state
class Game:
    def __init__(self):
        self.state = "menu"  # menu, playing, game_over, victory
        self.game_mode = None  # "classic" or "unlimited"
        self.classic_max_level = 5 # Defines the max level for classic mode
        self.boss_level_interval = 5  # Boss appears every 5 levels (i.e., level 5, 10, 15 etc.)
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)

        # Create menu buttons
        button_width = 300
        button_height = 60
        button_x = WIDTH // 2 - button_width // 2

        self.classic_button = Button(
            button_x, HEIGHT // 2 - 50,
            button_width, button_height,
            "Classic Mode (5 Levels)",
            (50, 50, 150), (100, 100, 200)
        )

        self.unlimited_button = Button(
            button_x, HEIGHT // 2 + 50,
            button_width, button_height,
            "Unlimited Mode",
            (150, 50, 50), (200, 100, 100)
        )

        # Call reset_game_state to initialize all dynamic game elements
        self.reset_game_state()

    def start_new_game(self, mode):
        """Prepares and starts a new game session with the specified mode."""
        self.reset_game_state() # Clear previous game state
        self.game_mode = mode
        self.state = "playing"
        # Initial setup for the first level
        if self.level % self.boss_level_interval == 0:
            print(f"Starting game on Boss level {self.level}!")
            self.boss = BossEnemy()
            # Scale boss based on its tier (which is level/interval)
            boss_tier = self.level // self.boss_level_interval
            self.boss.health = 10 + (boss_tier - 1) * 5
            self.boss.speed = 2 + (boss_tier - 1) * 0.5
            self.shields = [] # No shields on boss levels
        else:
            print(f"Starting game on regular level {self.level}!")
            self.create_enemies()
            self.create_shields()


    def reset_game_state(self):
        """Resets all game-specific variables to their initial values."""
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.shields = []
        self.power_ups = []
        self.boss = None
        self.score = 0
        self.level = 1
        # Note: self.game_mode is set by menu selection, not reset here

    def create_enemies(self):
        self.enemies = [] # Ensure previous enemies are cleared
        rows = 5
        cols = 11
        # Base enemy speed for the level, capped to avoid excessively fast enemies
        current_enemy_speed = 1 + (self.level - 1) * 0.2
        if current_enemy_speed > 5: # Cap enemy speed if it gets too high
            current_enemy_speed = 5

        for row in range(rows):
            for col in range(cols):
                x = 100 + col * 50
                y = 50 + row * 50
                enemy_type = 3 - (row // 2)  # Different enemy types based on row (3, 2, 1, 1, 1)
                enemy = Enemy(x, y, enemy_type)
                enemy.speed = current_enemy_speed # Apply level-based speed
                self.enemies.append(enemy)

    def create_shields(self):
        self.shields = [] # Ensure previous shields are cleared
        shield_width = 80 # Width of a single shield structure (for positioning)
        shield_y = HEIGHT - 150

        # Define positions for 4 shield structures
        for shield_base_x in [100, 300, 500, 700]:
            # Create individual blocks for each shield structure
            for row in range(6):
                for col in range(8):
                    # These conditions define the arch shape of the shield
                    if not (row == 0 and (col < 2 or col > 5)) and \
                       not (row == 1 and (col == 0 or col == 7)): # Small gaps on 2nd row too
                        x = shield_base_x - (shield_width / 2) + col * 10
                        y = shield_y + row * 10
                        self.shields.append(ShieldBlock(x, y))

    def check_collisions(self):
        # Player bullets with enemies
        # Iterate over a copy of the list to allow safe removal from the original
        bullets_to_remove = []
        enemies_to_remove = []
        powerups_to_add = []

        for bullet in self.bullets:
            if bullet.is_enemy: # This loop is for player bullets only
                continue

            # Check collision with enemies
            enemy_hit = False
            for enemy in self.enemies:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):

                    enemies_to_remove.append(enemy)
                    self.score += enemy.points

                    # Chance to drop power-up
                    if random.random() < 0.15:  # 15% chance
                        power_type = random.randint(0, 1) # 0 for double bullet, 1 for speed boost
                        powerups_to_add.append(PowerUp(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, power_type))

                    if explosion_sound: # Play sound only if loaded
                        explosion_sound.play()
                    enemy_hit = True
                    break # Bullet hit an enemy, so it's gone. No need to check other enemies for this bullet.

            if enemy_hit:
                bullets_to_remove.append(bullet)
                continue # Go to the next player bullet

            # Check player bullets with boss
            if self.boss:
                if (bullet.x < self.boss.x + self.boss.width and
                    bullet.x + bullet.width > self.boss.x and
                    bullet.y < self.boss.y + self.boss.height and
                    bullet.y + bullet.height > self.boss.y):

                    bullets_to_remove.append(bullet)
                    self.boss.health -= 1

                    if self.boss.health <= 0:
                        boss_tier = self.level // self.boss_level_interval
                        self.score += 500 * boss_tier  # Higher score for later bosses
                        self.boss = None # Boss is defeated!
                        if explosion_sound:
                            explosion_sound.play()
                        # Level progression will be handled by the main update loop after this
                    continue # Bullet hit boss, no need to check shields for this bullet

            # Player bullets with shields
            for shield in self.shields:
                if (bullet.x < shield.x + shield.width and
                    bullet.x + bullet.width > shield.x and
                    bullet.y < shield.y + shield.height and
                    bullet.y + bullet.height > shield.y):
                    if shield.hit():
                        self.shields.remove(shield) # Remove from shields directly
                    bullets_to_remove.append(bullet)
                    break # Bullet hit a shield, so it's gone.

        # Apply removals for player bullets and enemies
        for bullet in bullets_to_remove:
            if bullet in self.bullets: self.bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in self.enemies: self.enemies.remove(enemy)
        self.power_ups.extend(powerups_to_add) # Add new power-ups

        # Enemy bullets with player
        enemy_bullets_to_remove = []
        if not self.player.invincible:
            for bullet in self.enemy_bullets:
                if (bullet.x < self.player.x + self.player.width and
                    bullet.x + bullet.width > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + bullet.height > self.player.y):

                    enemy_bullets_to_remove.append(bullet)
                    self.player.lives -= 1
                    self.player.invincible = True
                    self.player.invincible_timer = 120  # 2 seconds at 60 FPS

                    if explosion_sound: # Play sound only if loaded
                        explosion_sound.play()

                    if self.player.lives <= 0:
                        self.state = "game_over"
                    break # Player hit, no need to check other enemy bullets for this frame

        # Enemy bullets with shields
        for bullet in self.enemy_bullets:
            if bullet in enemy_bullets_to_remove: # Already marked for removal (e.g., hit player)
                continue

            for shield in self.shields:
                if (bullet.x < shield.x + shield.width and
                    bullet.x + bullet.width > shield.x and
                    bullet.y < shield.y + shield.height and
                    bullet.y + bullet.height > shield.y):
                    if shield.hit():
                        self.shields.remove(shield) # Remove from shields directly
                    enemy_bullets_to_remove.append(bullet)
                    break # Bullet hit a shield, so it's gone.

        # Apply removals for enemy bullets
        for bullet in enemy_bullets_to_remove:
            if bullet in self.enemy_bullets: self.enemy_bullets.remove(bullet)

        # Power-ups with player
        powerups_collected_to_remove = []
        for power_up in self.power_ups:
            if (power_up.x < self.player.x + self.player.width and
                power_up.x + power_up.width > self.player.x and
                power_up.y < self.player.y + self.player.height and
                power_up.y + power_up.height > self.player.y):

                powerups_collected_to_remove.append(power_up)

                if power_up.power_type == 0:  # Double bullet
                    self.player.double_bullet = True
                    self.player.double_bullet_timer = 600  # 10 seconds (60 FPS * 10)
                else:  # Speed boost
                    self.player.speed = 8
                    self.player.speed_boost_timer = 600  # 10 seconds

                if powerup_sound: # Play sound only if loaded
                    powerup_sound.play()
                break # Player can only pick up one power-up at a time (if multiple overlap)

        # Apply removals for collected power-ups
        for power_up in powerups_collected_to_remove:
            if power_up in self.power_ups: self.power_ups.remove(power_up)


    def update(self):
        if self.state == "menu":
            # Update menu (check button hover)
            mouse_pos = pygame.mouse.get_pos()
            self.classic_button.check_hover(mouse_pos)
            self.unlimited_button.check_hover(mouse_pos)
            return

        if self.state != "playing":
            return # Only update game logic if playing

        # Update player
        self.player.update()

        # Update bullets
        # Iterate over copies to allow removal while looping
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.off_screen():
                self.enemy_bullets.remove(bullet)

        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.move()
            if power_up.off_screen():
                self.power_ups.remove(power_up)

        # Update enemies
        move_down = False
        for enemy in self.enemies:
            enemy.move()
            # Check if any enemy hits the screen edge
            if enemy.x <= 0 or enemy.x >= WIDTH - enemy.width:
                move_down = True
                break # A single enemy hitting the edge is enough to trigger descent for all


        if move_down:
            for enemy in self.enemies:
                enemy.direction *= -1 # Reverse horizontal direction
                enemy.descend() # Move down

        # Random enemy shooting (only if there are regular enemies and no boss)
        if self.enemies and not self.boss and random.random() < 0.015 + (self.level * 0.001): # Increased chance with level
            shooting_enemy = random.choice(self.enemies)
            self.enemy_bullets.append(
                Bullet(
                    shooting_enemy.x + shooting_enemy.width // 2,
                    shooting_enemy.y + shooting_enemy.height,
                    1, # Direction down
                    True # is_enemy bullet
                )
            )

        # Boss logic
        if self.boss:
            if self.boss.update(): # Returns True when it's time to shoot
                self.boss.reset_shoot_timer()
                # Boss shoots 3 bullets in a spread
                for offset in [-15, 0, 15]: # Spread out the bullets more
                    self.enemy_bullets.append(
                        Bullet(
                            self.boss.x + self.boss.width // 2 + offset,
                            self.boss.y + self.boss.height,
                            1, # Direction down
                            True # is_enemy bullet
                        )
                    )

        # Check collisions (after all movements for the frame)
        self.check_collisions()

        # Check if enemies reached bottom (game over condition)
        for enemy in self.enemies:
            if enemy.y + enemy.height > HEIGHT - 50: # If enemy goes too low
                self.state = "game_over"
                break

        # Level progression / Victory conditions
        # This block determines what happens after enemies/boss are cleared
        if not self.enemies and not self.boss: # This means the current wave (either aliens or boss) is cleared

            if self.game_mode == "classic":
                if self.level == self.classic_max_level: # If it was the final level (Level 5) and boss is gone
                    self.state = "victory" # Game wins!
                    print("Classic Mode Completed!")
                    return # Exit update, game is won
                else: # Advance to the next level in Classic Mode
                    self.level += 1
                    print(f"Advancing to Classic level {self.level}")
                    # Check if the NEXT level is a boss level (which will be Level 5 in Classic Mode)
                    if self.level == self.classic_max_level: # Specifically for Level 5 in Classic
                        print(f"Classic Mode Level {self.level} - Boss incoming!")
                        self.boss = BossEnemy()
                        # Scale boss based on its tier (which for classic is just 1)
                        self.boss.health = 10 # Default boss health for Classic Mode final boss
                        self.boss.speed = 2 # Default boss speed
                        self.shields = [] # No shields on boss levels
                    else: # Regular Classic level
                        self.create_enemies()
                        self.create_shields()

            elif self.game_mode == "unlimited":
                self.level += 1
                print(f"Advancing to Unlimited level {self.level}")

                # Check if this is a boss level for Unlimited mode
                if self.level % self.boss_level_interval == 0:
                    print(f"Boss level {self.level} reached! Creating boss...")
                    self.boss = BossEnemy()
                    # Make the boss stronger with each boss level appearance
                    boss_tier = self.level // self.boss_level_interval
                    self.boss.health = 10 + (boss_tier - 1) * 5 # Base 10 HP + 5 for each tier
                    self.boss.speed = 2 + (boss_tier - 1) * 0.5 # Base 2 speed + 0.5 for each tier
                    self.shields = [] # No shields on boss levels
                else:
                    self.create_enemies() # Regular level - create standard enemies
                    self.create_shields() # Re-create shields

    def draw(self):
        # Draw background
        screen.blit(background, (0, 0))

        if self.state == "menu":
            # Draw menu screen
            title = self.big_font.render("SPACE INVADERS", True, WHITE)
            # Adjusted Y-coordinate to move the title higher
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))

            # Draw mode selection text
            select_text = self.font.render("Select Game Mode:", True, WHITE)
            screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - 120))

            # Draw buttons
            self.classic_button.draw()
            self.unlimited_button.draw()

        elif self.state == "game_over":
            # Draw game over screen
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            level_text = self.font.render(f"Level Reached: {self.level}", True, WHITE)
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            menu_text = self.font.render("Press M for Main Menu", True, WHITE)

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 + 10))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 90))

        elif self.state == "victory":
            # Draw victory screen
            victory_text = self.big_font.render("VICTORY!", True, GREEN)
            congrats_text = self.font.render("Congratulations! You've completed Classic Mode!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            menu_text = self.font.render("Press M for Main Menu", True, WHITE)

            screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 4))
            screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 50))

        else:  # playing state
            # Draw player
            self.player.draw()

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw()

            # Draw boss
            if self.boss:
                self.boss.draw()
                # Draw boss health for better visibility
                boss_health_text = self.font.render(f"Boss HP: {self.boss.health}", True, RED)
                screen.blit(boss_health_text, (WIDTH // 2 - boss_health_text.get_width() // 2, 70))

            # Draw bullets
            # Combine lists for drawing efficiency
            for bullet in self.bullets + self.enemy_bullets:
                bullet.draw()

            # Draw shields
            for shield in self.shields:
                shield.draw()

            # Draw power-ups
            for power_up in self.power_ups:
                power_up.draw()

            # Draw HUD (Score, Level, Lives)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)

            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))
            screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

            # Draw game mode indicator
            mode_display_text = "Classic" if self.game_mode == "classic" else "Unlimited"
            mode_text = self.font.render(f"Mode: {mode_display_text}", True, CYAN)
            screen.blit(mode_text, (10, 40))

            # Draw power-up indicators with timers
            if self.player.double_bullet:
                # Calculate remaining seconds for display
                remaining_time_double = max(0, self.player.double_bullet_timer // FPS)
                double_text = self.font.render(f"Double Bullets ({remaining_time_double}s)", True, CYAN)
                screen.blit(double_text, (10, HEIGHT - 30))

            if self.player.speed > 5: # Speed is boosted if > original 5
                # Calculate remaining seconds for display
                remaining_time_speed = max(0, self.player.speed_boost_timer // FPS)
                speed_text = self.font.render(f"Speed Boost ({remaining_time_speed}s)", True, ORANGE)
                screen.blit(speed_text, (WIDTH - speed_text.get_width() - 10, HEIGHT - 30))

            # Draw boss level indicator
            if self.level % self.boss_level_interval == 0 and self.boss: # Only show if it's a boss level AND boss is present
                boss_indicator_text = self.font.render("BOSS LEVEL!", True, RED)
                screen.blit(boss_indicator_text, (WIDTH // 2 - boss_indicator_text.get_width() // 2, 40))

# Create game instance
game = Game()

# Main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
            # Check for button clicks in menu
            if game.state == "menu":
                mouse_pos = pygame.mouse.get_pos()
                if game.classic_button.is_clicked(mouse_pos, True):
                    game.start_new_game("classic")
                elif game.unlimited_button.is_clicked(mouse_pos, True):
                    game.start_new_game("unlimited")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.state == "playing":
                # Fire bullet
                if laser_sound: # Play sound only if loaded
                    laser_sound.play()

                if game.player.double_bullet:
                    # Adjust positions for double bullets to be next to player ship
                    game.bullets.append(Bullet(game.player.x + 10, game.player.y))
                    game.bullets.append(Bullet(game.player.x + game.player.width - 10, game.player.y))
                else:
                    game.bullets.append(Bullet(game.player.x + game.player.width // 2, game.player.y))

            elif event.key == pygame.K_r and game.state == "game_over":
                # Restart game with same mode
                if game.game_mode: # Only restart if a mode was previously selected
                    game.start_new_game(game.game_mode)
                else: # Fallback to menu if no mode was set (shouldn't happen with current flow)
                    game.state = "menu"
                    game.reset_game_state()


            elif event.key == pygame.K_m and (game.state == "game_over" or game.state == "victory"):
                # Return to main menu
                game.state = "menu"
                game.reset_game_state() # Reset game elements when returning to menu

    # Handle continuous player movement when keys are held down
    if game.state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.player.move("left")
        if keys[pygame.K_RIGHT]:
            game.player.move("right")

    # Update game state
    game.update()

    # Draw everything
    game.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()