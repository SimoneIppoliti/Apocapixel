import sys, pygame
from pygame.locals import *
import managers
import text
import player

_framerate = 60
delta_time = 1 / _framerate
window = None
score_text = None
killed_enemies_text = None
w_x = 1024
w_y = 768

def main():
    # Initialise screen
    pygame.init()

    # Create window
    window = pygame.display.set_mode((w_x, w_y))
    pygame.display.set_caption("Apocapixels")

    # Create main surface
    screen = pygame.Surface(window.get_size())
    screen = screen.convert()
    screen.fill((0, 0, 0))

    # Time initialisation
    timer = pygame.time.Clock()

    # GRAPHICS MANAGER
    #--- Debug Sprites
    managers.GraphicsManager.add_texture("Assets\Player\Player.png", "player")
    managers.GraphicsManager.add_texture("Assets\Enemies\Enemy.png", "enemy")
    managers.GraphicsManager.add_texture("Assets\Bullets\Bullet.png", "bullet")

    #--- Player's sprites
    for i in range(3):
        path = "Assets\Player\Player_Idle_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "p_idle_" + str(i))

    for i in range(3):
        path = "Assets\Player\Player_Walk_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "p_walk_" + str(i))

    for i in range(3):
        path = "Assets\Player\Player_Attack_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "p_attack_" + str(i))

    for i in range(4):
        path = "Assets\Player\Player_Die_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "p_die_" + str(i))

    for i in range(4):
        path = "Assets\Player\Ghost_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "ghost_" + str(i))

    managers.GraphicsManager.add_texture("Assets\Player\Player_Hit.png", "p_hit")

    #--- Items' Sprites
    for i in range(4):
        path = "Assets\Items\HP_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "hp_" + str(i))

    for i in range(4):
        path = "Assets\Items\XP_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "xp_" + str(i))

    for i in range(7):
        path = "Assets\Items\Gold_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "gold_" + str(i))

    #--- Bullets
    for i in range(3):
        path = "Assets\Bullets\Bullet_LV1_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv1_" + str(i))

    for i in range(3):
        path = "Assets\Bullets\Bullet_LV2_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv2_" + str(i))

    for i in range(4):
        path = "Assets\Bullets\Bullet_LV3_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv3_" + str(i))

    for i in range(3):
        path = "Assets\Bullets\Bullet_LV4_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv4_" + str(i))

    for i in range(3):
        path = "Assets\Bullets\Bullet_LV5_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv5_" + str(i))

    for i in range(4):
        path = "Assets\Bullets\Bullet_LV6_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "bullet_lv6_" + str(i))

    # Enemies
    for i in range(3):
        path = "Assets\Enemies\Minion_Walk_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "minion_walk_" + str(i))

    for i in range(7):
        path = "Assets\Enemies\Minion_Die_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "minion_die_" + str(i))

    for i in range(3):
        path = "Assets\Enemies\Zombie_Walk_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "zombie_walk_" + str(i))

    for i in range(7):
        path = "Assets\Enemies\Zombie_Die_" + str(i) + ".png"
        managers.GraphicsManager.add_texture(path, "zombie_die_" + str(i))

    path = "Assets\Enemies\Minion_Hit.png"
    managers.GraphicsManager.add_texture(path, "minion_hit")

    path = "Assets\Enemies\Zombie_Hit.png"
    managers.GraphicsManager.add_texture(path, "zombie_hit")

    # Draw Manager
    managers.DrawManager(window, screen)

    # UI Manager
    text.UIManager()

    # Game Objects
    p = player.Player((100.0, 100.0), (0.5, 0.85), "player") # MAKE IT SPAWN IN THE CENTER OF THE SCREEN
    
    managers.WavesManager(p)

    # Event loop
    while True:
        delta_time = timer.tick(_framerate) * 0.001

        for event in pygame.event.get():
            if event.type == QUIT:
                return
        
        managers.UpdateManager.update()
        managers.WavesManager.update()
        managers.CollisionManager.update()

        managers.DrawManager.reorder_layers()
        managers.DrawManager.draw()

if __name__ == "__main__": main()