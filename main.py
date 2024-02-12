import pygame
import random
import time

# Initialize the game
pygame.init()

# Set the screen size to the full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set the screen width and height
width, height = pygame.display.get_surface().get_size()

# Set the screen title
pygame.display.set_caption("Monster Attack")

# Set the background color
screen.fill((255, 255, 255))


#load level images
level_images = []
level_images.append(pygame.image.load("level-01.jpg"))
level_images.append(pygame.image.load("level-02.jpg"))
level_images.append(pygame.image.load("level-03.jpg"))
level_images.append(pygame.image.load("level-04.jpg"))
level_images.append(pygame.image.load("level-05.jpg"))
level_images.append(pygame.image.load("level-06.jpg"))
level_images.append(pygame.image.load("spider-level-07.jpg"))
#scale level images
for i in range(len(level_images)):
    width = 100
    height = 100
    level_images[i] = pygame.transform.scale(level_images[i], (width, height))

laser_image = pygame.transform.scale(pygame.image.load("laser.webp"), (50, 50))
laser_dead_image = pygame.transform.scale(laser_image, (50, 10))  # Example scaling for "squashed" state

# At the beginning of your game setup, after loading other assets
spider_image = pygame.transform.scale(pygame.image.load("spider.webp"), (400, 400))
spider_dead_image = pygame.transform.scale(spider_image, (400, 100))  # Example dead image scaling







class Enemy:
    def __init__(self, x, y, health, image, dead_image, arm_image=None, is_spider=False):
        self.x = x
        self.y = y
        self.is_spider = is_spider
        self.health = health
        self.image = image
        self.attacking = False  # Add an attacking flag
        self.dead_image = dead_image
        self.arm_image = arm_image  # New attribute for the arm image
        self.dead = False
        self.attack_frame = 0  # Tracks the attack animation frame
        self.max_health = health

    def move_towards_player(self, player):
        if not self.dead and not player.dead:
            dx, dy = player.x - self.x, player.y - self.y
            dist = max(abs(dx), abs(dy))
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * .1 * level  # Slower movement rate
                self.y += dy * .1 * level
                    

    def attack_player(self, player):
        # Check if close enough to attack
        
        if not self.dead and not player.dead: 
            print("attacking", self.x, self.y, player.x, player.y, self.dead, player.dead)
            attack_distance = 50
            
            if abs(self.x - player.x) < attack_distance and abs(self.y - player.y) < attack_distance and not self.dead:
                self.attacking = True
                player.hit()  # Reduce player health
            else:
                self.attacking = False

    def draw(self, screen):
        if self.dead:
            screen.blit(self.dead_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

            if not self.is_spider:
                # Always draw the arm to the side, even if not attacking
                arm_offset_x = self.image.get_width()  # Place the arm to the right side of the enemy
                arm_offset_y = self.image.get_height() // 4  # Adjust vertical position if needed
                arm_x = self.x + arm_offset_x
                arm_y = self.y + arm_offset_y
                screen.blit(self.arm_image, (arm_x, arm_y))
            if self.is_spider:
                self.draw_health_bar(screen)

            # Animate the arm when attacking
            if self.attacking and not self.is_spider:
                # Example animation: Move the arm up and down
                self.attack_frame += 1  # Increment the frame count
                if self.attack_frame <= 5:
                    # Move arm upwards for the first 5 frames
                    arm_y -= 5  # Adjust value for noticeable movement
                elif self.attack_frame <= 10:
                    # Move arm downwards for the next 5 frames
                    arm_y += 5  # Adjust value for noticeable movement
                else:
                    # Reset the frame count after 10 frames to loop the animation
                    self.attack_frame = 0

                # Draw the animated arm
                screen.blit(self.arm_image, (arm_x, arm_y))

    def draw_health_bar(self, screen):
        # Define the health bar's size and position
        bar_width = 400 * (self.health / self.max_health)  # Assuming max health is initialized
        bar_height = 20  # Health bar height
        bar_x = self.x + (self.image.get_width() / 2) - (bar_width / 2)
        bar_y = self.y - bar_height - 10

        # Draw the health bar background
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, 400, bar_height))
        # Draw the current health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width, bar_height))


    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.dead = True

    def is_dead(self):
        return self.dead


zombie_image = pygame.transform.scale(pygame.image.load("zombie.jpg"), (100, 100))
zombie_dead_image = pygame.transform.scale(zombie_image, (100, 10))

bat_image = pygame.transform.scale(pygame.image.load("bat.webp"), (100, 100))
bat_dead_image = pygame.transform.scale(bat_image, (100, 10))

# Load and scale images for dragon, ghost, pumpkin, skeleton
dragon_image = pygame.transform.scale(pygame.image.load("dragon.webp"), (100, 100))
dragon_dead_image = pygame.transform.scale(dragon_image, (100, 10))  # Example scaling for dead image

ghost_image = pygame.transform.scale(pygame.image.load("ghost.jpg"), (100, 100))
ghost_dead_image = pygame.transform.scale(ghost_image, (100, 10))  # Example scaling for dead image

pumpkin_image = pygame.transform.scale(pygame.image.load("pumpkin.jpg"), (100, 100))
pumpkin_dead_image = pygame.transform.scale(pumpkin_image, (100, 10))  # Example scaling for dead image

skeleton_image = pygame.transform.scale(pygame.image.load("skeleton.webp"), (100, 100))
skeleton_dead_image = pygame.transform.scale(skeleton_image, (100, 10))  # Example scaling for dead image

# Load and scale arm images
zombie_arm_image = pygame.transform.scale(pygame.image.load("zombie-arm.jpg"), (50, 50))
bat_arm_image = pygame.transform.scale(pygame.image.load("bat-arm.jpg"), (50, 50))
dragon_arm_image = pygame.transform.scale(pygame.image.load("dragon-arm.jpg"), (50, 50))
ghost_arm_image = pygame.transform.scale(pygame.image.load("ghost-arm.jpg"), (50, 50))
pumpkin_arm_image = pygame.transform.scale(pygame.image.load("pumpkin-arm.jpg"), (50, 50))
skeleton_arm_image = pygame.transform.scale(pygame.image.load("skeleton-arm.jpg"), (50, 50))



#random zombie locations
zombie_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    zombie_locations.append((x, y))

#random bat locations
bat_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    bat_locations.append((x, y))

# Repeat for other enemy types
dragon_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    dragon_locations.append((x, y))

ghost_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    ghost_locations.append((x, y))

pumpkin_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    pumpkin_locations.append((x, y))

skeleton_locations = []
for i in range(5):
    x = random.randint(0, screen.get_width() - 100)
    y = random.randint(0, screen.get_height() - 100)
    skeleton_locations.append((x, y))


# Create enemies
    
enemies = []
# Assuming zombie_locations, bat_locations, etc., are defined similarly to before
for x, y in zombie_locations:
    enemies.append(Enemy(x, y, 2, zombie_image, zombie_dead_image, zombie_arm_image))

for x, y in bat_locations:
    enemies.append(Enemy(x, y, 2, bat_image, bat_dead_image, bat_arm_image))

for x, y in dragon_locations:
    enemies.append(Enemy(x, y, 2, dragon_image, dragon_dead_image, dragon_arm_image))

for x, y in ghost_locations:
    enemies.append(Enemy(x, y, 2, ghost_image, ghost_dead_image, ghost_arm_image))

for x, y in pumpkin_locations:
    enemies.append(Enemy(x, y, 2, pumpkin_image, pumpkin_dead_image, pumpkin_arm_image))

for x, y in skeleton_locations:
    enemies.append(Enemy(x, y, 2, skeleton_image, skeleton_dead_image, skeleton_arm_image))

debug = False

def reset_or_populate_enemies(enemies, level, populate_new_level=False):
    if populate_new_level:
        # Completely clear the enemies list for a fresh start
        enemies.clear()

        if level == 7:
            # Create the special spider enemy for level 7
            x = random.randint(0, screen.get_width() - 400)
            y = random.randint(0, screen.get_height() - 400)
            spider = Enemy(x, y, 1000, spider_image, spider_dead_image, None, is_spider=True)
            enemies.append(spider)
        else: # Populate regular enemies for other levels

            if debug:
                num_new_enemies = 1  # Example: Keep the enemy count low for debugging
            else:
                num_new_enemies = 30 * level  # Example: Increase enemy count with level

            types = ["zombie", "bat", "dragon", "ghost", "pumpkin", "skeleton"]

            for _ in range(num_new_enemies):
                x = random.randint(0, screen.get_width() - 100)
                y = random.randint(0, screen.get_height() - 200)  # Keep them away from the bottom

                this_type = random.choice(types)
                if this_type == "zombie":
                    enemies.append(Enemy(x, y, 2, zombie_image, zombie_dead_image, zombie_arm_image))
                
                elif this_type == "bat":
                    enemies.append(Enemy(x, y, 2, bat_image, bat_dead_image, bat_arm_image))
                
                elif this_type == "dragon":
                    enemies.append(Enemy(x, y, 2, dragon_image, dragon_dead_image, dragon_arm_image))

                elif this_type == "ghost":
                    enemies.append(Enemy(x, y, 2, ghost_image, ghost_dead_image, ghost_arm_image))

                elif this_type == "pumpkin":
                    enemies.append(Enemy(x, y, 2, pumpkin_image, pumpkin_dead_image, pumpkin_arm_image))

                elif this_type == "skeleton":
                    enemies.append(Enemy(x, y, 2, skeleton_image, skeleton_dead_image, skeleton_arm_image))

    else:
        # Reset the existing enemies
        for enemy in enemies:
            if not enemy.dead:
                # Reset the position of each enemy if needed
                enemy.x = random.randint(0, screen.get_width() - 100)
                enemy.y = random.randint(0, screen.get_height() - 200)





class Player:
    def __init__(self, x, y, health, image, dead_image):
        self.x = x
        self.y = y
        self.health = health
        self.image = image
        self.dead_image = dead_image
        self.dead = False
        self.respawn_time = 5  # seconds
        self.death_timestamp = None

    def hit(self):
        if not self.dead:
            self.health -= 1
            if self.health <= 0:
                self.dead = True
                self.death_timestamp = time.time()

    def respawn(self, current_time):
        if self.dead and (current_time - self.death_timestamp >= self.respawn_time):
            self.dead = False
            self.health = 5  # Reset health on respawn
            # Reset position if needed, or handle it outside this method
            # Respawn at a random location at the bottom of the screen
            self.x = random.randint(0, screen.get_width() - self.image.get_width())
            self.y = screen.get_height() - self.image.get_height()
            reset_or_populate_enemies(enemies, level)

    def draw(self, screen):
        if self.dead:
            screen.blit(self.dead_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def move(self, direction):
        if not self.dead:
            if direction == "LEFT":
                self.x -= 10  # Move left
            elif direction == "RIGHT":
                self.x += 10  # Move right
            #if player goes to the edge, don't allow it to go any further
            if self.x < 0:
                self.x = 0
            elif self.x > screen.get_width() - self.image.get_width():
                self.x = screen.get_width() - self.image.get_width()

    def draw_health_bar(self, screen):
        # Draw the health bar above the player's head
        health_bar_width = 50
        health_bar_height = 5
        border_color = (0, 0, 0)
        health_color = (0, 255, 0)
        background_color = (255, 0, 0)
        
        # Background
        pygame.draw.rect(screen, background_color, (self.x, self.y - health_bar_height - 10, health_bar_width, health_bar_height))
        # Health
        health_width = (self.health / 5) * health_bar_width
        pygame.draw.rect(screen, health_color, (self.x, self.y - health_bar_height - 10, health_width, health_bar_height))
        # Optional: Border
        pygame.draw.rect(screen, border_color, (self.x, self.y - health_bar_height - 10, health_bar_width, health_bar_height), 1)


          


class AIHelper(Player):
    def __init__(self, x, y, health, image, dead_image):
        super().__init__(x, y, health, image, dead_image)
        self.shoot_cooldown = 0

    def update(self, enemies, screen):
        # Implement AI movement towards the nearest enemy or strategic positioning
        self.move_automatically(enemies)
        # Implement AI shooting logic
        if self.shoot_cooldown <= 0:
            self.shoot(enemies, screen)
            self.shoot_cooldown = 50  # Adjust cooldown based on desired shooting frequency
        else:
            self.shoot_cooldown -= 1

    def move_automatically(self, enemies):
        # Example: Move towards the nearest enemy
        for enemy in enemies:
            if enemy.dead:
                enemies.remove(enemy)
        if enemies:
            for enemy in enemies:
                x = enemy.x
                if x < self.x:
                    self.x -= 2
                elif x > self.x:
                    self.x += 2
                # if reaches the other side, go back
                if self.x < 0:
                    self.x = 0
                elif self.x > screen.get_width() - self.image.get_width():
                    self.x = screen.get_width() - self.image.get_width()
                

    def shoot(self, enemies, screen):
        # Example: Shoot a laser towards the nearest enemy
        print("AI shooting")
        for enemy in enemies:
            if enemy.dead:
                enemies.remove(enemy)

        if enemies:
            print("AI shooting at enemy")
            print("AI position", self.x, self.y)
            nearest_enemy = min(enemies, key=lambda enemy: (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (nearest_enemy.x, nearest_enemy.y), 2)
            # Implement logic to reduce health of the hit enemy

            # Apply damage to the nearest enemy
            if (nearest_enemy.x - self.x) ** 2 + (nearest_enemy.y - self.y) ** 2 < 400**2:  # Example shooting range
                nearest_enemy.hit()  # Call the hit method on the enemy


# Initialize an empty list for AI helpers
ai_helpers = []




# Initialize the player with a starting position, health, and images
player = Player(screen.get_width() / 2, screen.get_height() - laser_image.get_height(), 5, laser_image, laser_dead_image)




# Set the game loop
running = True
level = 0

# Initialize a variable to store the target position for the laser
laser_target = None

laser_line_duration = 0

while running:
    current_time = time.time()

    # Continuous key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("LEFT")
    if keys[pygame.K_RIGHT]:
        player.move("RIGHT")

    screen.fill((255, 255, 255))  # Clear the screen


    # Within the game setup for level 2 or higher

    ai_x_position = random.randint(0, screen.get_width() - 100)
    #y position is bottom of the screen
    ai_y_position = screen.get_height() - 100
    
    if level == 8:
            # display mission completed
            font = pygame.font.Font(None, 36)
            text = font.render(f"Mission Completed", True, (0, 0, 0))
            screen.blit(text, (width // 2, height // 2))
            pygame.display.update()
            time.sleep(3)
            level = 1
            continue


    # Display level selection or gameplay based on level value
    if level == 0:
        # Display level selection
        for i, img in enumerate(level_images):
            screen.blit(img, (i * 100, 0))
    else:

        
        # Gameplay drawing: player, enemies, and optionally the laser line
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level {level}", True, (0, 0, 0))
        screen.blit(text, (width // 2, 0))

        if laser_target and laser_line_duration > 0:  # Draw the laser line if a target is set and duration is positive
            pygame.draw.line(screen, (255, 0, 0), (player.x + player.image.get_width() // 2, player.y), laser_target)
            laser_line_duration -= 1  # Decrement the duration each frame
           

        
        for enemy in enemies:  # Draw enemies
            enemy.draw(screen)
        
        player.draw(screen)  # Draw the player

        # Inside the game loop, after drawing everything
        player.draw_health_bar(screen)

        # Update and draw AI helpers
        for ai_helper in ai_helpers:
            ai_helper.update(enemies, screen)
            ai_helper.draw(screen)

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Level selection handling
        if level == 0 and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, _ in enumerate(level_images):
                if x >= i * 100 and x < (i + 1) * 100 and y >= 0 and y < 100:
                    level = i + 1  # Set the selected level
                    
                    # Optionally reset or initialize enemies here
                    break

        # Inside the game loop, after setting the laser_target
        if level > 0 and event.type == pygame.MOUSEBUTTONDOWN and not player.dead:  # Add player alive check
            laser_target = pygame.mouse.get_pos()  # Set the laser target
            laser_line_duration = 50  # Example: Show line for 5 frames

            print("Shoot laser")
            # Assuming the player's laser starts from the middle of the player image
            laser_start = (player.x + player.image.get_width() // 2, player.y)
            
            # Hit detection
            for enemy in enemies:
                # Create a simple hitbox for the enemy for this example
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
                # Check if the laser intersects this hitbox (simple approximation)
                if enemy_rect.collidepoint(laser_target):
                    enemy.hit()
                    if enemy.is_dead():
                        print(f"Enemy at ({enemy.x}, {enemy.y}) is dead.")
                        # Optionally remove the enemy from the list or mark it for removal

    if level > 0:
        # Handle enemy movement and attacks
        for enemy in enemies:
            enemy.move_towards_player(player)
            enemy.attack_player(player)


    # Inside the game loop, after updating and drawing everything
    if level > 0 and all(enemy.dead for enemy in enemies):
        level += 1  # Increment the level
        reset_or_populate_enemies(enemies, level, populate_new_level=True)  # Populate new level with enemies

        # Add a new AI helper at the start of each new level
        ai_x_position = player.x + random.randint(-100, 100)  # Adjust for closer positioning
        ai_y_position = player.y + random.randint(-50, 50)  # Adjust for closer positioning
        ai_helper = AIHelper(ai_x_position, ai_y_position, 5, laser_image, laser_dead_image)
        ai_helpers.append(ai_helper)



    # Check for and handle player respawn
    player.respawn(current_time)

    pygame.display.update()  # Update the display once per loop iteration


