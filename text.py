import game
from game_objects import *
import managers

class Text(GameObject):
    def __init__(self, font, text, position, pivot):
        self._position = position
        self.pivot = pivot

        self.string = text
        self.font = font
        self.color = (255, 255, 255)
        self.text = self.font.render(text, 0, self.color)
        image_size = self.text.get_size()

        p_x = image_size[0] * pivot[0]
        p_y = image_size[1] * pivot[1]
        self._pivot = (p_x, p_y)

        text_x = position[0] - self._pivot[0]
        text_y = position[1] - self._pivot[1]
        self.position = [text_x, text_y]

        self.is_active = True
        self.is_visible = True
        self.layer = managers.Layers.TEXT
        self.depth = 0

        managers.UpdateManager.add_item(self)
        managers.DrawManager.add_item(self)


    def update(self):
        text_x = self._position[0] - self._pivot[0]
        text_y = self._position[1] - self._pivot[1]
        self.position = [text_x, text_y]


    def draw(self, screen):
        screen.blit(self.text, self.position)


    def set_color(self, color):
        self.color = color
        self.text = self.font.render(self.string, 0, color)

    
    def set_text(self, text):
        self.text = text
        self.text = self.font.render(text, 0, self.color)


    def set_text_ext(self, text, color):
        self.text = text
        self.color = color
        self.text = self.font.render(text, 0, color)

class UIManager:
    score = 0
    killed_enemies = 0
    player_health_text = None
    active_bullet = None

    @classmethod
    def __init__(self):
        font = pygame.font.Font("Assets\Legendaria_1.ttf", 32)

        _x, _y = (game.w_x, game.w_y)

        self.score_text = Text(font, "Score: 0", (10, _y - 32), (0, 1))
        self.killed_enemies_text = Text(font, "Killed Enemies: 0", (10, _y - 8), (0, 1))
        self.player_health_text = Text(font, "Health: 0", (10, 8), (0, 0))
        self.active_bullet = Text(font, "Active Magic: Yo mum", (10, 60), (0, 1))


    @classmethod
    def score_add(self, val):
        self.score += val
        self.score_text.set_text("Score: " + str(self.score))


    @classmethod
    def killed_enemies_add(self, val):
        self.killed_enemies += val
        self.killed_enemies_text.set_text("Killed Enemies: " + str(self.killed_enemies))