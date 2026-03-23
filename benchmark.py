import time
import chess
import bots
import search
import evaluation
import csv

def benchmark_position(board,depth,engine_config):
    stats=search.init_stats()

    eval_fn=engine_config["eval_fn"]
    move_ordering_fn=engine_config["move_ordering_fn"]

    legal_moves=list(board.legal_moves)
    start = time.perf_counter()
    best_move=bots.BotAlphaBeta(board,legal_moves,depth,stats,eval_fn,move_ordering_fn)
    end = time.perf_counter()

    elapsed = end - start
    nodes=stats["nodes"]
    leaves = stats["leaves"]
    internal_nodes = nodes - leaves
    nps=nodes/elapsed if elapsed > 0 else 0
    q_nodes=stats["q_nodes"]

    return{
        "config_engine":engine_config["name"],
        "best_move":str(best_move),
        "time":elapsed,
        "nodes":nodes,
        "leaves":leaves ,
        "internal_nodes": internal_nodes,
        "cutoffs":stats["cutoffs"],
        "nps":nps,
        "q_nodes":q_nodes
    }


def build_fen_from_san(moves):
    board=chess.Board()
    for move in moves:
        board.push_san(move)
    return board.fen()



TEST_POSITIONS = [
    ("Initiale", chess.STARTING_FEN),

    ("Italienne", build_fen_from_san([
        "e4", "e5",
        "Nf3", "Nc6",
        "Bc4", "Bc5",
        "c3", "Nf6",
        "d3", "d6"
    ])),

    ("Sicilienne ouverte", build_fen_from_san([
        "e4", "c5",
        "Nf3", "d6",
        "d4", "cxd4",
        "Nxd4", "Nf6",
        "Nc3", "a6"
    ])),

    ("Milieu ouvert", build_fen_from_san([
        "e4", "e5",
        "Nf3", "Nc6",
        "Bc4", "Nf6",
        "d4", "exd4",
        "e5", "d5",
        "Bb5", "Ne4",
        "Nxd4", "Bd7"
    ])),

    ("Milieu fermé", build_fen_from_san([
        "d4", "d5",
        "c4", "e6",
        "Nc3", "Nf6",
        "Nf3", "Be7",
        "Bg5", "O-O",
        "e3", "h6",
        "Bh4", "b6"
    ])),

    ("Finale simple", "8/8/3k4/3P4/3K4/8/8/8 w - - 0 1"),
]



def save_benchmark_results_csv(results, filename):
    if not results:
        return
    
    fieldnames=list(results[0].keys())

    with open(filename, mode="w", newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def run_benchmark_suite(depth,engine_config):
    results=[]
    for name,fen in TEST_POSITIONS:
        board=chess.Board(fen)
        
        result = benchmark_position(board,depth,engine_config)
        result["position"] = name
        result["depth"] = depth

        print("===============Benchmark=================")
        print(f"Config Name       :{result['config_engine']}")
        print(f"Position          :{result['position']}")
        print(f"Depth             :{result['depth']}")
        print(f"Best move         :{result['best_move']}")
        print(f"Time              :{result['time']:.4f}s")
        print(f"Nodes             :{result['nodes']}")
        print(f"Internal Nodes    :{result['internal_nodes']}")
        print(f"Leaves            :{result['leaves']}")
        print(f"Cutoffs           :{result['cutoffs']}")
        print(f"NPS               :{result['nps']:.0f}")
        print(f"Quiescence Nodes  :{result['q_nodes']}")

        results.append(result)
    return results


def print_benchmark_summary(results):
    if not results:
        return
    
    total_time=sum(r["time"] for r in results)
    total_nodes=sum(r["nodes"] for r in results)
    total_q_nodes=sum(r["q_nodes"] for r in results)

    print("===============Summary=================")
    print(f"Nombres de runs        :{len(results)}")
    print(f"Temps totals           :{total_time:.4f}s")
    print(f"Nodes totals           :{total_nodes}")
    print(f"Total q_nodes          :{total_q_nodes}")
    print(f"Temps moyen            :{total_time/len(results):.4f}s")




#Engine 

ENGINE_MVV_LVA={
    "name" : "mvv_lva",
    "eval_fn":evaluation.evaluate_fast,
    "move_ordering_fn":search.ordering_moves_MVV_LVA,
}

ENGINE_BASIC={
    "name":"basic",
    "eval_fn":evaluation.evaluate_fast,
    "move_ordering_fn":search.ordering_moves_simple,
}

if __name__=="__main__":
    depth=5
    engine_config=ENGINE_BASIC
    results= run_benchmark_suite(depth,engine_config)
    print_benchmark_summary(results)
    save_benchmark_results_csv(results,"benchmark_results.csv")

