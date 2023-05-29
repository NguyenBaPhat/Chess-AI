import chess
import chess.engine
import numpy as np
from math import inf
import sys

class Chessboard:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = chess.Board(fen)
        self.center_square = [18,19,20,21,
                              26,27,28,29,
                              34,35,36,37,
                              42,43,44,45]

    def load_fen(self, fen):
        self.board.set_board_fen(fen)

    def evaluation(self):
        board = self.board
        center_squares = self.center_square

        # Initialize the evaluation to 0.
        evaluation = 0

        # Get all pieces position

        BP = board.pieces(chess.PAWN,   chess.BLACK)
        BN = board.pieces(chess.KNIGHT, chess.BLACK)
        BB = board.pieces(chess.BISHOP, chess.BLACK)
        BR = board.pieces(chess.ROOK,   chess.BLACK)
        BQ = board.pieces(chess.QUEEN,  chess.BLACK)
        BK = board.pieces(chess.KING,   chess.BLACK)

        WP = board.pieces(chess.PAWN,   chess.WHITE)
        WN = board.pieces(chess.KNIGHT, chess.WHITE)
        WB = board.pieces(chess.BISHOP, chess.WHITE)
        WR = board.pieces(chess.ROOK,   chess.WHITE)
        WQ = board.pieces(chess.QUEEN,  chess.WHITE)
        WK = board.pieces(chess.KING,   chess.WHITE)

        white_pieces = []
        black_pieces = []

        black_pieces.extend(BP)
        black_pieces.extend(BN)
        black_pieces.extend(BB)
        black_pieces.extend(BR)
        black_pieces.extend(BQ)
        black_pieces.extend(BK)

        white_pieces.extend(WP)
        white_pieces.extend(WN)
        white_pieces.extend(WB)
        white_pieces.extend(WR)
        white_pieces.extend(WQ)
        white_pieces.extend(WK)

        '''Criterion 1: Checkmate/Stalemate'''

        if (board.is_checkmate()):
            if(board.turn):
                return -inf
            else:
                return(inf)
            
        if (board.is_stalemate()):
            return 0
        '''Criterion 2: Pieces value'''

        evaluation += len(WP) + 3*(len(WN) + len(WB)) + 5*len(WR) + 9*len(WQ) + 100
        evaluation -= len(BP) + 3*(len(BN) + len(BB)) + 5*len(BR) + 9*len(BQ) + 100

        '''Criterion 3: Controlled squares'''

        # Get squares controlled by both side

        attacked_by_whites = []
        attacked_by_blacks = []

        for white_piece in white_pieces:
            attacked_by_whites.extend(board.attacks(white_piece))

        for black_piece in black_pieces:
            attacked_by_blacks.extend(board.attacks(black_piece))

        attacked_by_whites = list(set(attacked_by_whites))
        attacked_by_blacks = list(set(attacked_by_blacks))

        for square in attacked_by_whites:
            if (square in center_squares):
                evaluation += 0.1
            else:
                evaluation += 0.05

        for square in attacked_by_blacks:
            if (square in center_squares):
                evaluation -= 0.1   
            else:
                evaluation -= 0.05

        '''Criterion 4: Rook evaluation: Check for rook in rank 7th/2nd'''

        for white_rook in WR:
            if (not ((white_rook > 55) or (white_rook < 48))):
                evaluation += 1
    
        for black_rook in BR:
            if (not ((black_rook > 15) or (black_rook < 8))):
                evaluation -= 1

        '''Criterion 5: Check for King safety'''

        '''Criterion 5.1: Check for safety King position'''

        if (WK in (1,2,5,6)):       evaluation += 0.5
        if (BK in (57,58,61,62)):   evaluation -= 0.5

        '''Criterion 5.2: Check for double check'''

        if (len(board.attackers(chess.BLACK, list(WK)[0])) >= 2): evaluation -= 2
        if (len(board.attackers(chess.WHITE, list(BK)[0])) >= 2): evaluation += 2

        '''Criterion 6: Queen mobility'''

        for white_queen in WQ:
            if (len(board.attacks(white_queen)) >  8): evaluation += 0.2
            if (len(board.attacks(white_queen)) > 12): evaluation += 0.2
        
        for black_queen in BQ:
            if (len(board.attacks(black_queen)) >  8): evaluation -= 0.2
            if (len(board.attacks(black_queen)) > 12): evaluation -= 0.2


        '''Criterion 7: Knight mobility'''

        for white_knight in WN:
            if (len(board.attacks(white_knight)) > 3): evaluation += 0.1
            if (len(board.attacks(white_knight)) > 6): evaluation += 0.1

        for black_knight in BN:
            if (len(board.attacks(black_knight)) > 3): evaluation -= 0.1
            if (len(board.attacks(black_knight)) > 6): evaluation -= 0.1

        '''Criterion 8: Bishop mobility'''

        for white_bishop in WB:
            if (len(board.attacks(white_bishop)) > 5): evaluation += 0.1
            if (len(board.attacks(white_bishop)) > 8): evaluation += 0.1

        for black_bishop in BB:
            if (len(board.attacks(black_bishop)) > 5): evaluation -= 0.1
            if (len(board.attacks(black_bishop)) > 8): evaluation -= 0.1

        return round(evaluation, 3)

board = Chessboard()
# for move in board.board.legal_moves:
#     board.board.push(move)
#     print(move)
#     print(-evaluation(board))
#     board.board.pop()




def minimaxRoot(depth, board,isMaximizing):
    if (isMaximizing):
        bestMoveFinal = None
        possibleMoves = board.board.legal_moves
        bestMove = -inf
        for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.board.push(move)
                value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
                board.board.pop()
                if( value > bestMove):
                    bestMove = value
                    bestMoveFinal = move
        return bestMoveFinal
    else:
        bestMoveFinal = None
        possibleMoves = board.board.legal_moves
        bestMove = inf
        for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.board.push(move)
                value = min(bestMove, minimax(depth - 1, board,-10000,10000, isMaximizing))
                board.board.pop()
                if( value < bestMove):
                    bestMove = value
                    bestMoveFinal = move
        return bestMoveFinal

def minimax(depth, board, alpha, beta, is_maximizing):
    if(depth == 0):
        return board.evaluation()
    possibleMoves = board.board.legal_moves
    if(is_maximizing):
        bestMove = -inf
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = inf
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, is_maximizing))
            board.board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove
    
def calculateMove(board):
   possible_moves = board.board.legal_moves
   if(len(possible_moves) == 0):
       print("No more possible moves...Game Over")
       sys.exit()
   bestMove = None
   bestValue = inf
   n = 0
   for x in possible_moves:
       move = chess.Move.from_uci(str(x))
       board.board.push(move)
       boardValue = board.evaluation()
       board.board.pop()
       if(boardValue < bestValue):
           bestValue = boardValue
           bestMove = move

   return bestMove

def main():
    board = Chessboard()
    n = 0
    print(board.board)
    while n < 100:
        if n%2 == 0:
            suggest_move = minimaxRoot(3,board,True)
            print("Best move: ",suggest_move)
            move = input("Enter move: ")
            move = chess.Move.from_uci(str(move))
            board.board.push(move)
        else:
            move = minimaxRoot(3,board, False)
            print("Computers Turn:", move)
            move = chess.Move.from_uci(str(move))
            board.board.push(move)
        print(board.board)
        print("Score: ", board.evaluation())
        n += 1





if __name__ == "__main__":
    main()
