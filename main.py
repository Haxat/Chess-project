import chess
import random
import time
 
import search
import evaluation

def BotRandom(legal_moves):
    return random.choice(legal_moves)


def Botgreedy(board,legal_moves):
    score=0
    meilleur_coup = legal_moves[0]
    if(board.turn==chess.WHITE):
        score_meilleur_coup=float('-inf')
        for m in legal_moves:
            board.push(m)
            score = evaluation.terminal_score(board)
            #Coup Normal
            if(score is None):
                score=evaluation.evaluate(board)
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
            score=evaluation.terminal_score(board)
            #Coup Normal
            if (score is None):
                score=evaluation.evaluate(board)
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









def BotMiniMax(board, legal_moves, depth):
    time_start=time.perf_counter()
    stats = search.init_stats()
    best_move=legal_moves[0]
    if (board.turn==chess.WHITE):
        best_score= float('-inf')
        for m in legal_moves:
            board.push(m)
            score=search.MiniMax(board, depth-1, False,stats)
            board.pop()
            if(score==float('inf')):
                best_score=score
                best_move=m
                break
            elif (score>best_score):
                best_score=score
                best_move=m
    else:
        best_score= float(('inf'))
        for m in legal_moves:  
            board.push(m)
            score=search.MiniMax(board, depth-1, True,stats)
            board.pop()
            if(score==float('-inf')):
                best_score=score
                best_move=m
                break
            elif (score<best_score):
                best_score=score
                best_move=m
    time_end=time.perf_counter()
    print(f"Temps du coup: {time_end-time_start:.4f}")
    print("Cutoffs :", stats["cutoffs"])
    print("Internal nodes :", stats["nodes"] - stats["leaves"])
    print("Leaves visited :", stats["leaves"])
    
    
    return best_move




def BotAlphaBeta(board, legal_moves, depth):
    time_start=time.perf_counter()
    stats = search.init_stats()
    best_move=legal_moves[0]
    alpha=float("-inf")
    beta=float("inf")
    if (board.turn==chess.WHITE):
        best_score= float('-inf')
        for m in legal_moves:
            board.push(m)
            score=search.AlphaBeta(board, depth-1,alpha,beta, False,stats)
            board.pop()
            if(score==float('inf')):
                best_score=score
                best_move=m
                break
            elif (score>best_score):
                best_score=score
                best_move=m
            alpha = max(alpha, best_score)
    else:
        best_score= float('inf')
        for m in legal_moves:  
            board.push(m)
            score=search.AlphaBeta(board, depth-1, alpha, beta, True,stats)
            board.pop()
            if(score==float('-inf')):
                best_score=score
                best_move=m
                break
            elif (score<best_score):
                best_score=score
                best_move=m
            beta = min(beta, best_score)    
    time_end=time.perf_counter()
    print(f"Temps du coup: {time_end-time_start:.4f}")
    print("Cutoffs :", stats["cutoffs"])
    print("Internal nodes :", stats["nodes"] - stats["leaves"])
    print("Leaves visited :", stats["leaves"])
    return best_move


#Jeu
board= chess.Board()
nb_coup=0


print(board)
while (not board.is_game_over()):
    print("-----------------------------------------------------")
    legal_moves = list(board.legal_moves)

    #Blanc
    if(board.turn==chess.WHITE):
        m=BotMiniMax(board,legal_moves,2)
        print(f"Coup Blanc: {m}")
    #Noir
    else:
        m=BotAlphaBeta(board,legal_moves,2)
        print(f"Coup Noir: {m}")
    print(f"Evaluation: {evaluation.evaluate(board)}")
    board.push(m)
    print(board)
    nb_coup+=1
    



#Résultat
print("-----------------------------------------------------")
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
print(f"Nombre de coups joué {nb_coup}")



