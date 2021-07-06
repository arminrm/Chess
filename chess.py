from math import floor
import arcade
import os, os.path

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
SCREEN_TITLE = "Starting Template"

names = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
pieces = []
board = [[], [], [], [], [], [], [] ,[]]

x_positions = []
y_positions = []

valid_choice = False  
index = None

turn = "WHITE"
original_position = []  #include in class
original_piece = None
found = None

king = None
start = False
check_piece = None
king_moved = {"WHITE": 0, "BLACK": 0}
rook_moved = {"WHITE": 0, "BLACK": 0}
castle = False

pawn_straight = None

img_paths = [f"Project\\images\\{piece}" for piece in os.listdir("C:\\Users\\armin\\Downloads\\Project\\Project\\images")]
piece_imgs = {image: arcade.load_texture(image) for image in img_paths}

def assignment():

    global original_piece

    board[int(floor(original_position[1] / 100))][int(floor(original_position[0] / 100))] = None
    original_piece = board[int(floor(pieces[index].y / 100))][int(floor(pieces[index].x / 100))]
    board[int(floor(pieces[index].y / 100))][int(floor(pieces[index].x / 100))] = pieces[index]

def reassignment():  #this could be cut down if included as a condition

    global original_piece

    board[int(floor(pieces[index].y / 100))][int(floor(pieces[index].x / 100))] = original_piece
    [pieces[index].x, pieces[index].y] = original_position
    board[int(floor(original_position[1] / 100))][int(floor(original_position[0] / 100))] = pieces[index]

def rook_or_queen(temp, context, i, j):

    global check_piece

    if temp != None:
        if (temp.piece == "Rook" or temp.piece == "Queen") and temp.colour != turn:
            if context == "valid":
                reassignment()
            elif context == "check":
                check_piece = temp
            elif context == "checkmate":
                board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))] = original_piece
                board[int(floor(king.y / 100))][int(floor(king.x / 100))] = king
            return True

def bishop_or_queen(temp, context, i, j):

    global check_piece, king_moved

    if temp != None:
        if (temp.piece == "Bishop" or temp.piece == "Queen") and temp.colour != turn:
            if context == "valid":
                reassignment()
            elif context == "check":
                check_piece = temp
            elif context == "checkmate":
                board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))] = original_piece
                board[int(floor(king.y / 100))][int(floor(king.x / 100))] = king
            return True

def pawn_check(temp, context, i, j):

    global check_piece

    if temp != None and temp.piece == "Pawn" and temp.colour != turn:
        if abs(king.x + i - temp.x) == 100 and abs(king.y + j - temp.y) == 100:
            if context == "valid":
                reassignment()
            elif context == "check":
                check_piece = temp
            elif context == "checkmate":
                board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))] = original_piece
                board[int(floor(king.y / 100))][int(floor(king.x / 100))] = king
            return True
    
def move_rook(): 
    for piece in pieces:
        if piece.piece == "Rook" and piece.colour == turn and piece.x == 750:
            board[int(floor(piece.y / 100))][int(floor(piece.x / 100))] = None
            board[int(floor(pieces[index].y/ 100))][5] = piece
            [piece.x, piece.y] = [550, pieces[index].y]

def moved_piece():

    global castle

    if pieces[index].piece == "King":
        king_moved[turn] = 1
    elif pieces[index].piece == "Rook":
        rook_moved[turn] = 1

    if castle:
        move_rook()

def attack():  #might have to include assignment function

    global castle, pawn_straight
    for i, piece in enumerate(pieces): 
        if i != index and piece.x == pieces[index].x and piece.y == pieces[index].y:
            if piece.colour == pieces[index].colour or piece.piece == "King":
                reassignment()
                return False
            else:
                moved_piece()  #what if you are attacking a piece....
                if pieces[index].piece == "Pawn":
                    if pawn_straight:
                        reassignment()
                        return False
                pieces.pop(i)
                return True

    moved_piece()
    return True

def knight_check(x, y):  #could I shorten this??

    x = int(floor(x / 100))
    y = int(floor(y / 100))

    if x + 1 <= 7:
        if y + 2 <= 7:
            if board[y + 2][x + 1] != None:
                if board[y + 2][x + 1].piece == "Knight" and board[y + 2][x + 1].colour != turn:
                    #print("10")
                    return True
        if y - 2 >= 0:
            if board[y - 2][x + 1] != None:
                if board[y - 2][x + 1].piece == "Knight" and board[y - 2][x + 1].colour != turn:
                    #print("20")
                    return True

    if x - 1 >= 0:   
        if y + 2 <= 7:
            if board[y + 2][x - 1] != None:
                if board[y + 2][x - 1].piece == "Knight" and board[y + 2][x - 1].colour != turn:
                    #print("30")
                    return True
        if y - 2 >= 0:
            if board[y - 2][x - 1] != None:
                if board[y - 2][x - 1].piece == "Knight" and board[y - 2][x - 1].colour != turn:
                    #print("40")
                    return True
    
    if x + 2 <= 7:
        if y + 1 <= 7:
            if board[y + 1][x + 2] != None:
                if board[y + 1][x + 2].piece == "Knight" and board[y + 1][x + 2].colour != turn:
                    #print("50")
                    return True
        if y - 1 >= 0:
            if board[y - 1][x + 2] != None:
                if board[y - 1][x + 2].piece == "Knight" and board[y - 1][x + 2].colour != turn:
                    return True

    if x - 2 >= 0:
        if y + 1 <= 7:
            if board[y + 1][x - 2] != None:
                if board[y + 1][x - 2].piece == "Knight" and board[y + 1][x - 2].colour != turn:
                    return True
        if y - 1 >= 0:
            if board[y - 1][x - 2] != None:
                if board[y - 1][x - 2].piece == "Knight" and board[y - 1][x - 2].colour != turn:
                    #print(board[y - 1][x - 2].piece, board[y - 1][x - 2].colour)
                    return True
            
    return False
  
def direction_check(start_x, start_y, end_x, end_y, x_sign, y_sign):
    if y_sign != 0 and x_sign == 0:
        for row in range(start_y + (100 * y_sign), end_y, y_sign * 100):
            if board[int(floor(row / 100))][int(floor(start_x / 100))] != None:
                return board[int(floor(row / 100))][int(floor(start_x / 100))]
        return None
    elif x_sign != 0 and y_sign == 0:
        for col in range(start_x + (100 * x_sign), end_x, x_sign * 100):
            if board[int(floor(start_y/ 100))][int(floor(col / 100))] != None:
                return board[int(floor(start_y/ 100))][int(floor(col / 100))]
        return None
    else:
        for i in range(100, abs(end_x - start_x), 100):
            if start_y + (y_sign * i) in range(50, 751) and start_x + (x_sign * i) in range(50, 751): #use "in range"
                if board[int(floor((start_y + y_sign * i) / 100))][int(floor((start_x + x_sign * i) / 100))] != None:
                    return board[int(floor((start_y + y_sign * i) / 100))][int(floor((start_x + x_sign * i) / 100))]
        return None

    
#arraysname (row * total columns) + coloumn
def collision_detection(original_x, original_y, end_x, end_y, purpose):   #backwards....

    if pieces[index].piece != "Knight":
        if original_y > end_y:
            y = -1
        elif original_y < end_y:
            y = 1
        else:
            y = 0

        if original_x > end_x:
            x = -1
        elif original_x < end_x:
            x = 1
        else:
            x = 0

        if direction_check(original_x, original_y, end_x, end_y, x, y) != None:
            if purpose == "valid":
                [pieces[index].x, pieces[index].y] = original_position
            return False

    if purpose == "valid":
        return attack()
    else:
        if pawn_straight and board[int(floor(end_y / 100))][int(floor(end_x / 100))] != None:
            return False
        return True

def check(i, j, purpose):

    global king, original_piece

    if purpose == "checkmate":
        board[int(floor(king.y / 100))][int(floor(king.x / 100))] = None
        original_piece = board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))]
        board[int(floor((king.y + j) / 100))][int(floor((king.x + i) / 100))] = king

    temp = direction_check(king.x + i, king.y + j, 49, king.y + j, -1, 0) #it is because it checks this first lol
    if rook_or_queen(temp, purpose, i, j):
        return False
            
    temp = direction_check(king.x + i, king.y + j, 751, king.y + j, 1, 0)
    if rook_or_queen(temp, purpose, i, j):
        return False
            
    temp = direction_check(king.x + i, king.y + j, king.x + i, 751, 0, 1)
    if rook_or_queen(temp, purpose,i, j):
        return False

    temp = direction_check(king.x + i, king.y + j, king.x + i, 49, 0, -1)
    if rook_or_queen(temp, purpose, i, j):
        return False

    temp = direction_check(king.x + i, king.y + j, 751, 751, 1, 1)
    if turn == "WHITE" and pawn_check(temp, purpose, i, j):
        return False
    if bishop_or_queen(temp, purpose, i, j):
        return False

    temp = direction_check(king.x + i, king.y + j, 49, 751, -1, 1)
    #if temp != None:
        #print(temp.piece, temp.x, temp.y)
    if turn == "WHITE" and pawn_check(temp, purpose, i, j):
        return False
    if bishop_or_queen(temp, purpose, i, j):
        return False

    temp = direction_check(king.x + i, king.y + j, 751, 49, 1, -1)
    #if temp != None:
        #print(temp.piece, temp.x, temp.y)
    if turn == "BLACK" and pawn_check(temp, purpose, i, j):
        return False
    if bishop_or_queen(temp, purpose, i, j):
        return False

    temp = direction_check(king.x + i, king.y + j, 49, 49, -1, -1)
    if temp != None:
        print(temp.piece, temp.x, temp.y, turn, temp.colour)
    if turn == "BLACK" and pawn_check(temp, purpose, i, j):
        return False
    if bishop_or_queen(temp, purpose, i, j):
        return False

    if knight_check(king.x + i, king.y + j):
        if purpose == "valid":
            reassignment()
        elif purpose == "checkmate":
            board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))] = original_piece
            board[int(floor(king.y / 100))][int(floor(king.x / 100))] = king
        return False

    if purpose == "checkmate":
        board[int(floor((king.y + j)/ 100))][int(floor((king.x + i)/ 100))] = original_piece
        board[int(floor(king.y / 100))][int(floor(king.x / 100))] = king
    return True

def checkmate():

    global king, check_piece

    x = int(floor(king.x / 100))
    y = int(floor(king.y / 100))

    if check(0, 0, "check") == False:
        if x - 1 >= 0:    
            if (board[y][x - 1] != None and board[y][x - 1].colour != turn) or board[y][x - 1] == None:
                if check(-100, 0, "checkmate"):
                    print(1)
                    return False 

            if y - 1 >= 0: 
                if (board[y - 1][x] != None and board[y - 1][x].colour != turn) or board[y - 1][x] == None:
                    if check(0, -100, "checkmate"):
                        print(2)
                        return False

                if (board[y - 1][x - 1] != None and board[y - 1][x - 1].colour != turn) or board[y - 1][x - 1] == None:
                    if check(-100, - 100, "checkmate"):
                        print(3)
                        return False

            if y + 1 <= 7:
                if (board[y + 1][x] != None and board[y + 1][x].colour != turn) or board[y + 1][x] == None:
                    if check(0, 100, "checkmate"):
                        print(4)
                        return False

                if (board[y + 1][x - 1] != None and board[y + 1][x - 1].colour != turn) or board[y + 1][x - 1] == None:
                    if check(-100, 100, "checkmate"):
                        return False

        if x + 1 <= 7:
            if (board[y][x + 1] != None and board[y][x + 1].colour != turn) or board[y][x + 1] == None:
                if check(100, 0, "checkmate"):
                    print(5)
                    return False

            if y - 1 >= 0:
                if (board[y - 1][x] != None and board[y - 1][x].colour != turn) or board[y - 1][x] == None:
                    if check(0, -100, "checkmate"):
                        print(6)
                        return False

                if (board[y - 1][x + 1] != None and board[y - 1][x + 1].colour != turn) or board[y - 1][x + 1] == None:
                    if check(100, -100,"checkmate"):
                        print(7)
                        return False

            if y + 1 <= 7:
                if (board[y + 1][x] != None and board[y + 1][x].colour != turn) or board[y + 1][x] == None:
                    if check(0, 100, "checkmate"):
                        print(8)
                        return False 

                if (board[y + 1][x + 1] != None and board[y + 1][x + 1] .colour != turn) or board[y + 1][x + 1]  == None:
                    if check(100, 100, "checkmate"):
                        print(9)
                        return False

        if king.y > check_piece.y:
            y = -1
        elif king.y < check_piece.y:
            y = 1
        else:
            y = 0

        if king.x > check_piece.x:
            x = -1
        elif king.x < check_piece.x:
            x = 1
        else:
            x = 0

        for piece in pieces:
            if piece.piece != "King" and  piece.colour == turn:
                if y != 0 and x == 0:
                   for row in range(king.y + (100 * y), check_piece.y + y, y * 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, king.x, row):
                            if collision_detection(piece.x, piece.y, king.x, row, "checkmate"):
                                print(piece.piece, piece.colour, piece.x, piece.y, 1, row) 
                                return False    
                elif x != 0 and y == 0:
                    for col in range(king.x + (100 * x), check_piece.x + x, x * 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, col, king.y):
                            if collision_detection(piece.x, piece.y, col, king.y, "checkmate"):
                                print(piece.piece, piece.colour, piece.x, piece.y, 2, col)
                                return False
                else:
                    for i in range(100, abs(check_piece.x - king.x) + x, 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, king.x + x * i, king.y + y * i):
                            if collision_detection(piece.x, piece.y, king.x + x * i, king.y + y * i, "checkmate"):
                                print(piece.piece, piece.colour, piece.x, piece.y, 3, king.x + x * i, king.y + y * i) 
                                return False
        return True
    else:
        return False

def check_move(piece, colour, original_x, original_y, new_x, new_y):  #moves through king...

    global pieces, index, original_position, castle, pawn_straight

    if piece == "Rook":
        if new_x == original_x or new_y == original_y:
            return True
        else:
            return False
    elif piece == "Pawn":   #I could cut this whole section down to one function.....
        if colour == "WHITE":
            if [new_x, new_y] == [original_x, original_y + 100]:
                pawn_straight = True
                return True
            elif [new_x, new_y] == [original_x, original_y + 200]:
                if original_y == 150:
                    pawn_straight = True
                    return True 
            elif [new_x, new_y] == [original_x + 100, original_y + 100] or [new_x, new_y] == [original_x - 100, original_y + 100]:
                if board[int(floor(new_y/100))][int(floor(new_x/100))] != None and board[int(floor(new_y/100))][int(floor(new_x/100))].colour != turn:
                    pawn_straight = False
                    return True
            return False
        elif colour == "BLACK":
            if [new_x, new_y] == [original_x, original_y - 100]:
                pawn_straight = True
                return True
            elif [new_x, new_y] == [original_x, original_y - 200]:
                if original_y == 650:
                    pawn_straight = True
                    return True 
            elif [new_x, new_y] == [original_x + 100, original_y - 100] or [new_x, new_y] == [original_x - 100, original_y - 100]:
                if board[int(floor(new_y/100))][int(floor(new_x/100))] != None and board[int(floor(new_y/100))][int(floor(new_x/100))].colour != turn:
                    pawn_straight = False
                    return True
            return False
    elif piece == "Bishop":
        if new_x != original_x and new_y != original_y and abs(new_y - original_y) == abs(new_x - original_x):
            return True
        else:
            return False 
    elif piece == "Queen": 
        if new_x == original_x or new_y == original_y or abs(new_y - original_y) == abs(new_x - original_x):
            return True
        else:
            return False
    elif piece == "Knight":
        if (abs(new_x - original_x) == 100 and abs(new_y - original_y) == 200) or (abs(new_x - original_x) == 200 and abs(new_y - original_y) == 100):
            return True
        else:
            return False
    elif piece == "King":  #add castle condition here...
        if (abs(new_x - original_x) == 100 and new_y == original_y) or (abs(new_y - original_y) == 100 and new_x == original_x) or (abs(new_x - original_x) == 100 and abs(new_y - original_y) == 100):
            return True
        elif king_moved[turn] == 0 and rook_moved[turn] == 0:
            if new_x == original_x + 200 and new_y == original_y:
                castle = True
                return True 
        else:
            return False
                
def valid_move():  #moves through king...  -- original

    global pieces, index, original_position, king

    for piece in pieces:
        if piece.piece == "King" and piece.colour == turn:
            king = piece
            break

    if check_move(pieces[index].piece, pieces[index].colour, original_position[0], original_position[1], pieces[index].x, pieces[index].y):
            assignment()
            if check(0, 0, "valid") == False:
                return False
            else:
                return collision_detection(original_position[0], original_position[1], pieces[index].x, pieces[index].y, "valid")
    else:
        [pieces[index].x, pieces[index].y] = original_position
        return False

class chess_piece():   #camel-case, capitalized

    def __init__(self, piece, colour, x, y):
        self.image = None
        self.piece = piece
        self.colour = colour
        self.x = x
        self.y = y
        pieces.append(self)
    
    @classmethod
    def make_pieces(cls):
        for x, name in enumerate(names):
         board[0].append(chess_piece(name, "WHITE", (100 * x) + 50, 50))
         board[7].append(chess_piece(name, "BLACK", (100 * x) + 50, 750))
         board[1].append(chess_piece("Pawn", "WHITE", (100 * x) + 50, 150))
         board[6].append(chess_piece("Pawn", "BLACK", (100 * x) + 50, 650))

         for piece in pieces:
             piece.image = piece_imgs[f"Project\\images\\{piece.colour}_{piece.piece}.png"]

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):

        for row in range(2, 6):
            for col in range(8):
                board[row].append(None)
        
        chess_piece.make_pieces()

    def on_draw(self):

        arcade.start_render()
        #Print chess-board
        z = 0
        for y in range(0, 701, 100):
            y_positions.append(y + 50)
            for x in range(0 + z, 701 + z, 100):
                if x % 200 == 0:
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.AUBURN)
                else:
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.WHITE)
                if y == 0:
                    x_positions.append(x + 50)
            z += 100

        #print pieces
        for piece in pieces:
            if piece.colour == 'WHITE':
                arcade.draw_texture_rectangle(piece.x, piece.y, 70, 70, piece.image)
            elif piece.colour == 'BLACK':
                arcade.draw_texture_rectangle(piece.x, piece.y, 70, 70, piece.image)

    def on_mouse_motion(self, x, y, delta_x, delta_y):

        global pieces, index, valid_choice

        if valid_choice == True and start != True:
            pieces[index].x = x
            pieces[index].y = y

    def on_mouse_press(self, x, y, button, key_modifiers):

        global valid_choice, index, original_position

        if start != True:
            original_position = []
            for i, piece in enumerate(pieces):
                if x in range(piece.x - 50, piece.x + 50) and y in range(piece.y - 50, piece.y + 50):
                    if piece.colour == turn:
                        original_position = [piece.x, piece.y]
                        valid_choice = True
                        index = i
            
    def on_mouse_release(self, x, y, button, key_modifiers):
        
        global pieces, index, valid_choice, turn, found, start, king, castle, pawn_straight

        found = False
        
        if valid_choice == True and start != True:
            for row in range(8):
                if y in range(y_positions[row] - 50, y_positions[row] + 50):
                    for col in range(8):
                        if x in range(x_positions[col] - 50, x_positions[col] + 50):
                            pieces[index].x = x_positions[col]
                            pieces[index].y = y_positions[row]
                            found = True
                            break

                    if found:
                        break
  
            if [pieces[index].x, pieces[index].y] != original_position and valid_move():

                if turn == "WHITE":
                    turn = "BLACK"
                else:
                    turn = "WHITE"

                for piece in pieces:
                    if piece.piece == "King" and piece.colour == turn:
                        king = piece
                        break

                pawn_straight = False
                start = checkmate()
                print(start)

        valid_choice = False
        castle = False

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
