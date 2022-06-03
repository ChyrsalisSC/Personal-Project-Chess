import pygame


#binary numbers
"""

Convection is from Sebatian Lagues Coding adventure:chess AI youtube video


none = 0
King = 1
Pawn = 2
Knight = 3
Bishup = 4
Rook = 5
Queen = 6

White = 8
Black = 16
"""
peices = {"none": 0,
"n"  : 1, #knight
"p" : 2,
"k": 3,
"b": 4,
"r"  : 5,
"q" : 6,
"White" : 8,
"Black" : 16}

ID = ['B', 'b', 'K', 'k', 'N', 'n', 'P', 'p', 'Q', 'q', 'R', 'r']
"""
I wanted to use The fen string notation since i can copy paste it 
directly from the PGN of chess.com"""

#There are 8 ranks 1 to 8 each rank is a row from left to right across baord
#Files numbers a to h and are colms going from top to bottom
#startFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"

class Gamestate():
	def __init__(self):
		self.board = [[None for i in range(8)] for x in range(8)]
		self.whiteToMove = True
		self.moveLog =[]
		self.movefucntion = {'p': self.pawnmoves, 'r': self.rookmoves, 'b': self.bishupmoves,'n': self.knightmoves,
		'q': self.queenmoves,'k': self.kingmoves, }
		self.whiteking = (7,4)
		self.blackking = (0,4)
		self.checkmate = False
		self.stalemate = False
		self.empassantpos = ()
		self.CurrCastlerights = CaslteRights(True, True, True, True)
		self.Castlelog = [CaslteRights(self.CurrCastlerights.wks,self.CurrCastlerights.bks, 
			self.CurrCastlerights.wqs,self.CurrCastlerights.bqs)]

	def LoadFenString(self, fenstr):
		print(f"Loaded String:{fenstr}")
		file = 0
		rank = 0 #counting from 0
		fensplit = fenstr.split(' ',1)[0]
		print(fensplit)
		wk, wq ,bk ,bq = False, False, False, False
		for item in fensplit:
			#print(item)
			if (item == "/"):
				rank = 0
				file +=1
			else:
				#check if its a digit or a charater
				if item.isdigit():
					#print(f"{item} is a digit")
					for i in range(int(item)):
						self.board[file][rank] = None
						rank+=1
					 #add that many over to the right
				else:
					self.board[file][rank] = item
					rank+=1
		for item in self.board:

			print(item)


		turn = fenstr.split(' ',2)[1]
		if turn == 'b':
			self.whiteToMove = False
		can_castle = fenstr.split(' ',3)[2]
		strlen = len(can_castle)
		print(can_castle)
		if can_castle == "-":
			self.CurrCastlerights.wks = False
			self.CurrCastlerights.wqs = False
			self.CurrCastlerights.bks = False
			self.CurrCastlerights.bqs = False
			return
		for letter in can_castle:
			if letter == 'K':
				wk = True 
			if letter == 'Q':
				wq = True
			if letter == 'k':
				bk= True 
			if letter == 'q':
				bq = True 

		self.CurrCastlerights.wks = wk
		self.CurrCastlerights.wqs = wq
		self.CurrCastlerights.bks = bk
		self.CurrCastlerights.bqs = bq


		return

	def makemove(self, move):
		self.board[move.startrow][move.startcol] = None
		self.board[move.endrow][move.endcol] = move.piecemoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove #swap
		if move.piecemoved == 'K': 
			self.whiteking = (move.endrow, move.endcol)
		if move.piecemoved == 'k': 
			self.blackking = (move.endrow, move.endcol)


		if move.promotion:
			if move.piecemoved.isupper():
				self.board[move.endrow][move.endcol] ='Q'
			else:
				self.board[move.endrow][move.endcol] ='q'

		if move.isempmove:
			self.board[move.startrow][move.endcol] = None

		#update emppos posotiions

		if (move.piecemoved == 'p' or move.piecemoved =='P') and abs(move.startrow - move.endrow) == 2:
			self.empassantpos =((move.startrow+move.endrow)//2, move.startcol)
		else:
			self.empassantpos = ()


		if move.iscasltmove:
			if move.endcol - move.startcol == 2: #kingside
				self.board[move.endrow][move.endcol-1] = self.board[move.endrow][move.endcol+1] #moves rook
				self.board[move.endrow][move.endcol+1] = None
			else: #queenside
				self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-2]
				self.board[move.endrow][move.endcol-2] = None

		self.updatecastlerights(move)
		self.Castlelog.append(CaslteRights(self.CurrCastlerights.wks,self.CurrCastlerights.bks, 
			self.CurrCastlerights.wqs,self.CurrCastlerights.bqs))


	def redo(self): 
		#make this move eiffiecatnt by making fen cupdate the gamestate
		if(len(self.moveLog) != 0):
			move = self.moveLog.pop()
			self.board[move.startrow][move.startcol] = move.piecemoved
			self.board[move.endrow][move.endcol] = move.peicecaptured	
			self.whiteToMove = not self.whiteToMove #swap
			if move.piecemoved == 'K': #lower
				self.whiteking = (move.startrow, move.startcol)
			if move.piecemoved == 'k': #upper
				self.blackking = (move.startrow, move.startcol)

			if move.isempmove:
				self.board[move.endrow][move.endcol] = None
				self.board[move.startrow][move.endcol] = move.peicecaptured
				self.empassantpos = (move.endrow, move.endcol)

			if (move.piecemoved == 'p' or move.piecemoved == 'P') and abs(move.startrow - move.endrow) == 2:
				self.empassantpos = ()

			self.Castlelog.pop() #rid the appened castle rights
			self.CurrCastlerights 
			newrights =  self.Castlelog[-1]
			self.CurrCastlerights = CaslteRights(newrights.wks, newrights.bks, newrights.wqs, newrights.bqs)
			#undo castle

			if move.iscasltmove:
				if move.endcol - move.startcol == 2:
					self.board[move.endrow][move.endcol+1] = self.board[move.endrow][move.endcol-1] #move rook back
					self.board[move.endrow][move.endcol-1] = None
				else:
					self.board[move.endrow][move.endcol-2] = self.board[move.endrow][move.endcol+1] #move rook back
					self.board[move.endrow][move.endcol+1] = None


	def updatecastlerights(self, move):
		if move.piecemoved =='K':
			self.CurrCastlerights.wks = False
			self.CurrCastlerights.wqs = False
		elif move.piecemoved == 'k':
			self.CurrCastlerights.bks = False
			self.CurrCastlerights.bqs = False
		elif move.piecemoved == 'R': 
			if move.startrow ==7:
				if move.startcol == 0: #left
					self.CurrCastlerights.wqs = False
				elif move.startcol == 7:
					self.CurrCastlerights.wks = False
		elif move.piecemoved == 'r': 
			if move.startrow == 0:
				if move.startcol == 0: #left
					self.CurrCastlerights.bqs = False
				elif move.startcol == 7:
					self.CurrCastlerights.bks = False



	def getallmoves(self):
		moves = [] #overide -
		for row in range(len(self.board)):
			for col in range(len(self.board)):
				piece = self.board[row][col]
				
				if piece != None:
					#print(piece)

					if piece.isupper() == False:
						pc = "black"
					else:
						pc = "white"
					
					if (pc == "white" and self.whiteToMove) or (pc == "black" and not self.whiteToMove):
						piece = piece.lower()
						self.movefucntion[piece](row,col,moves) # lower the peice
						
		#for item in moves:
		#	print(item.ID)
		return moves

	def incheck(self):
		if self.whiteToMove:
			return self.underattack(self.whiteking[0], self.whiteking[1])
		else:
			return self.underattack(self.blackking[0], self.blackking[1])

	def underattack(self, row, col):
		self.whiteToMove = not self.whiteToMove
		opponentmoves = self.getallmoves()
		self.whiteToMove = not self.whiteToMove
		for move in opponentmoves:
			if move.endrow == row and move.endcol == col:
				return True
			
		return False


					
	def getvalidmoves(self):
		temp = self.empassantpos
		moves = self.getallmoves()
		tempcastle = CaslteRights(self.CurrCastlerights.wks,self.CurrCastlerights.bks, 
			self.CurrCastlerights.wqs,self.CurrCastlerights.bqs) #copy current castle rights


		if self.whiteToMove:
			self.getcaslterights(self.whiteking[0], self.whiteking[1], moves)
		else:
			self.getcaslterights(self.blackking[0], self.blackking[1], moves)

		for i in range(len(moves)-1, -1,-1):
			self.makemove(moves[i])

			self.whiteToMove = not self.whiteToMove # make movesswitchs the player 
			if self.incheck():
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove #swap back
			self.redo() #cancel out the makemove

		if len(moves) == 0:
			if self.incheck():
				self.checkmate = True 
			else:
				self.stalemate = True
		else:
			#this is incase you undo a move
			self.checkmate = False
			self.stalemate= False


		self.empassantpos = temp
		self.CurrCastlerights = tempcastle

		return moves


	def pawnmoves(self, row, col, moves):
		#white moves

		if self.whiteToMove: 
			if self.board[row-1][col] == None:  #move up one
				moves.append(Move((row, col),(row-1, col),self.board))
				if row == 6 and self.board[row-2][col] == None: #move up 2
					moves.append(Move((row, col),(row-2, col),self.board))
			if col-1 >= 0:
				tile = self.board[row-1][col-1]
				if tile != None and tile.islower():
					moves.append(Move((row, col),(row-1, col-1),self.board))
				elif (row-1, col-1) == self.empassantpos:
					moves.append(Move((row, col),(row-1, col-1),self.board, isempmove = True))

			if col+1 <= 7:
				tile = self.board[row-1][col+1]
				if tile != None and tile.islower():
					moves.append(Move((row, col),(row-1, col+1),self.board))
				elif (row-1, col+1) == self.empassantpos:
					moves.append(Move((row, col),(row-1, col+1),self.board, isempmove = True))

		else:
			if self.board[row+1][col] == None:  #move up one
				moves.append(Move((row, col),(row+1, col),self.board))
				if row == 1 and self.board[row+2][col] == None: #move up 2
					moves.append(Move((row, col),(row+2, col),self.board))
			if col-1 >= 0:
				tile = self.board[row+1][col-1]
				if tile != None and tile.isupper():
					moves.append(Move((row, col),(row+1, col-1),self.board))
				elif (row+1, col-1) == self.empassantpos:
					moves.append(Move((row, col),(row+1, col-1),self.board, isempmove = True))
			if col+1 <= 7:
				tile = self.board[row+1][col+1]
				if tile != None and tile.isupper():
					moves.append(Move((row, col),(row+1, col+1),self.board))
				elif (row+1, col+1) == self.empassantpos:
					moves.append(Move((row, col),(row+1, col+1),self.board, isempmove= True))
			

	def slidingmoves(self,row,col,moves,start, end):
		directions = [(-1,0), (0,-1), (1,0), (0,1), (-1,-1) ,(-1,1), (1,-1), (1,1)]
		span = directions[start:end]
		#print(span)
		for d in span:
			for i in range(1,8):
				endrow = row + d[0] * i
				endcol = col + d[1] * i
				if 0 <= endrow < 8 and 0 <=endcol < 8:
					piece = self.board[endrow][endcol]
					if piece == None:
						moves.append(Move((row, col),(endrow, endcol),self.board))
					elif piece.isupper() and not self.whiteToMove:
						#then its a white peie and its not whites turn so capture
						moves.append(Move((row, col),(endrow, endcol),self.board))
						break
					elif piece.islower() and self.whiteToMove:
						moves.append(Move((row, col),(endrow, endcol),self.board))
						break
						#then is a black peice and its no blacks turn so white captures blacks peice
					else:
						break
				else:
					break

	def rookmoves(self,row,col, moves):
		#print("ROOK CALLED")
		self.slidingmoves(row,col,moves,0, 4)
		
	def bishupmoves(self,row,col, moves):
		self.slidingmoves(row,col,moves,4, 8)

	def queenmoves(self,row,col, moves):
		self.slidingmoves(row,col,moves,0, 8)

	def knightmoves(self,row,col, moves):
		span = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2) ,(1,2), (2,-1), (2,1)]
		for i in span:
			endrow = row + i[0] 
			endcol = col + i[1]  
			if 0 <= endrow < 8 and 0 <=endcol < 8:
				piece = self.board[endrow][endcol]
				if piece == None:
					moves.append(Move((row, col),(endrow, endcol),self.board))
				elif piece.isupper() and not self.whiteToMove:
					#then its a white peie and its not whites turn so capture
					moves.append(Move((row, col),(endrow, endcol),self.board))
				elif piece.islower() and self.whiteToMove:
					moves.append(Move((row, col),(endrow, endcol),self.board))

	def kingmoves(self,row,col, moves):
		span = [(-1,0), (0,-1), (1,0), (0,1), (-1,-1) ,(-1,1), (1,-1), (1,1)]
		color= 'w' if self.whiteToMove else 'b'
		for i in span: 
			endrow = row + i[0]  #span[i][0]
			endcol = col + i[1]
			if 0 <= endrow < 8 and 0 <=endcol < 8:
				piece = self.board[endrow][endcol]
				if piece == None:
					moves.append(Move((row, col),(endrow, endcol),self.board))
				elif piece.isupper() and not self.whiteToMove:
					#then its a white peie and its not whites turn so capture
					moves.append(Move((row, col),(endrow, endcol),self.board))
				elif piece.islower() and self.whiteToMove:
					moves.append(Move((row, col),(endrow, endcol),self.board))

		

	def getcaslterights(self, row, col, moves):
		if self.underattack(row, col):
			return 
		if (self.whiteToMove and self.CurrCastlerights.wks) or (not self.whiteToMove and self.CurrCastlerights.bks):
			self.getkingsidemoves(row, col, moves)
		if (self.whiteToMove and self.CurrCastlerights.wqs) or (not self.whiteToMove and self.CurrCastlerights.bqs):
			self.getqueensidemoves(row, col, moves)


	def getkingsidemoves(self, row, col, moves):
		if self.board[row][col+1] == None and self.board[row][col+2] == None:
			if not self.underattack(row, col+1) and not self.underattack(row, col+2):
				moves.append(Move((row, col),(row, col+2),self.board, iscasltmove=True))

	def getqueensidemoves(self, row, col, moves):
		if self.board[row][col-1] == None and self.board[row][col-2] == None and self.board[row][col-3] == None:
			if not self.underattack(row, col-1) and not self.underattack(row, col-2):
				moves.append(Move((row, col),(row, col-2),self.board, iscasltmove=True))

	def fen(self):


		row = 0
		count = 0
		string = ""
		
		for rows in self.board:
			for piece in rows:
				if piece == None:
					count+=1
				else:
					if count != 0:
						string = string + str(count) + piece 
						count = 0
					else:
						string = string + piece 
			row +=1
			if count != 0:
				string = string + str(count) + "/"
				count = 0
			else:
				string = string + "/"
		print (string)

		"""
		for item in self.board:
			#print(item)

			for piece in item:
				#print(piece)
				if piece == None:
					count+=1
				else:
					if count != 0:
						sec = sec + str(count) + piece 
						count = 0
					else:
						sec = sec + piece 
			row +=1
			

			if count == 8:
				string = str(count) + "/" + string 
				count = 0
			else:
				
					
				if count != 0:
					# werid pugs 
					string = "/" + string
					string = str(count) + string
					string = sec + string 
					
					
					
				else:
					#print("here3")
					string = sec + "/" + string 
				sec = ""
				count = 0
			
		string = string[:-1]
		"""
		#string = string[:-1]
		space = False
		if self.whiteToMove == True:
			string = string + " " + "w "
		else:
		    string = string + " " + "b "  
		if self.CurrCastlerights.wks == True:
			string = string +  'K'
		if self.CurrCastlerights.wqs == True:
			string = string +  'Q'
		if (self.CurrCastlerights.wks == False) and (self.CurrCastlerights.wks == False):
			string = string +  '- '
		



		if self.CurrCastlerights.bks == True:
			string = string +  'k'
		if self.CurrCastlerights.bqs == True:
			string = string +  'q'
		if (self.CurrCastlerights.bks == False) and (self.CurrCastlerights.bks == False):
				string = string +  '-'
		


		string = string + " 0 1"
		#print(string)
		return string

class CaslteRights():
	def __init__(self, wks, bks, wqs, bqs):
		self.wks = wks
		self.bks = bks
		self.wqs = wqs
		self.bqs = bqs

class Move():
	#files = {0:'a',1:'b',2:'c',3:'d',5:'e',6:'f',7:'g', 8:'h'}
	def __init__(self, start, end, board, isempmove = False, iscasltmove = False):
		self.startrow = start[0]
		self.startcol = start[1]
		self.endrow = end[0]
		self.endcol = end[1]
		self.piecemoved = board[self.startrow][self.startcol]
		self.peicecaptured = board[self.endrow][self.endcol]
		self.ID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol	


		#clean this code up
		self.promotion = False
		if self.piecemoved == 'P' and self.endrow ==0:
			self.promotion = True 
		if self.piecemoved == 'p' and self.endrow ==7:
			self.promotion = True 

		#probs needs the board
		self.isempmove = isempmove
		if self.isempmove:
			self.peicecaptured = 'p' if self.piecemoved == 'P' else 'P'

		#casltemove
		self.iscasltmove = iscasltmove
		"""
		if (self.piecemoved == 'p' or self.piecemoved == 'P') and (self.endrow, self.endcol) == empos:
			self.isempmove = True;
		"""
	def __eq__ (self, other):
		if isinstance(other, Move):
			return self.ID == other.ID
		return False

	def getnotation(self):
		files = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g', 7:'h'}
		ranks = {0:8,1:7,2:6,3:5,4:4,5:3,6:2, 7:1}
		return str(files[self.startcol]) + str(ranks[self.startrow]) + str(files[self.endcol]) + str(ranks[self.endrow])




	

	

	




