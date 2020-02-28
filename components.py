import pygame, game
from enum import Enum
from pygame.math import *

class Sprite:
    def __init__(self, position, texture_list, pivot = (0, 0)):
        self.position = position # True position
        self.pivot = pivot # Normalized pivot
        self.flip_x = False
        self.flip_y = False
        
        x, y = texture_list[0].get_size()
        self.width = x
        self.height = y

        # True pivot
        self._pivot = (x * pivot[0], y * pivot[1])

        # Drawing position
        _x = self.position[0] - self._pivot[0]
        _y = self.position[1] - self._pivot[1]
        self.drawing_position = (_x, _y)
        self.textures = texture_list
        self.textures_number = len(self.textures)
        self.image_index = 0
        self.animation = Animation(False, False, 0, 0)

    
    def draw(self, screen):
        img = self.textures[self.image_index]
        img = pygame.transform.flip(img, self.flip_x, self.flip_y)
        screen.blit(img, self.drawing_position)


    def get_size(self, index = -1):
        i = self.image_index
        if index >= 0:
            i = index

        return self.textures[i].get_size()

    def set_animation(self, new_animation):
        self.animation = new_animation


    def update(self):
        x = self.position[0] - self._pivot[0]
        y = self.position[1] - self._pivot[1]
        self.drawing_position = (x, y)
        self.animation.update()
        self.image_index = self.animation.image_index

class AnimationState(Enum):
    PLAY = 0
    PAUSE = 1
    STOP = 2

class Animation:
    #_name = "" # DEBUG
    _n = 1

    def __init__(self, loop, ping_pong, frames, fps, start_index = 0):
        if start_index >= frames or start_index < 0:
            start_index = 0

        self.image_index = start_index
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.ping_pong = ping_pong
        if fps > 0:
            self._frame_time = 1 / fps
        else:
            self._frame_time = 0
        self._timer = 0
        self._state = AnimationState.PAUSE


    def play(self):
        self._state = AnimationState.PLAY


    def pause(self):
        self._state = AnimationState.PAUSE


    def stop(self):
        self._state = AnimationState.STOP

    
    def update(self):
        if self._state == AnimationState.PAUSE:
            return
        elif self._state == AnimationState.STOP:
            self.image_index = 0
            return
        
        self._timer += game.delta_time
        
        if self._timer >= self._frame_time:
            if self.loop:
                if self.image_index + self._n >= self.frames:
                    if self.ping_pong:
                        self.image_index -= self._n
                        self._n = -self._n
                        self._timer = 0
                        return
                    else:
                        self.image_index = 0
                elif self.image_index + self._n < 0:
                    if self.ping_pong:
                        self.image_index -= self._n
                        self._n = -self._n
                        self._timer = 0
                        return
                    else:
                        self.image_index = self.image_index
                else:
                    self.image_index += self._n
            else:
                if self.image_index + self._n >= self.frames:
                    return
                else:
                    self.image_index += self._n

            self._timer = 0

class Collider:
    def __init__(self, owner, relative_position):
        self.owner = owner
        self.relative_position = relative_position

        x = owner.position[0] + relative_position[0]
        y = owner.position[1] + relative_position[1]
        self.position = (x, y)

    def box_circle_collision(self, box, circle):
        rect_x, rect_y = box.position
        circle_x, circle_y = circle.position
        rect_width, rect_height = box.size

        nearest_x = max(rect_x, min(circle_x, rect_x + rect_width))
        nearest_y = max(rect_y, min(circle_y, rect_y + rect_height))

        delta_x = circle_x - nearest_x
        delta_y = circle_y - nearest_y
        delta_x *= delta_x
        delta_y *= delta_y

        return (delta_x + delta_y) < (circle.radius * circle.radius)

class CircleCollider(Collider):
    def __init__(self, owner, relative_position, radius):
        super().__init__(owner, relative_position)
        self.radius = radius


    def collide_with(self, collider):
        if collider is CircleCollider:
            radii = collider.radius + self.radius
            dist = Vector2(collider.position - self.position).length_squared
            #print(dist <= radii*radii)
            return dist <= radii*radii
        elif collider is BoxCollider:
            collision = self.box_circle_collision(collider, self)
            #print(collision)
            return collision
        
class BoxCollider(Collider):
    def __init__(self, owner, relative_position, size):
        super().__init__(owner, relative_position)
        self.size = (self.width, self.height) = size

    
    def collide_with(self, collider):
        if type(collider) == BoxCollider:
            x1 = self.position[0]
            x2 = collider.position[0]
            w1 = x1 + self.width
            w2 = x2 + collider.width
            y1 = self.position[1]
            y2 = collider.position[1]
            h1 = y1 + self.height
            h2 = y2 + collider.height
            collision = x1 <= w2 and w1 >= x2 and y1 <= h2 and h1 >= y2
            return collision
        elif type(collider) == CircleCollider:
            collision = self.box_circle_collision(self, collider)
            return collision