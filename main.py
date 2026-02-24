import chess
import random

board= chess.Board()

def BotRandom(legal_moves):
    return random.choice(legal_moves)


while (not board.is_game_over()):
    print(board)
    legal_moves = list(board.legal_moves)
    if(board.turn==chess.WHITE):
        #Bot
        move=BotRandom(legal_moves)
    else:
        #Joueur
        while(True):
            print("Coups possibles:", [move.uci() for move in legal_moves])
            move=input("Faire un coup: ")
            move = move.strip().lower()

            if(move=="exit"):
                print("Sortie du jeu")
                exit()

            try:
                move = chess.Move.from_uci(move)
            except ValueError:
                print("Erreur le format doit être UCI") 
                continue
            if (board.is_legal(move)):
                break
            else:
                print("Erreur ",move," est un coup illégal")
                print(board)
    board.push(move)
    

print(board)
if(board.result()=="1-0"):
    print("Victoire blanc")
elif(board.result()=="0-1"):
    print("Victoire noir")
elif(board.result()=="1/2-1/2"):
    print("Nulle")
else:
    print("Erreur")




