import chess

import bots
import evaluation
import search



def run_game():
    #Jeu
    board= chess.Board()
    nb_coup=0


    print(board)
    while (not board.is_game_over()):
        print("-----------------------------------------------------")
        legal_moves = list(board.legal_moves)
        stats=search.init_stats()
        #Blanc
        if(board.turn==chess.WHITE):
            m=bots.BotAlphaBeta(board,legal_moves,5,stats)
            print(f"Coup Blanc: {m}")
        #Noir
        else:
            m=bots.BotAlphaBeta(board,legal_moves,2,stats)
            print(f"Coup Noir: {m}")
        board.push(m)
        print(f"Evaluation: {evaluation.evaluate(board)}")
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



if __name__=="__main__":
    run_game()