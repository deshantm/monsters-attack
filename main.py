#Monster Attack
import pygame
import random
import time
import os
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

isLevelXA = False
isLevelXB = True
level = 8

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



# Load "The Dark Master" parts
dark_master_parts = {
    "tail": pygame.image.load("tail.webp"),
    "chain": pygame.image.load("chain.webp"),
    "head": pygame.image.load("head.webp"),
    "body": pygame.image.load("body.webp"),
    "leg": pygame.image.load("leg.webp"),
    "head_with_red_eyes": pygame.image.load("head-with-red-eyes.webp"),
    "feet": pygame.image.load("feet.webp"),
    "crystal": pygame.image.load("crystal.webp")
}



class Boss:
    def __init__(self, image, position):
        self.image = pygame.transform.scale(image, (100, 100))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.health = 100  # Example attribute
        self.max_health = 100  # Maximum health
        self.speed = 0.5  # Boss speed, adjust as needed
        self.defeated = False  # add a defeated flag

        # New attributes for internal position tracking with floating-point precision
        self.pos_x = float(position[0])
        self.pos_y = float(position[1])

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.defeated = True 
            #set the image to dead/flat image
            self.image = pygame.transform.scale(self.image, (100, 10))  # Example scaling for dead image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_position = (self.rect.x, self.rect.y - 10)
        bar_size = (self.rect.width, 10)
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (bar_position, (bar_size[0] * health_ratio, bar_size[1])))

    def update(self, player):
        if self.health > 0:
            self.chase_player(player.x, player.y)
            self.attack_player(player)
            # Update the rect position based on the internal floating-point tracking
            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)

    def chase_player(self, player_x, player_y):
        # Calculate direction vector towards the player
        dir_x = player_x - self.pos_x
        dir_y = player_y - self.pos_y

        # Normalize direction vector (if not zero) to ensure consistent speed
        distance = (dir_x**2 + dir_y**2)**0.5
        if distance > 0:
            dir_x /= distance
            dir_y /= distance

            # Accumulate the movement with floating-point precision
            self.pos_x += dir_x * self.speed
            self.pos_y += dir_y * self.speed

        print("chasing", self.pos_x, self.pos_y, player_x, player_y)

    def attack_player(self, player):
        # Define a simple attack hitbox around the boss
        attack_rect = pygame.Rect(self.rect.x - 10, self.rect.y - 10, self.rect.width + 20, self.rect.height + 20)
        player_rect = pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())

        # Check for collision with the player
        if attack_rect.colliderect(player_rect):
            player.hit()  # Assume hit() reduces the player's health and handles death



class TheDarkMaster():
    def __init__(self, parts, position):
        self.parts = parts
        self.attack_timer = 0
        self.attacking = False
        self.assembled_image = self.assemble_parts(parts)
        self.rect = self.assembled_image.get_rect()
        self.rect.topleft = position
        self.health = 1000
        self.speed = 1
        self.pos_x = float(position[0])
        self.pos_y = float(position[1])
        self.defeated = False
        


        self.zoom_dive_cooldown = 0
        self.is_zoom_diving = False
        self.level = 8
        
    def assemble_parts(self, parts):
        # Create a new surface for the assembled image with enough space and transparency
        assembled_surface = pygame.Surface((800, 1200), pygame.SRCALPHA)  # Adjust the size as needed to fit all parts

        #scale the parts
        for part in parts:
            parts[part] = pygame.transform.scale(parts[part], (100, 100))



        # Central piece: Body. We place it near the center of our surface
        body_pos = (300 - parts['body'].get_width() // 2, 500 - parts['body'].get_height() // 2)
        assembled_surface.blit(parts['body'], body_pos)
        screen.blit(assembled_surface, (0, 0))

        
        # Head on top of the body
        #if attacking, use the head with red eyes
        if self.attacking:
            #print("attacking")
            head_pos = (body_pos[0] + (parts['body'].get_width() - parts['head_with_red_eyes'].get_width()) // 2, body_pos[1] - parts['head_with_red_eyes'].get_height())
            assembled_surface.blit(parts['head_with_red_eyes'], head_pos)
        else:
            #print("not attacking")
            head_pos = (body_pos[0] + (parts['body'].get_width() - parts['head'].get_width()) // 2, body_pos[1] - parts['head'].get_height())
            assembled_surface.blit(parts['head'], head_pos)
        
        # Feet at the bottom of the body
        feet_pos = (body_pos[0] + (parts['body'].get_width() - parts['feet'].get_width()) // 2, body_pos[1] + parts['body'].get_height())
        assembled_surface.blit(parts['feet'], feet_pos)
        
        # Tail to the left side of the body
        tail_pos = (body_pos[0] - parts['tail'].get_width(), body_pos[1] + (parts['body'].get_height() - parts['tail'].get_height()) // 2)
        assembled_surface.blit(parts['tail'], tail_pos)
        
        # Chain to the left side of the tail
        # make sure it is on the left side of the tail
        chain_pos = (tail_pos[0] - parts['chain'].get_width(), body_pos[1] + (parts['body'].get_height() - parts['chain'].get_height()) // 2)
        assembled_surface.blit(parts['chain'], chain_pos)
        
        #put the crytal under the chain
        crystal_pos = (chain_pos[0] + (parts['chain'].get_width() - parts['crystal'].get_width()) // 2, chain_pos[1] + parts['chain'].get_height())
        assembled_surface.blit(parts['crystal'], crystal_pos)
        
        
        # Leg just below the body, slightly to the right
        leg_pos = (body_pos[0] + parts['body'].get_width() // 4, body_pos[1] + parts['body'].get_height() - parts['leg'].get_height() // 2)
        assembled_surface.blit(parts['leg'], leg_pos)
        
        
        
        return assembled_surface

    def draw(self, surface):
        if self.attacking:
            #print("Drawing: Attacking with red eyes")  # Debugging print
            # Update the assembled image to the "red eye" version when attacking
            self.assembled_image = self.assemble_parts(self.parts)
        else:
            #print("Drawing: Not attacking, normal eyes")  # Debugging print
            self.assembled_image = self.assemble_parts(self.parts)
        surface.blit(self.assembled_image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_position = (self.rect.x, self.rect.y - 10)
        bar_size = (self.rect.width, 10)
        health_ratio = self.health / 1000
        pygame.draw.rect(surface, (255, 0, 0), (bar_position, (bar_size[0] * health_ratio, bar_size[1])))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.defeated = True
            self.assembled_image = pygame.transform.scale(self.assembled_image, (800, 100))



    def update(self, player):
        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.attacking = True
            print(f"Updating: attack_timer={self.attack_timer}, attacking={self.attacking}")  # Debugging print
        else:
            self.attacking = False
        
        if self.health > 0 and not self.is_zoom_diving:
            self.move_horizontally(player.x)
            self.choose_action(player)
        

    def move_horizontally(self, player_x):
        if player_x < self.pos_x:
            self.pos_x -= self.speed
        elif player_x > self.pos_x:
            self.pos_x += self.speed
        self.rect.x = int(self.pos_x)

    def tail_swipe(self, player):
        # Example logic for tail swipe, might involve animation or hit detection
        print("Tail swipe attack")
        self.attack_timer = 300
        # Implement hit detection and apply damage to player if within range

    def zoom_dive(self, player):
        print("Zoom dive attack")
        self.is_zoom_diving = True
        self.attack_timer = 300
        # Implement the zoom dive attack logic, moving towards the player quickly and dealing damage
        # Reset is_zoom_diving and zoom_dive_cooldown after the attack

    def choose_action(self, player):
        print(f"Choosing action. Current zoom_dive_cooldown: {self.zoom_dive_cooldown}")  # Debug print

        if self.zoom_dive_cooldown <= 0:
            action = random.choice(["tail_swipe", "zoom_dive"])
            print(f"Action chosen: {action}")  # Debug print

            if action == "tail_swipe":
                self.tail_swipe(player)
                self.attacking = True
                print("Performing tail swipe. Setting attacking to True.")  # Debug print
            else:
                self.zoom_dive(player)
                self.zoom_dive_cooldown = random.randint(20, 40)  # Cooldown before next zoom dive
                self.attacking = True  # Assuming you want to set attacking to True for zoom dive as well
                print(f"Performing zoom dive. New zoom_dive_cooldown: {self.zoom_dive_cooldown}, Setting attacking to True.")  # Debug print
        else:
            self.zoom_dive_cooldown -= 1
            self.attacking = False
            print(f"Not attacking. Decremented zoom_dive_cooldown to: {self.zoom_dive_cooldown}, Setting attacking to False.")  # Debug print





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
                if self.is_spider:
                
                    print(f"[Before Movement Update] Spider Position: x={self.x}, y={self.y} Level: {level} - From: chase_player")
                    #sleep for 3 seconds
                    #time.sleep(3)
                self.x += dx * .1 * level  # Slower movement rate
                self.y += dy * .1 * level
                if self.is_spider:
                    print(f"[After Movement Update] Spider Position: x={self.x}, y={self.y}  Level: {level} - From: chase_player")
                    #time.sleep(3)

                    

    def attack_player(self, player):
        # Check if close enough to attack
        
        if not self.dead and not player.dead: 
            #print("attacking", self.x, self.y, player.x, player.y, self.dead, player.dead)
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

# Assuming boss_images is a dictionary where keys are level numbers
boss_images = {}
boss_filenames = ['boss-1.jpeg', 'boss-2.jpeg', 'boss-3.png', 'boss-4.png', 'boss-5.jpeg', 'boss-6.jpeg', 'boss-7.jpeg']
for i, filename in enumerate(boss_filenames, start=1):  # Start at level 1
    try:
        image_path = os.path.join(filename)  # Adjust path as necessary
        boss_images[i] = pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Error loading boss image {filename}: {e}")


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


all_bosses = []  # List to keep track of all bosses, including defeated ones


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

level_7_boss_defeated = False
spider_ready = False
spider_already_spawned = False

def reset_or_populate_enemies(enemies, level, populate_new_level=False):

    global spider_already_spawned
    
    if populate_new_level:
        # Completely clear the enemies list for a fresh start
        enemies.clear()

        if level == 7 and level_7_boss_defeated and spider_ready and not spider_already_spawned:
            # Create the special spider enemy for level 7
    
            x = random.randint(0, screen.get_width() - 400)
            y = random.randint(0, screen.get_height() - 400)
            spider = Enemy(x, y, 1000, spider_image, spider_dead_image, None, is_spider=True)
            print(f"Creating/Resetting Spider at Position: x={x}, y={y} - Level: {level}")
            enemies.append(spider)
            spider_already_spawned = True
        elif level < 7: # Populate regular enemies for other levels

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
        self.jumping = False

    def jump(self):
        if not self.dead and not self.jumping:
            self.y -= 200  # Move up


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

    def update(self, enemies, bosses, screen):
        # Implement AI movement towards the nearest enemy or strategic positioning
        self.move_automatically(enemies)
        # Implement AI shooting logic
        if self.shoot_cooldown <= 0:
            self.shoot(enemies, bosses, screen)
            self.shoot_cooldown = 50  # Adjust cooldown based on desired shooting frequency
        else:
            self.shoot_cooldown -= 1

    def jump(self):
         #same jump as player
        if not self.dead and self.jumping:
            self.y -= 200 # Move up

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

        #if jump timer is up, jump
        if self.jumping:
            self.jump()
                

    def shoot(self, enemies, bosses, screen):
        # Example: Shoot a laser towards the nearest enemy
        #print("AI shooting")
        for enemy in enemies:
            if enemy.dead:
                enemies.remove(enemy)

        
        # First, check if there is a boss to shoot at
        if bosses:
            # Assuming bosses is a list but contains only one active boss at any time
            boss = next((boss for boss in bosses if not boss.defeated and boss.level == level), None)
            if boss:
                # Boss is present and not defeated
                pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (boss.pos_x, boss.pos_y), 2)
                # Check if within range and apply damage
                if (boss.pos_x - self.x) ** 2 + (boss.pos_y - self.y) ** 2 < 400**2:
                    boss.take_damage(10)  # Example damage value
                return  # Exit the method after handling the boss



        if enemies:
            #print("AI shooting at enemy")
            #print("AI position", self.x, self.y)
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


boss = None

# Set the game loop
running = True
level = 0
level = 8

# Initialize a variable to store the target position for the laser
laser_target = None

laser_line_duration = 0

#add ai jumping timer
ai_jumping_timer = 0

while running:
    current_time = time.time()
    #if player is on the ground, set jumping to false
    if player.y == screen.get_height() - player.image.get_height():
        player.jumping = False

    ai_jumping_timer += 1
    if ai_jumping_timer >= 500:
        ai_jumping_timer = 0
        for ai_helper in ai_helpers:
            ai_helper.jumping = True
    else:
        for ai_helper in ai_helpers:
            ai_helper.jumping = False


    #ai jumping based on timer
    for ai_helper in ai_helpers:
        if ai_helper.jumping:
            ai_helper.jump()
        else: #gravity pulls them down (if not a bottom)
            if ai_helper.y < screen.get_height() - ai_helper.image.get_height():
                ai_helper.y += 10

    # Continuous key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("LEFT")
    if keys[pygame.K_RIGHT]:
        player.move("RIGHT")
    #space bar to jump
    if keys[pygame.K_SPACE] and not player.jumping:
        player.jump()
        player.jumping = True

    else: #gravity pulls them down (if not a bottom)
        if player.y < screen.get_height() - player.image.get_height():
            player.y += 10

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
            isLevelXA = True
            level += 1
            
    
    # Example integration within the game loop

    if isLevelXA:  # Check if the current level is 8
        if not any(boss.level >= 8 for boss in all_bosses):  # Ensure "The Dark Master" isn't already spawned
            # Position where "The Dark Master" should appear
            screen_width, screen_height = screen.get_size()
            dark_master_position = (screen_width // 2, 10)
            
            # Create "The Dark Master"
            the_dark_master = TheDarkMaster(dark_master_parts, dark_master_position)
            
            all_bosses.append(the_dark_master)  # Add "The Dark Master" to the bosses list
        
        # Additional code to handle "The Dark Master" behavior, drawing, etc.



    # Display level selection or gameplay based on level value
    if level == 0:
        # Display level selection
        for i, img in enumerate(level_images):
            screen.blit(img, (i * 100, 0))
    else:

        
        # Gameplay drawing: player, enemies, and optionally the laser line
        font = pygame.font.Font(None, 36)
        text = font.render(f"Level {level}", True, (0, 0, 0))
        if level != 9:
            text = font.render(f"Level {level}", True, (0, 0, 0))
        else:
            text = font.render(f"Level XA", True, (0, 0, 0))
        screen.blit(text, (width // 2, 0))

        if laser_target and laser_line_duration > 0:  # Draw the laser line if a target is set and duration is positive
            pygame.draw.line(screen, (255, 0, 0), (player.x + player.image.get_width() // 2, player.y), laser_target)
            laser_line_duration -= 1  # Decrement the duration each frame
           

        
        for enemy in enemies:  # Draw enemies
            enemy.draw(screen)

        for boss in all_bosses:
            if level == 7 and boss.level == 7 and boss.defeated:
                level_7_boss_defeated = True
            if not boss.defeated:
                boss.update(player)  # Update only if the boss is not defeated
            boss.draw(screen)  # Draw every boss, including defeated ones

        player.draw(screen)  # Draw the player

        # Inside the game loop, after drawing everything
        player.draw_health_bar(screen)


        # Update and draw AI helpers
        for ai_helper in ai_helpers:
            ai_helper.update(enemies, all_bosses, screen)
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

            #print("Shoot laser")
            # Assuming the player's laser starts from the middle of the player image
            laser_start = (player.x + player.image.get_width() // 2, player.y)

            # Check collision with the boss
            if boss and boss.rect.collidepoint(laser_target):
                boss.take_damage(10)  # Example damage value
            
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

    if level > 1: 
        #check for number of ai helpers
        if len(ai_helpers) < level:
            ai_x_position = player.x + random.randint(-400, 400)  # Adjust for closer positioning
            ai_y_position = player.y + random.randint(-50, 50)  # Adjust for closer positioning
            ai_helper = AIHelper(ai_x_position, ai_y_position, 5, laser_image, laser_dead_image)
            ai_helpers.append(ai_helper)

    if (all(enemy.dead for enemy in enemies) and level >= 1 and level <= 6) or level == 7 and not level_7_boss_defeated :
    # This condition ensures a new boss is spawned for levels 2 to 7

        # Check if the boss for the next level has already been spawned
        if not any(boss.level == level for boss in all_bosses):
            boss_image = boss_images[level]  # Get the boss image for the current level
            boss_position = (400, 300)  # Example position
            new_boss = Boss(boss_image, boss_position)
            new_boss.level = level  # Track the level of the boss for identification
            all_bosses.append(new_boss)  # Add the new boss to the list



    # Inside the game loop, after updating and drawing everything
    if level > 0 and level < 7 and all(enemy.dead for enemy in enemies) and all(boss.defeated for boss in all_bosses if boss.level == level):
        level += 1  # Increment the level
        reset_or_populate_enemies(enemies, level, populate_new_level=True)  # Populate new level with enemies

       

    elif level == 7 and level_7_boss_defeated:
        spider_ready = True
        if not spider_already_spawned:
            reset_or_populate_enemies(enemies, level, populate_new_level=True)  # Populate new level with enemies
        #spider is defeated, print mission accomplished
        if all(enemy.dead for enemy in enemies):
            # Display mission accomplished
            font = pygame.font.Font(None, 36)
            text = font.render(f"Mission Accomplished", True, (0, 0, 0))
            screen.blit(text, (width // 2, height // 2))
            pygame.display.update()
            time.sleep(3)
            level += 1
    elif level == 8:
        isLevelXA = True
        level += 1
    
    
    if isLevelXA:
        the_dark_master.update(player)
        the_dark_master.draw(screen)  # Draw "The Dark Master" with its current state

    





    # Check for and handle player respawn
    player.respawn(current_time)

    pygame.display.update()  # Update the display once per loop iteration


