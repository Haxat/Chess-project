from evaluation import evaluate, terminal_score, evaluate_fast




def init_stats():
    return{
        "nodes": 0,
        "leaves": 0,
        "cutoffs": 0,
        "max_depth_reached": 0,
        "q_nodes": 0
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
        return quiescence_search(board,alpha,beta,maximizing_player,stats)
    
    legal_moves = order_moves(board,list(board.legal_moves))

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

def order_moves(board,legal_moves):
    capture=[]
    non_capture=[]
    for m in legal_moves:
        if board.is_capture(m):
            capture.append(m)
        else:
            non_capture.append(m)
    return capture + non_capture

def quiescence_search(board,alpha,beta,maximizing_player,stats):
    ts = terminal_score(board)
    if ts is not None:
        return ts
    stand_pat=evaluate_fast(board)
    best_score=stand_pat
    if maximizing_player:
        if stand_pat>=beta:
            return stand_pat
        alpha=max(alpha,stand_pat)

        legal_moves=list(board.legal_moves)
        for m in legal_moves:
            if(board.is_capture(m)):
                board.push(m)
                stats["q_nodes"] +=1
                score=quiescence_search(board,alpha,beta,not maximizing_player,stats)
                board.pop()
                best_score=max(best_score,score)
                alpha=max(alpha,best_score)
                if alpha>=beta:
                    break
    else :
        if stand_pat<=alpha:
            return stand_pat
        beta=min(beta,stand_pat)

        legal_moves=list(board.legal_moves)
        for m in legal_moves:
            if(board.is_capture(m)):
                board.push(m)
                stats["q_nodes"] +=1
                score=quiescence_search(board,alpha,beta,not maximizing_player,stats)
                board.pop()
                best_score=min(best_score,score)
                beta=min(beta,best_score)
                if alpha>=beta:
                    break
    return best_score            

        