from abc import ABC, abstractmethod

import numpy as np
import pygame

pygame.init()
# window = pygame.display.set_mode((0, 0), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

DEFAULT_FONT = 'twcencondensedextra'

colors = {'White': (255, 255, 255),
          'LightGray': (240, 240, 240),
          'Gray': (200, 200, 200),
          'DarkGray': (100, 100, 100),
          'Black': (0, 0, 0),
          'Red': (255, 0, 0),
          'DarkRed': (153, 0, 0),
          'Green': (0, 255, 0),
          'DarkGreen': (0, 153, 0),
          'Blue': (0, 0, 255),
          'DarkBlue': (0, 0, 153),
          'Yellow': (255, 255, 51),
          'DarkYellow': (204, 204, 0),
          'Orange': (255, 153, 51),
          'DarkOrange': (204, 102, 0),
          'Purple': (153, 51, 255),
          'DarkPurple': (102, 0, 204),
          'Cyan': (51, 255, 255),
          'DarkCyan': (0, 204, 204),
          }


def quitProgram():
    pygame.quit()
    quit()


class Object(ABC):
    @abstractmethod
    def draw(self, force=False):
        pass

    def handleMouseDown(self, click_pos):
        pass

    def handleMouseUp(self, click_pos):
        pass


class Text(Object):
    def __init__(self, text, center, font_size=36, color=colors['Black']):
        self.text = text
        self.color = color
        self.center = center
        self.font_size = font_size

    def draw(self, force=False, update=True):
        if force:
            font = pygame.font.SysFont(DEFAULT_FONT, self.font_size)
            text = font.render(self.text, True, self.color)
            text_rect = text.get_rect()
            text_rect.center = self.center
            window.blit(text, text_rect)

            if update:
                pygame.display.update(text_rect)


class TextBlock(Object):
    def __init__(self, text, center, font_size=36, color=colors['Black']):
        self.text = text
        self.color = color
        self.center = center
        self.font_size = font_size

    def draw(self, force=False):
        if force:
            lines = self.text.split('\n')
            for i in range(len(lines)):
                line = lines[i]
                text_object = Text(line, self.center + [0, (i - float(len(lines) - 1) / 2) * self.font_size],
                                   self.font_size, self.color)

                text_object.draw(force=True)
                del text_object


class Button(Object):
    def __init__(self, center=(0, 0), size=(100, 50), color=colors['Red'], clicked_color=colors['DarkRed'],
                 text="Default", text_color=colors['Black'], text_size=30, action=None, action_arg=None):
        self.center = np.array(center)
        self.size = np.array(size)
        self.color = color
        self.clicked_color = clicked_color
        self.text = Text(text, center, text_size, text_color)
        self.action = action
        self.action_arg = action_arg
        self.clicked = False
        self.prev_clicked = True

    def draw(self, force=False):
        if force or not self.prev_clicked == self.clicked:
            if self.clicked:
                button_color = self.clicked_color
            else:
                button_color = self.color

            update_rect = pygame.draw.rect(window, button_color, (self.center - self.size / 2, self.size))
            self.text.draw(force=True)
            pygame.display.update(update_rect)

        self.prev_clicked = self.clicked

    def handleMouseDown(self, click_pos):
        if all(abs(click_pos - self.center) < self.size / 2):
            self.clicked = True
        else:
            self.clicked = False

    def handleMouseUp(self, click_pos):
        self.clicked = False
        if all(abs(click_pos - self.center) < self.size / 2):
            if self.action is not None:
                if self.action_arg is not None:
                    self.action(self.action_arg)
                else:
                    self.action()


class ToggleButton(Button):
    def __init__(self, center=(0, 0), size=(100, 50), color=colors['Red'], clicked_color=colors['DarkRed'],
                 text="Default", text_color=colors['Black'], text_size=30, action=None, action_arg=None,
                 alt_text="Default", alt_action=None, alt_action_arg=None):
        super(ToggleButton, self).__init__(center, size, color, clicked_color, text,
                                           text_color, text_size, action, action_arg)
        self.toggle_state = False
        self.prev_toggle_state = False
        self.alt_text = Text(alt_text, center, text_size, text_color)
        self.alt_action = alt_action
        self.alt_action_arg = alt_action_arg

    def draw(self, force=False):
        if force or not (self.prev_clicked == self.clicked and self.toggle_state == self.prev_toggle_state):
            if self.clicked or self.toggle_state:
                button_color = self.clicked_color
            else:
                button_color = self.color
            update_rect = pygame.draw.rect(window, button_color, (self.center - self.size / 2, self.size))

            if self.toggle_state:
                self.alt_text.draw(force=True)
            else:
                self.text.draw(force=True)
            pygame.display.update(update_rect)

        self.prev_clicked = self.clicked
        self.prev_toggle_state = self.toggle_state

    def handleMouseDown(self, click_pos):
        if all(abs(click_pos - self.center) < self.size / 2):
            self.clicked = True
        else:
            self.clicked = False

    def handleMouseUp(self, click_pos):
        self.clicked = False
        if all(abs(click_pos - self.center) < self.size / 2):
            if self.toggle_state:
                self.carefullyDoAction(self.alt_action, self.alt_action_arg)
            else:
                self.carefullyDoAction(self.action, self.action_arg)

            self.toggle_state = not self.toggle_state

    def carefullyDoAction(self, action, action_arg):
        if action is not None:
            if action_arg is not None:
                action(action_arg)
            else:
                action()


class Slider(Object):
    def __init__(self, var_obj, var_range, center, var_name='Default', var_type=int, line_len=600, line_width=10,
                 line_color=colors['Gray'], circle_radius=25, circle_color=colors['Blue'], text_color=colors['Black'],
                 text_size=30):

        self.var_obj = var_obj
        self.var_range = var_range
        self.center = np.array(center)
        self.var_name = var_name
        self.var_type = var_type
        self.line_len = line_len
        self.line_width = line_width
        self.line_color = line_color
        self.circle_radius = circle_radius
        self.circle_color = circle_color
        self.circle_position = self.center - [self.line_len / 2, 0]
        self.circle_clicked = False
        self.text_color = text_color
        self.text_size = text_size
        self.update = True
        self.enabled = True

    # Should move this to the Object class
    def moveCenter(self, new_center):
        self.circle_position += np.array(new_center) - self.center
        self.center = np.array(new_center)
        self.update = True

    def disable(self, disable):
        self.enabled = not disable
        self.update = True

    def draw(self, force=False):
        if force or self.update:
            update_rect = pygame.draw.rect(window, colors['White'],
                                           (self.center - [self.line_len / 2 + self.circle_radius, self.circle_radius],
                                            [self.line_len + self.circle_radius * 2, self.circle_radius * 3.3]))

            pygame.draw.line(window, self.line_color, self.center - [self.line_len / 2, 0],
                             self.center + [self.line_len / 2, 0], self.line_width)

            pygame.draw.circle(window, self.circle_color, self.circle_position.astype(int),
                               self.circle_radius)

            if self.enabled:
                text_color = self.text_color
            else:
                text_color = colors['Gray']
            text = Text(self.var_name + " = " + str(self.var_obj[0]), self.center + [0, self.circle_radius * 1.5],
                        self.text_size, text_color)
            text.draw(True, False)
            del text

            pygame.display.update(update_rect)
            self.update = False

    def handleMouseDown(self, click_pos):
        if self.enabled:
            if self.circle_clicked:
                self.update = True
                self.circle_position = np.clip(click_pos, self.center - [self.line_len / 2, 0],
                                               self.center + [self.line_len / 2, 0])

                var = (((self.circle_position - self.center)[0] + self.line_len / 2) / self.line_len *
                       (self.var_range[1] - self.var_range[0])) + self.var_range[0]
                if self.var_type == float:
                    var = '%.2f' % (var)
                self.var_obj[0] = self.var_type(var)

            else:
                if np.linalg.norm(click_pos - self.circle_position) < self.circle_radius:
                    self.circle_clicked = True

    def handleMouseUp(self, click_pos):
        self.circle_clicked = False
