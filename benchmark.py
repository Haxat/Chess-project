import time
import chess
import bots
import search



def benchmark_position(board,depth):
    stats=search.init_stats()

    legal_moves=list(board.legal_moves)
    start = time.perf_counter()
    best_move=bots.BotAlphaBeta(board,legal_moves,depth,stats)
    end = time.perf_counter()

    elapsed = end - start
    nodes=stats["nodes"]
    leaves = stats["leaves"]
    internal_nodes = nodes - leaves
    nps=nodes/elapsed if elapsed > 0 else 0
    q_nodes=stats["q_nodes"]

    return{
        "best_move":best_move,
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



def run_benchmark_suite():
    depth = 2
    for name,fen in TEST_POSITIONS:
        board=chess.Board(fen)
        

        result = benchmark_position(board,depth)

        print("===============Benchmark=================")
        print(f"Position          :{name}")
        print(f"Depth             :{depth}")
        print(f"Best move         :{result['best_move']}")
        print(f"Time              :{result['time']:.4f}s")
        print(f"Nodes             :{result['nodes']}")
        print(f"Internal Nodes    :{result['internal_nodes']}")
        print(f"Leaves            :{result['leaves']}")
        print(f"Cutoffs           :{result['cutoffs']}")
        print(f"NPS               :{result['nps']:.0f}")
        print(f"Quiescence Nodes  :{result['q_nodes']}")


if __name__=="__main__":
    run_benchmark_suite()