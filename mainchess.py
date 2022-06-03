import pygame as p
from Engine import *
from Ai import *

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQAURE_SIZE = WIDTH//COLS

LOGCOLOR = (143,188,143) #seagreen wood(202,164,114) olive (107,142,35)

BLACK = (166,123,91)   #revert bacl to black (0)
WHITE = (247,228,215)  #revert to white at (255,255,255)

LOGWIDTH = 400
LOGHEIGHT = HEIGHT

IMAGES = {}
FPS = 15
p.font.init()
test = "7n/2p2R1p/r3qP2/Nk6/1p5Q/3P2n1/1p6/3K3B w - - 0 1"
startFEN = test
startFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"
FONT = p.font.Font(None, 18)
def LoadImages():
	names = ['bd', 'bl', 'kd', 'kl', 'nd', 'nl', 'pd', 'pl', 'qd', 'ql', 'rd', 'rl']
	ID = ['b', 'B', 'k', 'K', 'n', 'N', 'p', 'P', 'q', 'Q', 'r', 'R']

	itr = 0
	for itr in range(12):
		IMAGES[ID[itr]] = p.transform.scale(p.image.load("Pieces/Chess_" + names[itr] + "t60.png"), (SQAURE_SIZE,SQAURE_SIZE))
	#access images using their ID
		itr+=1



def drawBoard(screen):
	"""
	draws the board tiles
	"""

	colors = [p.Color(WHITE), p.Color(BLACK)] #you can change the color of the board here
	for row in range(ROWS):
		for col in range(COLS):
			color = colors[(col+row)%2]
			p.draw.rect(screen,color,p.Rect(col*SQAURE_SIZE, row*SQAURE_SIZE, SQAURE_SIZE,SQAURE_SIZE))

def drawPeices(screen, board):
	"""
	draws peies on the boatrd
	"""
	for row in range(ROWS):
		for col in range(COLS):
			piece = board[row][col]
			if piece != None: 
				screen.blit(IMAGES[piece], p.Rect(col*SQAURE_SIZE, row*SQAURE_SIZE, SQAURE_SIZE,SQAURE_SIZE))
	
def DrawGame(screen, gs, Valid_moves, selected_sqaure, movefont):
	"""
	This fucntion will draw all the graphics
	"""
	drawBoard(screen)
	Highlight(screen, gs, Valid_moves, selected_sqaure)
	drawPeices(screen, gs.board)
	drawMoveLog(screen, gs, movefont)


def drawMoveLog(screen, gs, movefont):
	movelogRect = p.Rect(WIDTH, 0, LOGWIDTH, LOGHEIGHT)
	p.draw.rect(screen, p.Color(LOGCOLOR), movelogRect)
	movelog = gs.moveLog
	movetexts = movelog
	padding = 5
	yiter = padding
	for i in range(len(movetexts)):
		text = movetexts[i].getnotation()
		textObject = movefont.render(text,True,p.Color('Black'))
		textlocation = movelogRect.move(padding, yiter)
		screen.blit(textObject, textlocation)
		yiter += textObject.get_height()



def Highlight(screen,gs, Valid_moves, selected_sqaure):
	if selected_sqaure != ():
		row, col = selected_sqaure
		piece = gs.board[row][col]
		if piece != None: 	
			s= p.Surface((SQAURE_SIZE, SQAURE_SIZE))
			s.set_alpha(150)  #transparecy value.
			s.fill(p.Color((255,233,0)))
			screen.blit(s, (col*SQAURE_SIZE, row*SQAURE_SIZE))
			s.fill(p.Color('red'))
			for move in Valid_moves:
				if move.startrow == row and move.startcol == col:
					screen.blit(s, (move.endcol*SQAURE_SIZE, move.endrow*SQAURE_SIZE))

def drawText(screen, text):
	font = p.font.SysFont("Helvitca", 32, True, False)
	textObject = font.render(text, 0,p.Color('Black'))
	textlocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2- textObject.get_height()/2)
	screen.blit(textObject, textlocation)

def drawfentext(screen, text):
	font = p.font.SysFont("Helvitca", 32, True, False)
	textObject = font.render(text, 0,p.Color('Black'))
	textlocation = p.Rect(800, 750, 400, 32)
	screen.blit(textObject, textlocation)


def Checkfen(fen):
	ID = ['B', 'b', 'K', 'k', 'N', 'n', 'P', 'p', 'Q', 'q', 'R', 'r','1','2','3','4','5','6','7','8', '-']
	count = 0
	for letter in fen:
		if letter == '/':
			count +=1
		if letter not in ID:
			return False

	if count == 7:
		return True
	return False





def main():
	p.init()
	screen = p.display.set_mode((WIDTH+ LOGWIDTH,HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	gs = Gamestate()
	gs.LoadFenString(startFEN)
	Valid_moves = gs.getvalidmoves()
	movemade = False #flag for when move is made.
	movefont = p.font.SysFont("calibri", 18, False, False)
	LoadImages()

	running = True
	selected_sqaure = () #(two tuples)
	pclicks = [] #keep track of player clicks [(), ()]

	#TEXT BOX
	input_box = p.Rect(800,700,400, 32)
	color_inactive =  p.Color(122,122,122)
	color_active = p.Color('Black') 
	color = color_inactive
	active = False
	text = ''
	gameover = False
	player_1 = True #true if human
	player_2 = False



	while running:
		human = (gs.whiteToMove and player_1) or (not gs.whiteToMove and player_2)
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False

			#KEY STUFF
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					gs.redo()
					movemade = True
				#print("SOMEONE WAS HIT")
				if active:
					if e.key == p.K_RETURN:
						try:
							print(text)
							gs.LoadFenString(text)
							Valid_moves = gs.getvalidmoves()
							text = ' '
						except:
							print("invalid string")
							

					elif e.key == p.K_BACKSPACE:
						text = text[:-1]
					else:
						text += e.unicode

			#mouse Stuff
			elif e.type == p.MOUSEBUTTONDOWN:
				if not gameover and human:
					loc = p.mouse.get_pos()
					#print(loc)
					col = loc[0]//SQAURE_SIZE
					row = loc[1]//SQAURE_SIZE 


					#TEXT BOX STUFF
					if input_box.collidepoint(e.pos):
						active = not active
						#print("here")
					else:
						active = False
						#print("ACTIVE OFF")

					color = color_active if active else color_inactive



					if selected_sqaure == (row, col) or col >= 8:
						selected_sqaure = ()
						pclicks = []
					else:
						selected_sqaure = (row, col)
						print(selected_sqaure)
						pclicks.append(selected_sqaure)

					if (len(pclicks) == 2):
						move = Move(pclicks[0], pclicks[1], gs.board)
						#print(move.getnotation())

						for i in range(len(Valid_moves)):
							if move == Valid_moves[i]:
								print(move.getnotation())
								
								gs.makemove(Valid_moves[i])
								movemade = True
								selected_sqaure = ()
								pclicks = []
								#print(gs.fen())
						if not movemade:
							pclicks =[selected_sqaure]
		#AI 
		if not gameover and not human:
			print(gs.fen())
			aimove = getstockmovefen(gs.fen())

			move = Move(aimove[0], aimove[1], gs.board)
			gs.makemove(move)
			movemade = True
			print(gs.fen())
			

		if movemade:
			
			Valid_moves = gs.getvalidmoves()
			#print("updating the moves")
			movemade = False

		DrawGame(screen, gs, Valid_moves, selected_sqaure, movefont)
		drawfentext(screen, "Enter In Fen string:")
		

		txt_surface = FONT.render(text, True, color)
		

		screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
		p.draw.rect(screen, color, input_box, 2)

		if gs.checkmate:
			gamemover = True
			if gs.whiteToMove:
				drawText(screen,"BLACK WINS CHECKMATE!")
			else:
				drawText(screen,"White WINS CHECKMATE!")

		elif gs.stalemate:
			gameover = True
			drawText(screen, "STALEMATE!")
		clock.tick(15)
		p.display.flip()



if __name__ == "__main__":
	main()