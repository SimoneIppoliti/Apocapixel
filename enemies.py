import game
import managers
from components import *
import text
from game_objects import *
import player

class Enemy(Actor):
    _name = "Enemy"
    damage = 10
    score = 1
    target = None

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.speed = 30.0
        self.radius = 19.0
        self.health = 10

        self.is_alive = True

        self._anim_counter = 0.0
        self._anim_time = 0.3
        self._rep_counter = 0.0
        self._rep_time = 0.25


    def set_target(self, target):
        self.target = target

    def update(self):
        dt = game.delta_time

        self.current_sprite.animation.play()

        # Chase target
        _pos = Vector2(self.position)

        if self.target == None:
            return

        _target_pos = Vector2(self.target.position)

        _dir = Vector2.normalize(_target_pos - _pos)
        _spr_flip = self.current_sprite.flip_x

        # Movement
        movement = _dir * self.speed * game.delta_time
        
        if _dir[0] > 0:
            _spr_flip = False
        elif _dir[0] < 0:
            _spr_flip = True

        # Repel
        if self.repulsion[0] == True:
            if self.current_sprite != self.die:
                if self.current_sprite != self.hit:
                    self.current_sprite = self.hit
                    self._anim_counter = 0

                if self.repulsion[2] <= 0:
                    self.repulsion[0] = False
                    if self.health <= 0:
                        self.is_alive = False
                else:
                    self.repulsion[2] -= self.repulsion[3] * dt * 0.75
                    force = self.repulsion[1] * self.repulsion[2]
                    xx = self.position[0] - force[0]
                    yy = self.position[1] - force[1]
                    self.set_position((xx, yy))

        # Sprite Update
        if self.is_alive:
            if self.current_sprite == self.hit:
                movement = (0, 0)

                if self.repulsion[1][0] < 0:
                    _spr_flip = True
                elif self.repulsion[1][0] > 0:
                    _spr_flip = False

                self._anim_counter += dt
                if self._anim_counter >= self._anim_time:
                    self.current_sprite = self.walk
                    self._anim_counter = 0
            else:
                self._anim_counter += dt
                if self._anim_counter > self._anim_time:
                    self.current_sprite = self.walk
        else:
            self.current_sprite = self.die
            self.current_sprite.animation.play()

            movement = (0, 0)

            img_ind = self.die.animation.image_index
            img_frames = self.die.animation.frames - 1
            death_check = img_ind >= img_frames
            if death_check:
                self._anim_counter += dt
                if self._anim_counter > self._anim_time * 2:
                    self.death()

        _x = self.position[0] + movement[0]
        _y = self.position[1] + movement[1]
        new_pos = (_x, _y)

        for s in self.sprites:
            s.flip_x = _spr_flip
            s.update()

        # Update everything
        self.set_position(new_pos)
        self.depth = -self.position[1]
        self.walk.position = self.die.position = self.hit.position = self.position

    def death(self):
        #super().death()
        self.is_active = False
        self.is_visible = False
        text.UIManager.score_add(self.score)
        text.UIManager.killed_enemies_add(1)
        managers.WavesManager.enemies_on_field -= 1
    
    def on_collide(self, obj, collider):
        if type(obj) == player.Player:
            super().on_collide(obj, collider)
            self.repel(obj, collider.direction, 10)

class ZombieMinion(Enemy):
    _name = "Zombie Minion"
    damage = 10
    score = 5

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)

        self.speed = 50.0
        self.radius = 12.0
        self.health = 3

        walk_texture_list = []
        die_texture_list = []
        hit_texture = []
        hit_texture.append(managers.GraphicsManager.get_texture("minion_hit"))

        for i in range(3):
            img = managers.GraphicsManager.get_texture("minion_walk_" + str(i))
            walk_texture_list.append(img)

        for i in range(7):
            img = managers.GraphicsManager.get_texture("minion_die_" + str(i))
            die_texture_list.append(img)

        # SPRITES
        self.walk = Sprite(self.position, walk_texture_list, self.pivot) # Walk sprites
        self.die = Sprite(self.position, die_texture_list, self.pivot) # Die sprites
        self.hit = Sprite(self.position, hit_texture, self.pivot) # Hit sprites

        self.die.animation.pause()

        self.current_sprite = self.walk
        self.sprites = []
        self.sprites.extend([self.walk, self.die, self.hit])

        # ANIMATIONS
        self.walk.animation = Animation(True, True, 3, 8, 1)
        self.die.animation = Animation(False, False, 7, 6, 0)

class Zombie(Enemy):
    _name = "Zombie"
    damage = 25
    score = 15

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)

        self.speed = 25.0
        self.radius = 14.0
        self.health = 10

        walk_texture_list = []
        die_texture_list = []
        hit_texture = []
        hit_texture.append(managers.GraphicsManager.get_texture("zombie_hit"))

        for i in range(3):
            img = managers.GraphicsManager.get_texture("zombie_walk_" + str(i))
            walk_texture_list.append(img)

        for i in range(7):
            img = managers.GraphicsManager.get_texture("zombie_die_" + str(i))
            die_texture_list.append(img)

        # SPRITES
        self.walk = Sprite(self.position, walk_texture_list, self.pivot) # Walk sprites
        self.die = Sprite(self.position, die_texture_list, self.pivot) # Die sprites
        self.hit = Sprite(self.position, hit_texture, self.pivot) # Hit sprites

        self.current_sprite = self.walk
        self.sprites = []
        self.sprites.extend([self.walk, self.die, self.hit])

        # ANIMATIONS
        self.walk.animation = Animation(True, True, 3, 4, 1)
        self.die.animation = Animation(False, False, 7, 6, 0)