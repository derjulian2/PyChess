
from pygame import *
from pygame_gui import *

from graphics.scenes.scene import *
from asset_manager import AssetManager

from gamelogic.piece import ChessPieceType, ChessPieceColor

"""
the chess-piece-images to be loaded by the AssetManager.
"""
chess_piece_image_paths = {
    (ChessPieceColor.white, ChessPieceType.pawn)   : "assets/white-pawn.png",
    (ChessPieceColor.white, ChessPieceType.knight) : "assets/white-knight.png",
    (ChessPieceColor.white, ChessPieceType.bishop) : "assets/white-bishop.png",
    (ChessPieceColor.white, ChessPieceType.rook)   : "assets/white-rook.png",
    (ChessPieceColor.white, ChessPieceType.queen)  : "assets/white-queen.png",
    (ChessPieceColor.white, ChessPieceType.king)   : "assets/white-king.png",

    (ChessPieceColor.black, ChessPieceType.pawn)   : "assets/black-pawn.png",
    (ChessPieceColor.black, ChessPieceType.knight) : "assets/black-knight.png",
    (ChessPieceColor.black, ChessPieceType.bishop) : "assets/black-bishop.png",
    (ChessPieceColor.black, ChessPieceType.rook)   : "assets/black-rook.png",
    (ChessPieceColor.black, ChessPieceType.queen)  : "assets/black-queen.png",
    (ChessPieceColor.black, ChessPieceType.king)   : "assets/black-king.png"
}


class App:
    """
    main-application-interface. holds the
    window's mainloop and the currently active scene
    of the application. 
    """

    def __init__(self, 
                 size: tuple[int, int] = (640 * 2, 480 * 2),
                 title: str = "PyChess") -> None:
        self.win: Surface                = display.set_mode(size, vsync=1)
        self.should_close: bool          = False
        self.ui_manager: UIManager       = UIManager(size)
        self.asset_manager: AssetManager = AssetManager(chess_piece_image_paths)
        self.clock: time.Clock           = time.Clock()
        self.time_delta: float           = 0
        self.background_color: Color     = Color("white")
        self.scene: Scene | None         = None

        display.set_caption(title)


    def change_scene(self, scene_type) -> None:
        """
        switches the active scene to an instance of the passed
        scene-type. 

        :param scene_type: the scene-type to be constructed. 
                           this type must be derived from graphics.scene.Scene
                           and take a pygame_gui.UIManager and asset_manager.AssetManager 
                           as parameters in it's constructor.
        """
        self.scene = scene_type(self.ui_manager, self.asset_manager)


    def process_events(self) -> None:
        """
        goes through all active events and passes them to
        the active scene. also checks for window-close events.
        """
        for e in event.get():
            if (e.type == QUIT):
                self.should_close = True
            if (self.scene is not None):
                self.scene.process_events(e)


    def update(self) -> None:
        """
        updates the active scene and passes time-delta to it.
        """
        if (self.scene is not None):
            self.scene.update(self.time_delta)


    def draw(self) -> None:
        """
        clears the window's surface with the set background-color and
        draws the currently set active-scene ontop.
        """
        self.win.fill(Color(255, 255, 255))
        if (self.scene is not None):
            self.scene.draw(self.win)
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