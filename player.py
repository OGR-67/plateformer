import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_charracter_assets()
        self.import_dust_run_particules()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        
        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        
        # player status
        self.status = "idle"
        self.facing_right = True
        self.on_ground = True
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        
    def import_charracter_assets(self):
        print("Importing character assets...")
        character_path = "graphics/character/"
        self.animations = {
            "idle":[],
            "run":[],
            "jump":[],
            "fall":[],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            print(f"\t{animation}: {len(self.animations[animation])} image(s) imported")
        print()
    
    def import_dust_run_particules(self):
        print("Importing run particles...")
        self.dust_run_particles = import_folder("graphics/character/dust_particles/run")
        print(f"\t{len(self.dust_run_particles)} particles imported")
        print()
        
    def animate(self):
        animation = self.animations[self.status]
        
        # Loop through frames 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set rectangle
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:    
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:    
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:    
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:    
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > self.gravity:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"
    
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()
    
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
     
        
    def jump(self):
        if self.on_ground: self.direction.y = self.jump_speed
    
    
    def update(self):
        self.get_input()   
        self.get_status()     
        self.animate()
        