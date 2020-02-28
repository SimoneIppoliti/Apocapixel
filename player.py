import pygame, game
from pygame.math import *
import managers
from components import *
from game_objects import *
import text
import bullets, enemies

class Player(Actor):
    _name = "Player"
    _bullet_pivot = []
    health = 100

    def __init__(self, position, pivot, texture):
        super().__init__(position, pivot, texture)
        self.mouse_pressed = [False, False, False]
        self._shoot_counter = 0.0
        self._shoot_time = 0.1
        self._anim_counter = 0.0
        self._anim_time = 0.3
        self._rep_counter = 0.0
        self._rep_time = 0.25

        self.radius = 14.0

        self.set_position(position)

        idle_texture_list = []
        walk_texture_list = []
        attack_texture_list = []
        die_texture_list = []
        hit_texture = []
        hit_texture.append(managers.GraphicsManager.get_texture("p_hit"))
        ghost_idle = []

        for i in range(3):
            img = managers.GraphicsManager.get_texture("p_idle_" + str(i))
            idle_texture_list.append(img)

        for i in range(3):
            img = managers.GraphicsManager.get_texture("p_walk_" + str(i))
            walk_texture_list.append(img)

        for i in range(3):
            img = managers.GraphicsManager.get_texture("p_attack_" + str(i))
            attack_texture_list.append(img)

        for i in range(4):
            img = managers.GraphicsManager.get_texture("p_die_" + str(i))
            die_texture_list.append(img)

        for i in range(4):
            img = managers.GraphicsManager.get_texture("ghost_" + str(i))
            ghost_idle.append(img)

        # SPRITES
        self.idle = Sprite(self.position, idle_texture_list, self.pivot) # Idle sprites
        self.walk = Sprite(self.position, walk_texture_list, self.pivot) # Walk sprites
        self.attack = Sprite(self.position, attack_texture_list, self.pivot) # Attack sprites
        self.die = Sprite(self.position, die_texture_list, self.pivot) # Die sprites
        self.hit = Sprite(self.position, hit_texture, self.pivot) # Hit sprites

        self.current_sprite = self.idle
        self.sprites = []
        self.sprites.extend([self.idle, self.walk, self.attack, self.die, self.hit])

        # ANIMATIONS
        self.idle.animation = Animation(True, False, 3, 6, 1)
        self.walk.animation = Animation(True, True, 3, 6, 1)
        self.attack.animation = Animation(True, True, 3, 6, 1)
        self.die.animation = Animation(False, False, 4, 2, 0)

        self.ghost_object = Actor(self.position, self.pivot, "player") # Change to Ghost object instead of Actor
        self.ghost_object.idle = Sprite(position, ghost_idle) # Add list of sprites
        self.ghost_object.idle_animation = Animation(True, True, 4, 6, 0) # Add parameters
        self.ghost_object.is_active = False
        self.ghost_object.is_visible = False

        # Player Stats
        self.is_alive = True
        self.speed = 70.0

        self._bullet_pool = []
        self._bullet_1 = []
        self._bullet_2 = []
        self._bullet_3 = []
        self._bullet_4 = []
        self._bullet_5 = []
        self._bullet_6 = []

        self._shooting_pos = (0, 0)

        for j in range(30):
            bullet = bullets.LightBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_1.append(bullet)

        self._bullet_pool.append(self._bullet_1)

        self.bullet_index = 0
        for j in range(30):
            bullet = bullets.GreenBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_2.append(bullet)

        self._bullet_pool.append(self._bullet_2)

        for j in range(30):
            bullet = bullets.IceBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_3.append(bullet)

        self._bullet_pool.append(self._bullet_3)

        for j in range(30):
            bullet = bullets.MagicBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_4.append(bullet)

        self._bullet_pool.append(self._bullet_4)

        for j in range(30):
            bullet = bullets.FireBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_5.append(bullet)

        self._bullet_pool.append(self._bullet_5)

        for j in range(30):
            bullet = bullets.DarkBullet((0, 0), (0.5, 1.0), "bullet")
            if j == 0:
                self._bullet_pivot = bullet._pivot
            managers.UpdateManager.add_item(bullet)
            managers.DrawManager.add_item(bullet)
            managers.CollisionManager.add_item(bullet)

            bullet.set_layer(managers.Layers.FOREGROUND)
            bullet.set_direction([0, 0])

            bullet.is_active = False
            bullet.is_visible = False

            self._bullet_6.append(bullet)

        self._bullet_pool.append(self._bullet_6)

        _str = "Health: " + str(self.health)
        text.UIManager.player_health_text.set_text(_str)

        bullet_str = self._bullet_pool[self.bullet_index][0]._name
        _str = "Active Magic: " + bullet_str
        text.UIManager.active_bullet.set_text(_str)
        

    def shoot(self, direction):
        for b in self._bullet_pool[self.bullet_index]:
            if b.is_active == False:
                b.is_active = True
                b.is_visible = True

                b.set_direction(direction)
                x = self.position[0] - self._shooting_pos[0]
                y = self.position[1] - self._shooting_pos[1]
                b.position = (x, y)
                b.current_sprite.animation.play()
                return True
        return False


    def update(self):
        dt = game.delta_time
        if self._shoot_time > self._shoot_counter:
            self._shoot_counter += dt

        new_speed = self.speed * dt # Frame independent speed

        self.current_sprite.animation.play()

        # Get keys
        key = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Movement Axes
        _x = 0
        _y = 0
        _spr_flip = self.current_sprite.flip_x

        # Key press checks
        if key[pygame.K_w]: # UP
            _y = -1.0
        if key[pygame.K_s]: # DOWN
            _y = 1.0
        if key[pygame.K_a]: # LEFT
            _x = -1.0
            _spr_flip = True
        if key[pygame.K_d]: # RIGHT
            _x = 1.0
            _spr_flip = False
        if key[pygame.K_1]:
            self.bullet_index = 0
            self.update_bullet_string()
        if key[pygame.K_2]:
            self.bullet_index = 1
            self.update_bullet_string()
        if key[pygame.K_3]:
            self.bullet_index = 2
            self.update_bullet_string()
        if key[pygame.K_4]:
            self.bullet_index = 3
            self.update_bullet_string()
        if key[pygame.K_5]:
            self.bullet_index = 4
            self.update_bullet_string()
        if key[pygame.K_6]:
            self.bullet_index = 5
            self.update_bullet_string()
        
        # Repel
        if self.repulsion[0] == True:
            if self.current_sprite != self.hit:
                self.current_sprite = self.hit
                self._anim_counter = 0

            if self.repulsion[2] <= 0:
                self.repulsion[0] = False
            else:
                self.repulsion[2] -= self.repulsion[3] * dt * 0.75
                force = self.repulsion[1] * self.repulsion[2]
                xx = self.position[0] + force[0]
                yy = self.position[1] + force[1]
                self.set_position((xx, yy))

        # Sprite Update
        if self.current_sprite == self.hit:
            _x = 0
            _y = 0
            self.mouse_pressed = [True, True, True]

            if self.repulsion[1][0] < 0:
                _spr_flip = False
            elif self.repulsion[1][0] > 0:
                _spr_flip = True

            self._anim_counter += dt
            if self._anim_counter >= self._anim_time:
                self.current_sprite = self.idle
                self._anim_counter = 0
        elif self.current_sprite != self.attack:
            if _x != 0 or _y != 0:
                self.current_sprite = self.walk
            elif _x == 0 and _y == 0:
                ind = 1
                self.current_sprite = self.idle
                self.attack.image_index = ind
        else:
            self._anim_counter += dt
            if self._anim_counter > self._anim_time:
                ind = self.current_sprite.image_index
                self.current_sprite = self.idle
                self.attack.image_index = ind
                self._anim_counter = 0

        # Mouse control
        if mouse_buttons[0] and not self.mouse_pressed[0]:
            if self._shoot_counter >= self._shoot_time:
                m_x, m_y = pygame.mouse.get_pos()
                m_x -= self._bullet_pivot[0]
                m_y -= self._bullet_pivot[1]
                s_x = self.position[0] - self._shooting_pos[0]
                s_y = self.position[1] - self._shooting_pos[1]
                _dir = Vector2(m_x - s_x, m_y - s_y)
                _dir = Vector2.normalize(_dir)
                self.shoot(_dir)
                self._shoot_counter = 0
            self.mouse_pressed[0] = True

            # Sprite
            ind = self.current_sprite.image_index
            if self.current_sprite == self.idle:
                ind = 1
            self.current_sprite = self.attack
            self.attack.image_index = ind
            self._anim_counter = 0
        elif not mouse_buttons[0] and self.mouse_pressed[0]:
            self.mouse_pressed[0] = False

        #self.current_sprite.update()
        for s in self.sprites:
            s.flip_x = _spr_flip
            s.update()

        # Movement
        if _x != 0 or _y != 0:
            m_dir = Vector2(_x, _y)
            movement = (Vector2.normalize(m_dir) * new_speed)
            new_pos = self.position + movement
            self.set_position(new_pos)
        
        # Update everything
        self.depth = -self.position[1]
        self.idle.position = self.attack.position = self.walk.position = self.die.position = self.ghost_object.position = self.hit.position = self.position


    def set_sprite(self, new_sprite):
        self.current_sprite = new_sprite
        size = self.current_sprite.get_size()
        self.current_sprite.position = size * self.pivot

    
    def on_collide(self, obj, collider):
        if issubclass(type(obj), bullets.Bullet):
            return
        elif issubclass(type(obj), enemies.Enemy):
            self.current_sprite = self.hit
            self.health -= obj.damage
            _str = "Health: " + str(self.health)
            text.UIManager.player_health_text.set_text(_str)

        super().on_collide(obj, collider)


    def set_name(name):
        self._name = name


    def update_bullet_string(self):
        bullet_str = self._bullet_pool[self.bullet_index][0]._name
        _str = "Active Magic: " + bullet_str
        text.UIManager.active_bullet.set_text(_str)