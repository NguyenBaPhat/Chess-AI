import chess
import math
import random
import sys
from math import inf

def minimax(depth, board, alpha, beta, is_maximizing, the_move):
    if(depth == 0):
        return evaluation(board), the_move
    possibleMoves = board.legal_moves

    if(is_maximizing):
        maxEval = -9999
        BestMove = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            Eval, this_move = minimax(depth - 1, board,alpha,beta, not is_maximizing, BestMove)
            if Eval > maxEval:
                maxEval = Eval
                BestMove = move
            board.pop()
            alpha = max(alpha,maxEval)
            if beta <= alpha:
                return maxEval, BestMove
        return maxEval, BestMove
    else:
        minEval = 9999
        BestMove = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            Eval, this_move = minimax(depth - 1, board,alpha,beta, not is_maximizing, BestMove)
            if Eval < minEval:
                minEval = Eval
                BestMove = move
            board.pop()
            beta = min(beta,minEval)
            if(beta <= alpha):
                return minEval, BestMove
        return minEval, BestMove
    
def calculateMove(board):
    Eval, bestMove = minimax(4, board, -9999, 9999, board.turn, None)
    print(bestMove)
    return bestMove

def evaluation(board):
    center_squares = [18,19,20,21,
                              26,27,28,29,
                              34,35,36,37,
                              42,43,44,45]

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

    evaluation += len(WP) + 3*(len(WN) + len(WB)) + 5*len(WR) + 9*len(WQ)
    evaluation -= len(BP) + 3*(len(BN) + len(BB)) + 5*len(BR) + 9*len(BQ)

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

    # '''Criterion 4: Rook evaluation: Check for rook in rank 7th/2nd'''

    # for white_rook in WR:
    #     if (not ((white_rook > 55) or (white_rook < 48))):
    #         evaluation += 1

    # for black_rook in BR:
    #     if (not ((black_rook > 15) or (black_rook < 8))):
    #         evaluation -= 1

    # '''Criterion 5: Check for King safety'''

    # '''Criterion 5.1: Check for safety King position'''

    # if (WK in (1,2,5,6)):       evaluation += 0.5
    # if (BK in (57,58,61,62)):   evaluation -= 0.5

    # '''Criterion 5.2: Check for double check'''

    # if (len(board.attackers(chess.BLACK, list(WK)[0])) >= 2): evaluation -= 2
    # if (len(board.attackers(chess.WHITE, list(BK)[0])) >= 2): evaluation += 2

    # '''Criterion 6: Queen mobility'''

    # for white_queen in WQ:
    #     if (len(board.attacks(white_queen)) >  8): evaluation += 0.1
    #     if (len(board.attacks(white_queen)) > 12): evaluation += 0.1
    
    # for black_queen in BQ:
    #     if (len(board.attacks(black_queen)) >  8): evaluation -= 0.1
    #     if (len(board.attacks(black_queen)) > 12): evaluation -= 0.1


    # '''Criterion 7: Knight mobility'''

    # for white_knight in WN:
    #     if (len(board.attacks(white_knight)) > 3): evaluation += 0.05
    #     if (len(board.attacks(white_knight)) > 6): evaluation += 0.05

    # for black_knight in BN:
    #     if (len(board.attacks(black_knight)) > 3): evaluation -= 0.05
    #     if (len(board.attacks(black_knight)) > 6): evaluation -= 0.05

    # '''Criterion 8: Bishop mobility'''

    # for white_bishop in WB:
    #     if (len(board.attacks(white_bishop)) > 5): evaluation += 0.05
    #     if (len(board.attacks(white_bishop)) > 8): evaluation += 0.05

    # for black_bishop in BB:
    #     if (len(board.attacks(black_bishop)) > 5): evaluation -= 0.05
    #     if (len(board.attacks(black_bishop)) > 8): evaluation -= 0.05

    return round(evaluation, 3)