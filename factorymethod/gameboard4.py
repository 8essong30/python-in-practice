import io
import itertools
import os
import sys
import tempfile
import unicodedata


DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
        "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")
BLACK, WHITE = ("BLACK", "WHITE")


def main():
    checkers = CheckersBoard()
    print(checkers)

    chess = ChessBoard()
    print(chess)

    if sys.platform.startswith("win"):
        filename = os.path.join(os.getcwd(), "gameboard.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(sys.stdout.getvalue())
        print("wrote '{}'".format(filename), file=sys.__stdout__)


if sys.platform.startswith("win"):
    def console(char, background):
        return char or " "
    sys.stdout = io.StringIO()
else:
    def console(char, background):
        return "\x1B[{}m{}\x1B[0m".format(
                43 if background == BLACK else 47, char or " ")


class AbstractBoard:

    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()


    def populate_board(self):
        raise NotImplementedError()


    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y + x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):

    def __init__(self):
        self.populate_board()


    def populate_board(self): # Thanks to Doug Hellmann for the idea!
        def black():
            return create_piece(DRAUGHT, BLACK)
        def white():
            return create_piece(DRAUGHT, WHITE)
        rows = ((None, black()), (black(), None), (None, black()),
                (black(), None),            # 4 black rows
                (None, None), (None, None), # 2 blank rows
                (None, white()), (white(), None), (None, white()),
                (white(), None))            # 4 white rows
        self.board = [list(itertools.islice(
            itertools.cycle(squares), 0, len(rows))) for squares in rows]  # 리스트 컴프리헨션, itertools 함수 사용


class ChessBoard(AbstractBoard):

    def __init__(self):
        super().__init__(8, 8)


    def populate_board(self):
        for row, color in ((0, BLACK), (7, WHITE)):
            for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
                    ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
                for column in columns:
                    self.board[row][column] = create_piece(kind, color)
        for column in range(8):
            for row, color in ((1, BLACK), (6, WHITE)):
                self.board[row][column] = create_piece(PAWN, color)  # 클래스 객체 바로 호출해서 원하는 인스턴스 겟


def create_piece(kind, color):
    color = "White" if color == WHITE else "Black"
    name = {DRAUGHT: "Draught", PAWN: "ChessPawn", ROOK: "ChessRook",
            KNIGHT: "ChessKnight", BISHOP: "ChessBishop",
            KING: "ChessKing", QUEEN: "ChessQueen"}[kind]
    return globals()[color + name]()  # globals()로 얻은 딕셔너리에서 해당 클래스를 동적으로 찾음


class Piece(str):

    __slots__ = ()


for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    # 함수를 반환하는 함수, new() 반환 위해 char 타입을 인자로 바로 호출
    new = (lambda char: lambda Class: Piece.__new__(Class, char))(char)
    new.__name__ = "__new__"
    Class = type(name, (Piece,), dict(__slots__=(), __new__=new))
    globals()[name] = Class  # setattr() 보다 더 나은 방법


if __name__ == "__main__":
    main()
