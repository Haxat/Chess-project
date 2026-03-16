import chess


def evaluate(board):
    score=0
    score+=len(board.pieces(chess.PAWN, chess.WHITE))
    score+=len(board.pieces(chess.KNIGHT, chess.WHITE))*3
    score+=len(board.pieces(chess.BISHOP, chess.WHITE))*3
    score+=len(board.pieces(chess.ROOK, chess.WHITE))*5
    score+=len(board.pieces(chess.QUEEN, chess.WHITE))*9

    score-=len(board.pieces(chess.PAWN, chess.BLACK))
    score-=len(board.pieces(chess.KNIGHT, chess.BLACK))*3
    score-=len(board.pieces(chess.BISHOP, chess.BLACK))*3
    score-=len(board.pieces(chess.ROOK, chess.BLACK))*5
    score-=len(board.pieces(chess.QUEEN, chess.BLACK))*9

    #Bonnus sur le nb de coups légaux
    board_WHITE=board.copy()
    board_WHITE.turn=chess.WHITE

    board_BLACK=board.copy()
    board_BLACK.turn=chess.BLACK

    legal_moves_WHITE=list(board_WHITE.legal_moves)
    legal_moves_BLACK=list(board_BLACK.legal_moves)

    score+=len(legal_moves_WHITE)*0.1 - len(legal_moves_BLACK)*0.1



    #Contrôle du centre
    cases_centre = [chess.D4, chess.E4, chess.D5, chess.E5]

    for case in cases_centre:
        piece = board.piece_at(case)
        if (piece is None):
            continue
        elif (piece.color==chess.WHITE):
            score+=0.1
        else:
            score-=0.1

    return score

def terminal_score(board):
    if (not board.is_game_over()):
        return None
    
    outcome = board.outcome()

    if (outcome.winner is True):
        return float('inf')
    elif (outcome.winner is False):
        return float('-inf')    
    else:
        return 0    