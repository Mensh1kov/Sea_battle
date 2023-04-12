import abc

from pygame import Surface
from pygame.event import Event


class Display(metaclass=abc.ABCMeta):
    def __init__(self, size: (int, int)):
        self.size = size

    @abc.abstractmethod
    def render(self, surface: Surface):
        pass

    @abc.abstractmethod
    def handle_event(self, event: Event):
        pass
