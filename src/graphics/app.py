
from graphics.board import ChessBoard
from graphics.asset_manager import AssetManager

from utility.vec import vec2i, vec2f

from pygame import Surface, time, display, event, Event, Color, QUIT
from pygame_gui import UIManager

from typing import Optional, Any
from os import PathLike


class App:
    """
    main-application-interface. holds the
    window's mainloop and the currently active scene
    of the application. 
    """

    def __init__(self, 
                 size: vec2i,
                 title: Optional[str] = None,
                 icon: Optional[Any] = None,
                 assets: Optional[dict[Any, PathLike]] = None) -> None:
        self.ui_manager: UIManager       = UIManager(size)
        self.asset_manager: AssetManager = AssetManager(assets)
        
        self.win: Surface                = display.set_mode(size, vsync=1)
        self.should_close: bool          = False
        self.clock: time.Clock           = time.Clock()
        self.time_delta: float           = 0
        
        self.asset_manager.load_images()
        if (icon):
            display.set_icon(self.asset_manager.images[icon])
        if (title):
            display.set_caption(title)

        self.background_color: Color     = Color("white")
        self.board: ChessBoard           = ChessBoard(vec2i(0, 0), min(size), self.asset_manager)


    def process_events(self) -> None:
        """
        goes through all active events and passes them to
        the active scene. also checks for window-close events.
        """
        for e in event.get():
            if (e.type == QUIT):
                self.should_close = True
            self.board.process_events(e)


    def update(self) -> None:
        """
        updates the active scene and passes time-delta to it.
        """
        self.board.update(self.time_delta)


    def draw(self) -> None:
        """
        clears the window's surface with the set background-color and
        draws the currently set active-scene ontop.
        """
        self.win.fill(self.background_color)
        self.board.draw(self.win)
        display.flip()


    def exec(self) -> None:
        """
        runs the application's mainloop of process_events(), update() and draw()
        while also measuring the time between each frame.
        """
        while (not self.should_close):
            self.time_delta = self.clock.tick(60) / 1000
            self.process_events()
            self.update()
            self.draw()