import game
from pygame.math import *
import managers
from components import *

class GameObject:
    position = ()
    def __init__(self, position, pivot, texture):
        texture = managers.GraphicsManager.get_texture(texture)
        self.position = position
        self.pivot = pivot

        image_size = texture.get_size()

        texture_list = []
        texture_list.append(texture)

        p_x = image_size[0] * pivot[0]
        p_y = image_size[1] * pivot[0]
        self._pivot = (p_x, p_y)

        sprite_x = position[0] - self._pivot[0]
        sprite_y = position[1] - self._pivot[1]
        spr_position = (sprite_x, sprite_y)
        self.current_sprite = Sprite(spr_position, texture_list, self.pivot)

        self.is_active = True
        self.is_visible = True
        self.layer = managers.Layers.PLAYGROUND
        self.depth = 0

        managers.UpdateManager.add_item(self)
        managers.DrawManager.add_item(self)

    
    def draw(self, screen):
        #pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), int(self.radius))
        self.current_sprite.draw(screen)


    def set_layer(self, layer):
        managers.DrawManager.remove_item(self)
        self.layer = layer
        managers.DrawManager.add_item(self)
        

    def set_position(self, new_position):
        self.position = new_position
        self.current_sprite.position = new_position


    def on_collide(self, obj, collision):
        d = collision.distance
        _dir = collision.direction

        rr = collision.min_distance
        _dist = abs(rr - d)
        delta = _dir * _dist

        self.set_position(self.position - delta)

        

class Actor(GameObject):
    radius = 0
    repulsion = [False, [0, 0], 0]

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.depth = -position[1]
        managers.CollisionManager.add_item(self)

    
    def repel(self, obj, direction, distance):
        obj.repulsion = [True, direction, distance, distance*distance]


    def death(self):
        self.is_active = False
        self.is_visible = False
        self.is_alive = False