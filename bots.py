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




def BotMiniMax(board, legal_moves, depth,stats,eval_fn):
    best_move=legal_moves[0]
    if (board.turn==chess.WHITE):
        best_score= float('-inf')
        for m in legal_moves:
            board.push(m)
            score=search.MiniMax(board,depth-1,False,stats,eval_fn)
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
            score=search.MiniMax(board,depth-1,True,stats,eval_fn)
            board.pop()
            if(score==float('-inf')):
                best_score=score
                best_move=m
                break
            elif (score<best_score):
                best_score=score
                best_move=m
    
    return best_move




def BotAlphaBeta(board,legal_moves,depth,stats,eval_fn,moves_ordernoring_fn):
    best_move=legal_moves[0]
    alpha=float("-inf")
    beta=float("inf")
    if (board.turn==chess.WHITE):
        best_score= float('-inf')
        for m in legal_moves:
            board.push(m)
            score=search.AlphaBeta(board,depth-1,alpha,beta,False,stats,eval_fn,moves_ordernoring_fn)
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
            score=search.AlphaBeta(board,depth-1,alpha,beta,True,stats,eval_fn,moves_ordernoring_fn)
            board.pop()
            if(score==float('-inf')):
                best_score=score
                best_move=m
                break
            elif (score<best_score):
                best_score=score
                best_move=m
            beta = min(beta, best_score)    
    return best_move

