import chess
import random

board= chess.Board()

def BotRandom(legal_moves):
    return random.choice(legal_moves)

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

def Botgreedy(board,legal_moves):
    score=0
    meilleur_coup = legal_moves[0]
    if(board.turn==chess.WHITE):
        score_meilleur_coup=float('-inf')
        for m in legal_moves:
            board.push(m)
            score = terminal_score(board)
            #Coup Normal
            if(score is None):
                score=evaluate(board)
            board.pop()
            if(score==float('inf')):
                return m
            elif((score==score_meilleur_coup and random.random()<0.5) or score>score_meilleur_coup):
                    meilleur_coup=m
                    score_meilleur_coup=score
            
    else:
        score_meilleur_coup=float('inf')
        for m in legal_moves:
            board.push(m)
            score=terminal_score(board)
            #Coup Normal
            if (score is None):
                score=evaluate(board)
            board.pop()
            if(score==float('-inf')):
                return m
            elif((score==score_meilleur_coup and random.random()<0.5) or score<score_meilleur_coup):
                meilleur_coup=m
                score_meilleur_coup=score
    return meilleur_coup

#Joueur
def Humain(board,legal_moves):

    while(True):
        print("Coups possibles:", [m.uci() for m in legal_moves])
        m=input("Faire un coup: ")
        m = m.strip().lower()

        if(m=="exit"):
            print("Sortie du jeu")
            exit()

        try:
            m = chess.Move.from_uci(m)
        except ValueError:
            print("Erreur le format doit être UCI") 
            continue
        if (board.is_legal(m)):
            break
        else:
            print("Erreur ",m," est un coup illégal")
            print(board)
    return m






def MiniMax(board,depth,maximizing_player):
    ts = terminal_score(board)
    if (ts is not None):
        return ts
    
    if(depth==0):
        return evaluate(board)
    
    legal_moves = list(board.legal_moves)

    if (maximizing_player):
        best_score=float('-inf')
        for m in legal_moves:         
            board.push(m)
            score=MiniMax(board,depth-1,not maximizing_player)
            board.pop()
            best_score=max(score,best_score)
    else:
        best_score=float('inf')
        for m in legal_moves:
            board.push(m)
            score=MiniMax(board,depth-1,not maximizing_player)
            board.pop()
            best_score=min(score,best_score)
    return best_score



def BotMiniMax(board, legal_moves, depth):
    best_move=legal_moves[0]
    if (board.turn==chess.WHITE):
        best_score= float('-inf')
        for m in legal_moves:
            board.push(m)
            score=MiniMax(board, depth-1, False)
            board.pop()
            if(score==float('inf')):
                return m
            elif (score>best_score):
                best_score=score
                best_move=m
    else:
        best_score= float(('inf'))
        for m in legal_moves:  
            board.push(m)
            score=MiniMax(board, depth-1, True)
            board.pop()
            if(score==float('-inf')):
                return m
            elif (score<best_score):
                best_score=score
                best_move=m
    return best_move






#Jeu

while (not board.is_game_over()):
    print(board)
    legal_moves = list(board.legal_moves)

    #Blanc
    if(board.turn==chess.WHITE):
        print("Coup Blanc: ")
        m=BotRandom(legal_moves)
    #Noir
    else:
        print("Coup Noir: ")
        m=Botgreedy(board,legal_moves)
    board.push(m)
    



#Résultat
print(board)
if(board.result()=="1-0"):
    print("Victoire blanc")
elif(board.result()=="0-1"):
    print("Victoire noir")
elif(board.result()=="1/2-1/2"):
    print("Nulle")
else:
    print("Erreur")
print(board.outcome())




