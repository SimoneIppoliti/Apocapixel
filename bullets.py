import pygame, game
from pygame.math import *
import components
import managers
from game_objects import *
from enemies import *

class Bullet(Actor):
    # Default speed & damage - DEBUG ONLY
    _speed = 180.0
    _damage = 10
    _name = "Bullet"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8


    def set_speed_damage(self, speed, damage):
        self._speed = speed
        self._damage = damage

    
    def set_direction(self, direction):
        self._direction = direction

    
    def update(self):
        x, y = pygame.display.get_surface().get_size()

        new_speed = self._speed * game.delta_time
        movement = Vector2(self._direction) * new_speed
        new_pos = self.position + movement
        self.set_position(new_pos)

        self.depth = -self.position[1]
        self.current_sprite.update()

        if self.position[0] < -100 or self.position[0] > x + 100:
            self.is_active = False
            self.is_visible = False
        if self.position[1] < -100 or self.position[1] > y + 100:
            self.is_active = False
            self.is_visible = False

    
    def on_collide(self, obj, collision):
        if issubclass(type(obj), Enemy):
            super().on_collide(obj, collision)
            self.repel(obj, collision.direction, 10)
            obj.health -= self._damage
            self.is_active = False
            self.is_visible = False

class LightBullet(Bullet):
    _speed = 180.0
    _damage = 1
    _name = "Light Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(3):
            img = managers.GraphicsManager.get_texture("bullet_lv1_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 3, 3, 0)

class GreenBullet(Bullet):
    _speed = 160.0
    _damage = 1
    _name = "Poison Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(3):
            img = managers.GraphicsManager.get_texture("bullet_lv2_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 3, 3, 0)

class IceBullet(Bullet):
    _speed = 140.0
    _damage = 2
    _name = "Ice Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(4):
            img = managers.GraphicsManager.get_texture("bullet_lv3_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 4, 3, 0)

class MagicBullet(Bullet):
    _speed = 150.0
    _damage = 4
    _name = "Magic Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(3):
            img = managers.GraphicsManager.get_texture("bullet_lv4_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 3, 3, 0)

class FireBullet(Bullet):
    _speed = 160.0
    _damage = 6
    _name = "Fire Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(3):
            img = managers.GraphicsManager.get_texture("bullet_lv5_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 3, 3, 0)

class DarkBullet(Bullet):
    _speed = 90.0
    _damage = 12
    _name = "Dark Orb"

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.radius = 8

        sprite_list = []

        for i in range(4):
            img = managers.GraphicsManager.get_texture("bullet_lv6_" + str(i))
            sprite_list.append(img)

        self.current_sprite = components.Sprite(self.position, sprite_list, self.pivot)
        self.current_sprite.animation = components.Animation(True, False, 4, 3, 0)