from math import floor
import arcade
#changes to the check function (assignment and final portion); changes to valid move function

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

king = []
start = False
check_piece = None

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

def rook_or_queen(temp, i):

    global check_piece

    if temp != None:
        if (temp.piece == "Rook" or temp.piece == "Queen") and temp.colour != turn:
            if i == "valid":
                reassignment()
            elif i == "check":
                check_piece = temp
            return True

def bishop_or_queen(temp, i):

    global check_piece

    if temp != None:
        if (temp.piece == "Bishop" or temp.piece == "Queen") and temp.colour != turn:
            if i == "valid":
                reassignment()
            elif i == "check":
                check_piece = temp
            return True


def attack():  #might have to include assignment function
    for i, piece in enumerate(pieces): 
        if i != index and piece.x == pieces[index].x and piece.y == pieces[index].y:
            if piece.colour == pieces[index].colour or piece.piece == "King":
                reassignment()
                return False
            else:
                pieces.pop(i)
                return True

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
            else:
                return False

    if purpose == "valid":
        return attack()
    else:
        return True

def check(i, j, purpose):

    global king

    temp = direction_check(king[0] + i, king[1] + j, 49, king[1] + j, -1, 0)
    if rook_or_queen(temp, purpose):
        return False
            
    temp = direction_check(king[0] + i, king[1] + j, 751, king[1] + j, 1, 0)
    if rook_or_queen(temp, purpose):
        return False
            
    temp = direction_check(king[0] + i, king[1] + j, king[0] + i, 751, 0, 1)
    if rook_or_queen(temp, purpose):
        return False

    temp = direction_check(king[0] + i, king[1] + j, king[0] + i, 49, 0, -1)
    if rook_or_queen(temp, purpose):
        return False

    temp = direction_check(king[0] + i, king[1] + j, 751, 751, 1, 1)
    if bishop_or_queen(temp, purpose):
        return False

    temp = direction_check(king[0]+ i, king[1] + j, 49, 751, -1, 1)
    if bishop_or_queen(temp, purpose):
        return False

    temp = direction_check(king[0] + i, king[1] + j, 751, 49, 1, -1)
    if bishop_or_queen(temp, purpose):
        return False

    temp = direction_check(king[0] + i, king[1] + j, 49, 49, -1, -1)
    if bishop_or_queen(temp, purpose):
        return False

    if knight_check(king[0] + i, king[1] + j):
        if purpose == "valid":
            reassignment()
        return False

    return True

def checkmate():

    global king, check_piece

    x = int(floor(king[0]/ 100))
    y = int(floor(king[1] / 100))

    check(0, 0, "check")

    if check(0, 0, "check") == False:
        if x - 1 >= 0:    
            if (board[y][x - 1] != None and board[y][x - 1].colour != turn) or board[y][x - 1] == None:
                if check(-100, 0, "checkmate"):
                    return False #no checkmate

            if y - 1 >= 0: 
                if (board[y - 1][x] != None and board[y - 1][x].colour != turn) or board[y - 1][x] == None:
                    if check(0, -100, "checkmate"):
                        return False #no checkmate

                if (board[y - 1][x - 1] != None and board[y - 1][x - 1].colour != turn) or board[y - 1][x - 1] == None:
                    if check(-100, - 100, "checkmate"):
                        return False #no checkmate

            if y + 1 <= 7:
                if (board[y + 1][x] != None and board[y + 1][x].colour != turn) or board[y + 1][x] == None:
                    if check(0, 100, "checkmate"):
                        return False #no checkmate

                if (board[y + 1][x - 1] != None and board[y + 1][x - 1].colour != turn) or board[y + 1][x - 1] == None:
                    if check(-100, 100, "checkmate"):
                        return False #no checkmate

        if x + 1 <= 7:
            if (board[y][x + 1] != None and board[y][x + 1].colour != turn) or board[y][x + 1] == None:
                if check(100, 0, "checkmate"):
                    return False #no checkmate

            if y - 1 >= 0:
                if (board[y - 1][x] != None and board[y - 1][x].colour != turn) or board[y - 1][x] == None:
                    if check(0, -100, "checkmate"):
                        return False #no checkmate

                if (board[y - 1][x + 1] != None and board[y - 1][x + 1].colour != turn) or board[y - 1][x + 1] == None:
                    if check(100, -100,"checkmate"):
                        return False #no checkmate

            if y + 1 <= 7:
                if (board[y + 1][x] != None and board[y + 1][x].colour != turn) or board[y + 1][x] == None:
                    if check(0, 100, "checkmate"):
                        return False #no checkmate

                if (board[y + 1][x + 1] != None and board[y + 1][x + 1] .colour != turn) or board[y + 1][x + 1]  == None:
                    if check(100, 100, "checkmate"):
                        return False #no checkmate

        if king[1] > check_piece.y:
            y = -1
        elif king[1] < check_piece.y:
            y = 1
        else:
            y = 0

        if king[0] > check_piece.x:
            x = -1
        elif king[0] < check_piece.x:
            x = 1
        else:
            x = 0

        for piece in pieces:
            if piece.piece != "King" and  piece.colour == turn:
                if y != 0 and x == 0:
                   for row in range(king[1] + (100 * y), check_piece.y + y, y * 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, king[0], row):
                            if collision_detection(piece.x, piece.y, king[0], row, "checkmate"):
                                return False          
                elif x != 0 and y == 0:
                    for col in range(king[0] + (100 * x), check_piece.x + x, x * 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, col, king[1]):
                            if collision_detection(piece.x, piece.y, col, king[1], "checkmate"):
                                return False
                else:
                    for i in range(100, abs(check_piece.x - king[0]) + x, 100):
                        if check_move(piece.piece, piece.colour, piece.x, piece.y, king[0] + x * i, king[1] + y * i):
                            if collision_detection(piece.x, piece.y, king[0] + x * i, king[1] + y * i, "checkmate"):
                                return False
        return True
    else:
        return False

def check_move(piece, colour, original_x, original_y, new_x, new_y):  #moves through king...

    global pieces, index, original_position

    if piece == "Rook":
        if new_x == original_x or new_y == original_y:
            return True
        else:
            return False
    elif piece == "Pawn":   #assumption potential error...
        if ([new_x, new_y] == [original_x, original_y + 100] and colour == "WHITE") or ([new_x, new_y] == [original_x, original_y - 100] and colour == "BLACK"):
            return True
        else:
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
    elif piece == "King":  #change condition...
        if (abs(new_x - original_x) == 100 and new_y == original_y) or (abs(new_y - original_y) == 100 and new_x == original_x) or (abs(new_x - original_x) == 100 and abs(new_y - original_y) == 100):
            return True
        else:
            return False
    
def valid_move():  #moves through king...  -- original

    global pieces, index, original_position, king

    for piece in pieces:
        if piece.piece == "King" and piece.colour == turn:
            king = [piece.x, piece.y]
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
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.BLACK)
                else:
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.WHITE)
                if y == 0:
                    x_positions.append(x + 50)
            z += 100

        #print pieces
        for piece in pieces:
            if piece.colour == 'WHITE':
                arcade.draw_text(piece.piece, piece.x, piece.y, arcade.color.BLUE)
            elif piece.colour == 'BLACK':
                arcade.draw_text(piece.piece, piece.x, piece.y, arcade.color.RED)

    #def on_update(self, delta_time):


    #def on_key_press(self, key, key_modifiers):
        
        #pass

    #def on_key_release(self, key, key_modifiers):


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
        
        global pieces, index, valid_choice, turn, found, start, king

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
                        king = [piece.x, piece.y]
                        break

                start = checkmate()

        valid_choice = False

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
