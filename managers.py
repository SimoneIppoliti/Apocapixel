import pygame, game
from enum import Enum
from pygame.math import *
from game_objects import *
import random, enemies

class Layers(Enum):
    BACKGROUND = 0
    PLAYGROUND = 1
    FOREGROUND = 2
    GUI = 3
    TEXT = 4

class GraphicsManager:
    _textures = {}

    @classmethod
    def add_texture(self, file_path, texture_name):
        temp_file = pygame.image.load(file_path)
        size = temp_file.get_size()

        size = (size[0] * 3, size[1] * 3) # Scale Sprite x3
        temp_file = pygame.transform.scale(temp_file, size)

        self._textures.update({texture_name : temp_file})

    @classmethod
    def get_texture(self, key):
        return self._textures.get(key)

class DrawManager:
    _background = []
    _playground = []
    _foreground = []
    _gui = []
    _text = []
    
    window = None
    screen = None

    @classmethod
    def __init__(self, window, screen):
        self.window = window
        self.screen = screen
    

    @classmethod
    def add_item(self, item):
        if item.layer == Layers.BACKGROUND:
            self._background.append(item)
        elif item.layer == Layers.PLAYGROUND:
            self._playground.append(item)
        elif item.layer == Layers.FOREGROUND:
            self._foreground.append(item)
        elif item.layer == Layers.GUI:
            self._gui.append(item)
        elif item.layer == Layers.TEXT:
            self._text.append(item)


    @classmethod
    def remove_item(self, item):
        if item.layer == Layers.BACKGROUND:
            self._background.remove(item)
        elif item.layer == Layers.PLAYGROUND:
            self._playground.remove(item)
        elif item.layer == Layers.FOREGROUND:
            self._foreground.remove(item)
        elif item.layer == Layers.GUI:
            self._gui.remove(item)
        elif item.layer == Layers.TEXT:
            self._text.remove(item)


    @classmethod
    def draw(self):
        self.screen.fill((23, 44, 31))
        for go in self._background:
            if go != None and go.is_visible:
                go.draw(self.screen)
        
        for go in self._playground:
            if go != None and go.is_visible:
                go.draw(self.screen)

        for go in self._foreground:
            if go != None and go.is_visible:
                go.draw(self.screen)

        for go in self._gui:
            if go != None and go.is_visible:
                go.draw(self.screen)

        for go in self._text:
            if go != None and go.is_visible:
                go.draw(self.screen)
        
        self.window.blit(self.screen, (0, 0))
        pygame.display.flip()
    
    
    @classmethod
    def quicksort(self, arr):
        shallower = []
        pivot_list = []
        deeper = []
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            for i in arr:
                if i.depth > pivot.depth:
                    deeper.append(i)
                elif i.depth < pivot.depth:
                    shallower.append(i)
                else:
                    pivot_list.append(i)
            shallower = self.quicksort(shallower)
            deeper = self.quicksort(deeper)
            return deeper + pivot_list + shallower

    
    @classmethod
    def reorder_layers(self):
        self._background = self.quicksort(self._background)
        self._playground = self.quicksort(self._playground)
        self._foreground = self.quicksort(self._foreground)
        self._gui = self.quicksort(self._gui)

class UpdateManager:
    _game_objects = []

    @classmethod
    def add_item(self, go):
        self._game_objects.append(go)
    

    @classmethod
    def update(self):
        for item in self._game_objects:
            if item.is_active:
                item.update()

class CollisionManager:
    _game_objects = []
    _length = 0

    @classmethod
    def add_item(self, item):
        self._game_objects.append(item)
        self._length = len(self._game_objects)


    @classmethod
    def update(self):
        for i in range(0, self._length - 1):
            for j in range(i + 1, self._length):
                obj1 = self._game_objects[i]
                obj2 = self._game_objects[j]

                if (not obj1.is_active) or (not obj2.is_active):
                    continue

                collision = self.check_collision(obj1, obj2)

                if collision.detected:
                    obj1.on_collide(obj2, collision)
                    collision.direction *= -1
                    obj2.on_collide(obj1, collision)

    
    def check_collision(obj1, obj2):
        p1 = Vector2(obj1.position)
        p2 = Vector2(obj2.position)

        d = p1.distance_to(p2) # Distance between p1 & p2
        if d > 0:
            _dir = (p2 - p1).normalize()# Direction
        else:
            _dir = Vector2(0, 0)
        rr = obj1.radius + obj2.radius # Radii of each obj

        return CollisionInfo(d, rr, _dir)

class CollisionInfo:
    def __init__(self, distance, min_distance, direction):
        self.distance = distance
        self.min_distance = min_distance
        self.detected = distance < min_distance
        self.direction = direction

class WavesManager:
    _enemy_pool = []
    curr_index = 0
    max_enemies_on_field = 30
    enemies_on_field = 0
    time_between_spawns = 1.0
    counter = 0.0

    @classmethod
    def __init__(self, player):
        enemy_list = []
        pos = (0, 0)
        piv = (0.5, 0.85)
        tex = "enemy"
        minion = enemies.ZombieMinion(pos, piv, tex)
        zombie = enemies.Zombie(pos, piv, tex)
        enemy_list.append(minion)
        enemy_list.append(zombie)
        for i in range(100):
            r = random.choice(enemy_list)
            if r == minion:
                _minion = enemies.ZombieMinion(pos, piv, tex)
                _minion.set_target(player)
                _minion.is_active = False
                _minion.is_visible = False
                self._enemy_pool.append(_minion)
            else:
                _zombie = enemies.Zombie(pos, piv, tex)
                _zombie.set_target(player)
                _zombie.is_active = False
                _zombie.is_visible = False
                self._enemy_pool.append(_zombie)

    @classmethod
    def update(self):
        dt = game.delta_time
        self.counter += dt

        if self.counter >= self.time_between_spawns:
            e = self._enemy_pool[self.curr_index]

            if self.enemies_on_field <= self.max_enemies_on_field:
                if e.is_active == False:

                    n = random.randint(0, 2)
                    r_list = []
                    r_list.append(-10)
                    r_list.append(game.w_x + 10)

                    if n == 0:
                        _y = -10
                        _x = random.randint(-10, game.w_x + 10)
                    elif n == 1:
                        _y = game.w_y + 10
                        _x = random.randint(-10, game.w_x + 10)
                    else:
                        _y = random.randint(-10, game.w_y + 10)
                        _x = random.choice(r_list)
                    
                    e.set_position((_x, _y))

                    e.is_active = True
                    e.is_visible = True

                self.curr_index += 1
                self.enemies_on_field += 1

                if self.curr_index >= len(self._enemy_pool):
                    self.curr_index = 0

                self.counter = 0