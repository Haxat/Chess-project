import chess

PAWN_TABLE =   [0,0,0,0,0,0,0,0,
                1,1,1,1,1,1,1,1,
                1,1,2,2,2,2,1,1,
                1,2,3,3,3,3,2,1,
                2,3,4,4,4,4,3,2,
                3,4,5,5,5,5,4,3,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,]
KNIGHT_TABLE=  [-5,-4,-4,-4,-4,-4,-4,-5,
                -4,-2,-2,-2,-2,-2,-2,-4,
                -4,+0,+2,+2,+2,+2,+0,-4,
                -4,+3,+3,+5,+5,+3,+3,-4,
                -4,+3,+3,+5,+5,+3,+3,-4,
                -4,+0,+2,+2,+2,+2,+0,-4,
                -4,-2,-2,-2,-2,-2,-2,-4,
                -5,-4,-4,-4,-4,-4,-4,-5,]

BISHOP_TABLE=  [-1,-1,-1,-1,-1,-1,-1,-1,
                -1,+0,+0,+0,+0,+0,+0,-1,
                -1,+0,+2,+2,+2,+2,+0,-1,
                -1,+2,+2,+2,+2,+2,+2,-1,
                -1,+2,+2,+2,+2,+2,+2,-1,
                -1,+0,+2,+2,+2,+2,+0,-1,
                -1,+0,+0,+0,+0,+0,+0,-1,
                -1,-1,-1,-1,-1,-1,-1,-1,]

ROOK_TABLE=    [-1,+0,+1,+2,+2,+1,+0,-1,
                -1,+0,+1,+2,+2,+1,+0,-1,
                -1,+0,+1,+2,+2,+1,+0,-1,
                -1,+0,+1,+2,+2,+1,+0,-1,
                -1,+0,+1,+2,+2,+1,+0,-1,
                -1,+0,+1,+2,+2,+1,+0,-1,
                +1,+2,+2,+2,+2,+2,+2,+1,
                -1,+0,+1,+2,+2,+1,+0,-1,]

QUEEN_TABLE=   [+0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,
                +0,+0,+1,+2,+2,+1,+0,+0,]

KING_MIDGAME_TABLE=  [+2,+3,+1,-3,-3,+1,+3,+2,
                    -3,-3,-3,-4,-4,-4,-3,-3,
                    -5,-5,-5,-5,-5,-5,-5,-5,
                    -5,-5,-5,-5,-5,-5,-5,-5,
                    -5,-5,-5,-5,-5,-5,-5,-5,
                    -5,-5,-5,-5,-5,-5,-5,-5,
                    -5,-5,-5,-5,-5,-5,-5,-5,
                    -5,-5,-5,-5,-5,-5,-5,-5,]

KING_END_TABLE= [-5,-4,-4,-4,-4,-4,-4,-5,
                    -4,-2,-2,-2,-2,-2,-2,-4,
                    -4,+0,+2,+2,+2,+2,+0,-4,
                    -4,+3,+3,+5,+5,+3,+3,-4,
                    -4,+3,+3,+5,+5,+3,+3,-4,
                    -4,+0,+2,+2,+2,+2,+0,-4,
                    -4,-2,-2,-2,-2,-2,-2,-4,
                    -5,-4,-4,-4,-4,-4,-4,-5,]


def is_endgame(board):
     return (
        len(board.pieces(chess.QUEEN, chess.WHITE)) == 0
        and len(board.pieces(chess.QUEEN, chess.BLACK)) == 0
    )

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
    board_WHITE=board.copy(stack=False)
    board_WHITE.turn=chess.WHITE

    board_BLACK=board.copy(stack=False)
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
    outcome = board.outcome()
    if outcome is None:
        return None
    if outcome.winner is True:
        return float('inf')
    elif outcome.winner is False:
        return float('-inf')    
    else:
        return 0    
    

def evaluate_fast(board):
    score = 0      
    
    # matériel seulement
    score += len(board.pieces(chess.PAWN, chess.WHITE))
    score += len(board.pieces(chess.KNIGHT, chess.WHITE))*3
    score += len(board.pieces(chess.BISHOP, chess.WHITE))*3
    score += len(board.pieces(chess.ROOK, chess.WHITE))*5
    score += len(board.pieces(chess.QUEEN, chess.WHITE))*9

    score -= len(board.pieces(chess.PAWN, chess.BLACK))
    score -= len(board.pieces(chess.KNIGHT, chess.BLACK))*3
    score -= len(board.pieces(chess.BISHOP, chess.BLACK))*3
    score -= len(board.pieces(chess.ROOK, chess.BLACK))*5
    score -= len(board.pieces(chess.QUEEN, chess.BLACK))*9

    cases_centre = [chess.D4, chess.E4, chess.D5, chess.E5]

    #Contrôle du centre
    for case in cases_centre:
        piece = board.piece_at(case)
        if (piece is None):
            continue
        elif (piece.color==chess.WHITE):
            score+=0.1
        else:
            score-=0.1

    #Tables
    for square in board.pieces(chess.PAWN,chess.WHITE):
        score+=PAWN_TABLE[square]*0.1
    for square in board.pieces(chess.PAWN,chess.BLACK):
        score-=PAWN_TABLE[chess.square_mirror(square)]*0.1


    for square in board.pieces(chess.KNIGHT,chess.WHITE):
        score+=KNIGHT_TABLE[square]*0.05
    for square in board.pieces(chess.KNIGHT,chess.BLACK):
        score-=KNIGHT_TABLE[chess.square_mirror(square)]*0.05

    for square in board.pieces(chess.BISHOP,chess.WHITE):
        score+=BISHOP_TABLE[square]*0.1
    for square in board.pieces(chess.BISHOP,chess.BLACK):
        score-=BISHOP_TABLE[chess.square_mirror(square)]*0.1

    for square in board.pieces(chess.ROOK,chess.WHITE):
        score+=ROOK_TABLE[square]*0.05
    for square in board.pieces(chess.ROOK,chess.BLACK):
        score-=ROOK_TABLE[chess.square_mirror(square)]*0.05

    for square in board.pieces(chess.QUEEN,chess.WHITE):
        score+=QUEEN_TABLE[square]*0.05
    for square in board.pieces(chess.QUEEN,chess.BLACK):
        score-=QUEEN_TABLE[chess.square_mirror(square)]*0.05

    if is_endgame(board):
        for square in board.pieces(chess.KING,chess.WHITE):
            score+=KING_END_TABLE[square]*0.05
        for square in board.pieces(chess.KING,chess.BLACK):
            score-=KING_END_TABLE[chess.square_mirror(square)]*0.05
    else:
        for square in board.pieces(chess.KING,chess.WHITE):
            score+=KING_MIDGAME_TABLE[square]*0.05
        for square in board.pieces(chess.KING,chess.BLACK):
            score-=KING_MIDGAME_TABLE[chess.square_mirror(square)]*0.05

    return score   

    