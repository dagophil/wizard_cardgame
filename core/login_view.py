import pygame
import events
import logging
from pygame_view import PygameView
from resource_manager import ResourceManager
from widgets import TextInput
import copy


BACKGROUND_IMAGE = "resources/bg_green.png"
FONT = "resources/fonts/opensans/OpenSans-Regular.ttf"
FONT_ITALIC = "resources/fonts/opensans/OpenSans-Italic.ttf"
FONT_BOLD = "resources/fonts/opensans/OpenSans-Bold.ttf"
FONT_SIZE = 16
INPUT_FORE_COLOR = (255, 255, 255)
INPUT_FILL_COLOR = (0, 0, 0, 128)
INPUT_WIDTH = 200
INPUT_PADDING = (5, 5, 5, 5)
INPUT_OFFSET = 40


class LoginView(PygameView):
    """
    The pygame login view.
    """

    def __init__(self, ev_manager):
        assert isinstance(ev_manager, events.EventManager)
        self._ev_manager = ev_manager
        self._ev_manager.register_listener(self)
        self._resource_manager = ResourceManager.instance()

        self._focused = None

        # Get the background image.
        self._background = self._resource_manager.get_image(BACKGROUND_IMAGE, self.screen.get_size())

        # Get the fonts.
        self._font = self._resource_manager.get_font(FONT, FONT_SIZE)
        self._default_font = self._resource_manager.get_font(FONT_ITALIC, FONT_SIZE)

        # Create the text inputs.
        self._username_input = TextInput(self._font, INPUT_WIDTH, padding=INPUT_PADDING, color=INPUT_FORE_COLOR,
                                         fill=INPUT_FILL_COLOR, default_text="username",
                                         default_font=self._default_font)
        self._host_input = copy.copy(self._username_input)
        self._host_input.default_text = "host"
        self._port_input = copy.copy(self._username_input)
        self._port_input.default_text = "port"

    @property
    def input_x(self):
        return (self.screen.get_width() - INPUT_WIDTH - INPUT_PADDING[1] - INPUT_PADDING[3]) / 2

    @property
    def input_y(self):
        return self.screen.get_height() / 2

    @property
    def input_height(self):
        return self._username_input.render_height

    def focus(self, s):
        """
        Set to focus to the given input. s must be either None, "username", "host", "port".
        :param s: the input
        """
        assert s in [None, "username", "host", "port"]
        self._focused = s

    def object_at(self, x, y):
        """
        Return either None, "username", "host", "port", depending on which of those is the object at (x, y).
        :return: which object is hovered
        """
        if self.input_x <= x <= self.input_x + INPUT_WIDTH + INPUT_PADDING[1] + INPUT_PADDING[3]:
            if self.input_y <= y <= self.input_y + self.input_height:
                return "username"
            elif self.input_y + INPUT_OFFSET <= y <= self.input_y + INPUT_OFFSET + self.input_height:
                return "host"
            elif self.input_y + 2*INPUT_OFFSET <= y <= self.input_y + 2*INPUT_OFFSET + self.input_height:
                return "port"
        return None

    def notify(self, event):
        """
        Handle the given event.
        :param event: the event
        """
        if isinstance(event, events.InitEvent):
            pass
        elif isinstance(event, events.TickEvent):
            self.screen.blit(self._background, (0, 0))

            x = self.input_x
            y = self.input_y

            self._username_input.render(self.screen, (x, y))
            self._host_input.render(self.screen, (x, y+INPUT_OFFSET))
            self._port_input.render(self.screen, (x, y+2*INPUT_OFFSET))

            pygame.display.flip()
