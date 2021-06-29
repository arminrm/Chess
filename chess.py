from math import floor
import arcade
#maybe file for functions....

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
found = None

def assignment():
    board[int(floor(original_position[1] / 100))][int(floor(original_position[0] / 100))] = None
    board[int(floor(pieces[index].y / 100))][int(floor(pieces[index].x / 100))] = pieces[index]

def reassignment():  #this could be cut down if included as a condition
    board[int(floor(pieces[index].y / 100))][int(floor(pieces[index].x / 100))] = None
    [pieces[index].x, pieces[index].y] = original_position
    board[int(floor(original_position[1] / 100))][int(floor(original_position[0] / 100))] = pieces[index]

def rook_or_queen(temp):
    if temp != None:
        if (temp.piece == "Rook" or temp.piece == "Queen") and temp.colour != turn:
            reassignment()
            return True

def bishop_or_queen(temp):
    if temp != None:
        if (temp.piece == "Bishop" or temp.piece == "Queen") and temp.colour != turn:
            reassignment()
            return True


def attack():  #we could cut this down by using board
    for i, piece in enumerate(pieces): 
        if i != index and piece.x == pieces[index].x and piece.y == pieces[index].y:
            if piece.colour == pieces[index].colour or piece.piece == "King":
                [pieces[index].x, pieces[index].y] = original_position
                return False
            else:
                assignment()
                pieces.pop(i)
                return True

    assignment()
    return True

def direction_check(start_x, start_y, end_x, end_y, x_sign, y_sign):
    if y_sign != 0 and x_sign == 0:
        for row in range(start_y + (100 * y_sign), end_y, y_sign * 100):
            if board[int(floor(row / 100))][int(floor(pieces[index].x / 100))] != None:
                return board[int(floor(row / 100))][int(floor(pieces[index].x/ 100))]
        return None
    elif x_sign != 0 and y_sign == 0:
        for col in range(start_x + (100 * x_sign), end_x, x_sign * 100):
            if board[int(floor(pieces[index].y/ 100))][int(floor(col / 100))] != None:
                return board[int(floor(pieces[index].y / 100))][int(floor(col / 100))]
        return None
    else:
        for i in range(100, abs(end_x - start_x), 100):
            if (start_y + (y_sign * i) >= 50 and start_y + (y_sign * i) <= 750) and (start_x + (x_sign * i) >= 50 and start_x + (x_sign * i) <= 750):
                if board[int(floor((start_y + y_sign * i) / 100))][int(floor((start_x + x_sign * i) / 100))] != None:
                    return board[int(floor((start_y + y_sign * i) / 100))][int(floor((start_x + x_sign * i) / 100))]
        return None


#arraysname (row * total columns) + coloumn
def collision_detection():   #backwards....

    if original_position[1] > pieces[index].y:
        y = -1
    elif original_position[1] < pieces[index].y:
        y = 1
    else:
        y = 0

    if original_position[0] > pieces[index].x:
        x = -1
    elif original_position[0] < pieces[index].x:
        x = 1
    else:
        x = 0

    if direction_check(original_position[0], original_position[1], pieces[index].x, pieces[index].y, x, y) != None:
        [pieces[index].x, pieces[index].y] = original_position
        return False

    return attack()

def valid_move_king():

    assignment()  #I could also put this as a condition...

    temp = direction_check(pieces[index].x, pieces[index].y, 49, pieces[index].y, -1, 0)
    if temp != None:
        print(temp.piece)
    if rook_or_queen(temp):
        return False
    
    temp = direction_check(pieces[index].x, pieces[index].y, 751, pieces[index].y, 1, 0)
    if temp != None:
        print(temp.piece)
    if rook_or_queen(temp):
        return False
    
    temp = direction_check(pieces[index].x, pieces[index].y, pieces[index].x, 751, 0, 1)
    if temp != None:
        print(temp.piece)
    if rook_or_queen(temp):
        return False

    temp = direction_check(pieces[index].x, pieces[index].y, pieces[index].x, 49, 0, -1)
    if temp != None:
        print(temp.piece)
    if rook_or_queen(temp):
        return False

    temp = direction_check(pieces[index].x, pieces[index].y, 751, 751, 1, 1)
    if temp != None:
        print(temp.piece)
    if bishop_or_queen(temp):
        return False

    temp = direction_check(pieces[index].x, pieces[index].y, 49, 751, -1, 1)
    if temp != None:
        print(temp.piece)
    if bishop_or_queen(temp):
        return False

    temp = direction_check(pieces[index].x, pieces[index].y, 751, 49, 1, -1)
    if temp != None:
        print(temp.piece)
    if bishop_or_queen(temp):
        return False

    temp = direction_check(pieces[index].x, pieces[index].y, 49, 49, -1, -1)
    if temp != None:
        print(temp.piece)
    if bishop_or_queen(temp):
        return False

    return attack()

def valid_move():  #moves through king...

    global pieces, index, original_position
    if pieces[index].piece == "Rook":
        if pieces[index].x == original_position[0] or pieces[index].y == original_position[1]:
            return collision_detection()
        else:
            [pieces[index].x, pieces[index].y] = original_position
            return False
    elif pieces[index].piece == "Pawn":
        #if [pieces[index].x, pieces[index].y] == [original_position[0] + 100, original_position[1] + 100]:
            #if board[int(floor(pieces[index].y/ 100))][int(floor(pieces[index].x / 100))] != None:
                #return collision_detection()
            #else:
                #[pieces[index].x, pieces[index].y] = original_position
                #return False
        #elif [pieces[index].x, pieces[index].y] == [original_position[0], original_position[1] + 200]:
        return collision_detection()
    elif pieces[index].piece == "Bishop":
        if pieces[index].x != original_position[0] and pieces[index].y != original_position[1] and abs(pieces[index].y - original_position[1]) == abs(pieces[index].x - original_position[0]):
            return collision_detection()
        else:
            print("here")
            [pieces[index].x, pieces[index].y] = original_position
            return False 
    elif pieces[index].piece == "Queen": 
        if pieces[index].x == original_position[0] or pieces[index].y == original_position[1] or abs(pieces[index].y - original_position[1]) == abs(pieces[index].x - original_position[0]):
            return collision_detection()
        else:
            [pieces[index].x, pieces[index].y] = original_position
            return False
    elif pieces[index].piece == "Knight":
        if (abs(pieces[index].x - original_position[0]) == 100 and abs(pieces[index].y - original_position[1])) == 200 or (abs(pieces[index].x - original_position[0]) == 200 and abs(pieces[index].y - original_position[1]) == 100):
            return attack()
        else:
            [pieces[index].x, pieces[index].y] = original_position
            return False
    elif pieces[index].piece == "King":  #change condition...
        if abs(sum(original_position) - (pieces[index].x + pieces[index].y)) == 100 or abs(pieces[index].y - original_position[1]) == abs(pieces[index].x - original_position[0]):
            #check for check-position
            return valid_move_king()
        else:
            [pieces[index].x, pieces[index].y] = original_position
            return False
    return True

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

        if valid_choice == True:
            pieces[index].x = x
            pieces[index].y = y

    def on_mouse_press(self, x, y, button, key_modifiers):

        global valid_choice, index, original_position

        original_position = []
        for i, piece in enumerate(pieces):
            if x in range(piece.x - 50, piece.x + 50) and y in range(piece.y - 50, piece.y + 50):
                if piece.colour == turn:
                    original_position = [piece.x, piece.y]
                    valid_choice = True
                    index = i
            
    def on_mouse_release(self, x, y, button, key_modifiers):
        
        global pieces, index, valid_choice, turn, found

        found = False
        
        if valid_choice is True:
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
    
        valid_choice = False

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
