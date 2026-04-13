
from chess.piece import ChessPiece, ChessPieceType, ChessColor
from app import App

import pygame

from os import PathLike


def get_piece_image_paths() -> dict[ChessPiece, PathLike]:
    res = dict()
    for type in ChessPieceType:
        for color in ChessColor:
            res[ChessPiece(type, color)] = f"assets/{color.name}-{type.name}.png"
    return res


if __name__ == "__main__":
    pygame.init()
    app: App = App(size=(800, 800), 
                   title="PyChess", 
                   icon=ChessPiece(ChessPieceType.knight, ChessColor.white),
                   assets=get_piece_image_paths())
    # app.change_scene(ChessBoardScene)
    app.exec()
    pygame.quit()










