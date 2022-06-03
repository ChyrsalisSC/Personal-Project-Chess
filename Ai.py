from  stockfish import Stockfish
import random



stockfish = Stockfish(path = "/usr/games/stockfish")

stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0")






def setstockfish(fen):
	stockfish.set_fen_position(fen)
	return

def getstockmovefen(move):
	col = {'a':0, 'b': 1,'c': 2,'d':3,'e':4,'f':5,'g':6,'h':7}
	ranks = {'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6, '1':7}

	#print(move)
	stockfish.set_fen_position(move)
	next_move = stockfish.get_best_move()
	#print(f"sctokfish moves to {next_move}")
	start = next_move[0:2]
	end = next_move[2:4]
	#print(f"sctokfish moves to {next_move}")
	start = ranks[start[1]],  int(col[start[0]])
	end = ranks[end[1]], int(col[end[0]])
	#print(f"sctokfish moves to {next_move}")
	#print(start)
	#print(end)

	return start , end


	files = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g', 7:'h'}
	ranks = {0:8,1:7,2:6,3:5,4:4,5:3,6:2, 7:1}
	return str(files[self.startcol]) + str(ranks[self.startrow]) + str(files[self.endcol]) + str(ranks[self.endrow])



def getstockmove(move):
	mapping  = {'a':0, 'b': 1,'c': 2,'d':3,'e':4,'f':5,'g':6,'h':7}


	stockfish.make_moves_from_current_position([move])
	next_move = stockfish.get_best_move()
	start = next_move[0:2]
	end = next_move[2:4]

	start = mapping[start[0]], int(start[1])-1
	end=  mapping[end[0]], int(end[1])-1
	print(f" start = {start} and = {end}")

	return start , end






"""
{
    "Debug Log File": "waste.txt",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 1024, # 1024 MB for the hash table - you may want to increase/decrease this, depending on how much RAM you want to use. Should also be kept as some power of 2.
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 20,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 1350
}
"""



