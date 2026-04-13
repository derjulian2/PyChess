
from utility.vec import vec2i

from pygame import Rect, Color, Surface
import pygame


class Component:

    def __init__(self) -> None:
        pass




class DrawableComponent:

    def __init__(self) -> None:
        self.layer: int


class GameObjectComponent:


    def __init__(self) -> None:
        self.bounding_box: Rect
        self.color: Color


class SpriteComponent:


    def __init__(self) -> None:
        self.image: Surface

    
    def fit_image(self, sz: vec2i) -> None:
        self.image = pygame.transform.smoothscale(self.image, sz)