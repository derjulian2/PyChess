
from chess.common import ChessColor, ChessPiece
from chess.bitboard import ChessBitBoardPiece

from graphics.app import App

import pygame

from os import PathLike


def gen_piece_image_paths() -> dict[ChessPiece, PathLike]:
    res = dict()
    for piece in ChessPiece:
        for color in ChessColor:
            if not (piece == ChessPiece.none or color == ChessColor.none):
                res[ChessBitBoardPiece(color, piece)] = f"assets/{color.name}-{piece.name}.png"
    return res


if __name__ == "__main__":
    pygame.init()
    app: App = App(size=(800, 800), 
                   title="PyChess", 
                   icon=ChessBitBoardPiece(ChessColor.white, ChessPiece.knight),
                   assets=gen_piece_image_paths())
    app.exec()
    pygame.quit()





