import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        #self.image = pygame.Surface((TILE_SIZE // 2,TILE_SIZE))
        #self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft = pos)

        # player movement
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.gravity = 0.5
        self.jump_speed = 12
        self.collision_sprites = collision_sprites
        self.on_floor = False

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'code/graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        #loops over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)] 
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

        #set the rect
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)    

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

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -self.jump_speed

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'           

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                    self.on_ground = True

                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True

        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False

        #if self.on_floor and self.direction.y != 0:
        #    self.on_floor = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.get_status()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        self.animate()