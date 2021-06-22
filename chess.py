import arcade
#maybe file for functions....

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
SCREEN_TITLE = "Starting Template"

names = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
pieces = [] #include class

valid_choice = False  
index = None

turn = "WHITE"

original_position = []  #include in class
release_x = None
release_y = None

def collision_detection():
    
    for i, piece in enumerate(pieces):       #potential bug
        if i != index and piece.x == pieces[index].x and piece.y == pieces[index].y:
            if piece.colour == pieces[index].colour or piece.piece == "King":
                pieces[index].x = original_position[0]
                pieces[index].y = original_position[1]
                return False
            else:
                pieces.pop(i)
                return True
    return True

def valid_move():

    global pieces, index, original_position
    #loop through direction that piece has moved.
    if pieces[index].piece == "Rook":
        if pieces[index].x == original_position[0]:
            return collision_detection()
        elif pieces[index].y == original_position[1]:
            return collision_detection()
        else:
            pieces[index].x = original_position[0]
            pieces[index].y = original_position[1]
            return False
    return True

def mouse_release(i, value): #the main purpose is to centre; also detects position change 

    global original_position, index

    if (value - (value % 50)) % 100 == 0:
        if original_position[i] != value - (value % 50) + 50:
            if i == 0:
                pieces[index].x = value - (value % 50) + 50
            elif i == 1:
                pieces[index].y = value - (value % 50) + 50
            return True
        else:
            if i == 0:
                pieces[index].x = original_position[i] 
            elif i == 1:
                pieces[index].y = original_position[i]
            return False
    elif (value - (value % 50)) % 100 != 0:
        if original_position[i] != value - (value % 50):
            if i == 0:
                pieces[index].x = value - (value % 50) 
            elif i == 1:
                pieces[index].y = value - (value % 50)
            return True
        else:
            if i == 0:
                pieces[index].x = original_position[i]
            elif i == 1:
                pieces[index].y = original_position[i]
            return False

class chess_piece():   #camel-case, capitalized

    def __init__(self, piece, colour, x, y):
        self.piece = piece
        self.colour = colour
        self.x = x
        self.y = y
    
    @classmethod
    def make_pieces(cls):
        for x, name in enumerate(names):
            pieces.append(chess_piece (name, "WHITE", (100 * x) + 50, 50))
            pieces.append(chess_piece (name, "BLACK", (100 * x) + 50, 750))
            pieces.append(chess_piece ("Pawn", "WHITE", (100 * x) + 50, 150))
            pieces.append(chess_piece ("Pawn", "BLACK", (100 * x) + 50, 650))

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):

        chess_piece.make_pieces()

    def on_draw(self):

        arcade.start_render()
        #Print chess-board
        z = 0
        for y in range(0, 701, 100):
            for x in range(0 + z, 701 + z, 100):
                if x % 200 == 0:
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.BLACK)
                else:
                    arcade.draw_xywh_rectangle_filled(x - z, y, 100, 100, arcade.color.WHITE)
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

        global pieces, index

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
        
        global pieces, index, valid_choice, turn, release_x, release_y

        if valid_choice == True:
            release_x = mouse_release(0, x)
            release_y = mouse_release(1, y)
            if (release_x or release_y) and valid_move() is True:
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
