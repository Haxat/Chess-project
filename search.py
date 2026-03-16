import chess
from evaluation import evaluate, terminal_score

def init_stats():
    return{
        "nodes": 0,
        "leaves": 0,
        "cutoffs": 0,
    }



def MiniMax(board,depth,maximizing_player,stats):

    stats["nodes"] +=1
    ts = terminal_score(board)
    if (ts is not None):
        stats["leaves"] +=1
        return ts
    
    if(depth==0):
        stats["leaves"] +=1
        return evaluate(board)
    
    legal_moves = list(board.legal_moves)

    if (maximizing_player):
        best_score=float('-inf')
        for m in legal_moves:         
            board.push(m)
            score=MiniMax(board,depth-1,not maximizing_player,stats)
            board.pop()
            best_score=max(score,best_score)
    else:
        best_score=float('inf')
        for m in legal_moves:
            board.push(m)
            score=MiniMax(board,depth-1,not maximizing_player,stats)
            board.pop()
            best_score=min(score,best_score)
    return best_score


def AlphaBeta(board,depth,alpha,beta,maximizing_player,stats):
    stats["nodes"] +=1
    ts = terminal_score(board)

    if (ts is not None):
        stats["leaves"] +=1
        return ts
    
    if(depth==0):
        stats["leaves"] +=1
        return evaluate(board)
    
    legal_moves = list(board.legal_moves)

    if (maximizing_player):
        best_score=float('-inf')
        for m in legal_moves:         
            board.push(m)
            score=AlphaBeta(board,depth-1,alpha,beta,not maximizing_player,stats)
            board.pop()
            best_score=max(best_score,score)
            alpha=max(alpha,best_score)
            if(alpha>=beta):
                stats["cutoffs"] += 1
                break
    else:
        best_score=float('inf')
        for m in legal_moves:
            board.push(m)
            score=AlphaBeta(board,depth-1,alpha,beta,not maximizing_player,stats)
            board.pop()
            best_score=min(best_score,score)
            beta=min(beta,best_score)
            if(alpha>=beta):
                stats["cutoffs"] += 1
                break
    return best_score