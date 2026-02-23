import chess

board= chess.Board()

while (True):
    print(board)
    while(True):
        legal_moves = list(board.legal_moves)
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