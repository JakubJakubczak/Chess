from tkinter import *

GAME_WIDTH = 700
GAME_HEIGHT = 620
BOARD_WIDTH = 550
BOARD_HEIGHT = 550
BOARD_PADX = 30
BOARD_PADY = 30
SIZE = 8
SPACE_SIZE = BOARD_WIDTH/SIZE
SQUARES_COLORS = ["white", "green"]

SQUARES = [[0] * SIZE for _ in range(SIZE)]
rook = 5
knight = 3
bishop = 4
queen = 9
king = 2
pawn = 1
BOARD = [[0] * SIZE for _ in range(0, int(SIZE))]
''' 
BOARD = [[-rook, -knight, -bishop, -queen, -king, -bishop, -knight, -rook],
        [-pawn, -pawn, -pawn, -pawn, -pawn, -pawn, -pawn, -pawn, -pawn],
        [0, 0, 0, 0, 0, 0, 0 ,0],
        [0, 0, 0, 0, 0, 0, 0 ,0],
        [0, 0, 0, 0, 0, 0, 0 ,0],
        [0, 0, 0, 0, 0, 0, 0 ,0],
        [pawn, pawn, pawn, pawn, pawn, pawn, pawn, pawn, pawn   ],
        [rook, knight, bishop, queen, king, bishop, knight, rook]]
'''
gameOn = False
number_of_colors = 2
#figures = [[0] * SIZE for _ in range(0, int(SIZE))]



def isCheck():
    pass
def isMate():
    pass
def canCastle():
    pass
def castle():
    pass
def move(position):
    pass

def drag_start(event):
    global initial_position
    global drag_data
    item = event.widget.find_closest(event.x, event.y)
    item_type = event.widget.type(item)
    if item_type == 'rectangle':  # Check if the clicked item is a rectangle
        return  # Ignore rectangles
    drag_data = {'x': event.x, 'y': event.y, 'item': item}
    initial_position = {'x': event.x, 'y': event.y, 'item': item}

def drag_motion(event,canvas):
    global drag_data
    if drag_data:
        x, y = event.x - drag_data['x'], event.y - drag_data['y']
        canvas.move(drag_data['item'], x, y)
        drag_data['x'], drag_data['y'] = event.x, event.y
def drag_stop(event):
    global drag_data
   # if drag_data:
        #if drag_data['x']


def bind_figure(canvas, image_item):
    canvas.tag_bind(image_item, "<ButtonPress-1>", drag_start)
    canvas.tag_bind(image_item, "<B1-Motion>", lambda event: drag_motion(event, canvas))


def loadFigure(col, row,file, canvas):
    square_coords = canvas.coords(SQUARES[row - 1][col -1])
    square_coords_x1 = square_coords[0]
    square_coords_y1 = square_coords[1]
    square_coords_x2 = square_coords[2]
    square_coords_y2 = square_coords[3]

    photo_image = PhotoImage(master=game_window, file=file)
    image_height = photo_image.height()
    image_width = photo_image.width()
    figure_coords_x = (square_coords_x1 + square_coords_x2 - image_width) / 2
    figure_coords_y = (square_coords_y1 + square_coords_y2 - image_height) / 2

    return figure_coords_x, figure_coords_y, photo_image


def loadFigures(canvas):
    # definiowanie funkcji loadfigure(col, row, canvas)
    # zwracamy z tej funkcji koordynaty, photo_image oraz ewentualnie canvas
    # dodajemy do BOARDA odpowiednio obiekty(zaleznie jaka figura rozna klasa) z koordynatami i image
    #

    #white_pawns
    for col in range(1,SIZE +1):
        pre_last_row = 7
        file = 'w_pawn.png'
        color = 'white'
        x_coord, y_coord, photo = loadFigure(col, pre_last_row, file,canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        bind_figure(canvas, canvas_image)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image )
        BOARD[pre_last_row-1][col-1] = w_pawn

    # black_pawns
    for col in range(1, SIZE +1):
        pre_first_row = 2
        file = 'b_pawn.png'
        color = 'black'
        x_coord, y_coord, photo = loadFigure(col, pre_first_row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo,  canvas_image)
        BOARD[pre_first_row - 1][col - 1] = w_pawn

    # white_rooks
    for col in range(1, SIZE +1, SIZE-1):
        row = 8
        file = 'w_rook.png'
        color = 'white'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

    # black_rooks
    for col in range(1, SIZE + 1, SIZE - 1):
        row = 1
        file = 'b_rook.png'
        color = 'black'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn
    # white_bishop
    for col in range(2, SIZE, SIZE - 3):
        row = 8
        file = 'w_bishop.png'
        color = 'white'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

    # black_bishop
    for col in range(2, SIZE, SIZE - 3):
        row = 1
        file = 'b_bishop.png'
        color = 'black'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn
    # white_knight
    for col in range(3, SIZE-1, SIZE - 5):
        row = 8
        file = 'w_knight.png'
        color = 'white'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

    # black_bishop
    for col in range(3, SIZE-1, SIZE - 5):
        row = 1
        file = 'b_knight.png'
        color = 'black'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

    #queens
    for row in range(1, SIZE+1,SIZE-1):
        col = 4
        if row == 1:
            file = 'b_queen.png'
            color = 'black'
        if row == SIZE:
            file = 'w_queen.png'
            color = 'white'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

    # kings
    for row in range(1, SIZE + 1, SIZE - 1):
        col = 5
        if row == 1:
            file = 'b_king.png'
            color = 'black'
        if row == SIZE:
            file = 'w_king.png'
            color = 'white'
        x_coord, y_coord, photo = loadFigure(col, row, file, canvas)
        canvas_image = canvas.create_image(x_coord, y_coord, image=photo, anchor=NW)
        w_pawn = Pawn(color, x_coord, y_coord, photo, canvas_image)
        BOARD[row - 1][col - 1] = w_pawn

        '''
        square_coords = canvas.coords(SQUARES[pre_last_row-1][i])
        square_coords_x1 = square_coords[0]
        square_coords_y1 = square_coords[1]
        square_coords_x2 = square_coords[2]
        square_coords_y2 = square_coords[3]

        photo_image = PhotoImage(master=game_window, file='w_pawn.png')
        image_height = photo_image.height()
        image_width = photo_image.width()
        figure_coords_x = (square_coords_x1 + square_coords_x2 - image_width)/2
        figure_coords_y = (square_coords_y1 + square_coords_y2 - image_height)/2
        #znika, trzeba zrobic, zeby garbage colector nie usuwal zdjeć


        figures[pre_last_row - 1][i] = photo_image
        

    # black_pawns
    for i in range(0, 8):
        pre_first_row = 2
        square_coords = canvas.coords(SQUARES[pre_first_row  - 1][i])
        square_coords_x1 = square_coords[0]
        square_coords_y1 = square_coords[1]
        square_coords_x2 = square_coords[2]
        square_coords_y2 = square_coords[3]

        photo_image = PhotoImage(master=game_window, file='b_pawn.png')
        image_height = photo_image.height()
        image_width = photo_image.width()
        figure_coords_x = (square_coords_x1 + square_coords_x2 - image_width) / 2
        figure_coords_y = (square_coords_y1 + square_coords_y2 - image_height) / 2
        w_pawn: object = canvas.create_image(figure_coords_x, figure_coords_y, image=photo_image, anchor=NW)
        canvas.photo_image = photo_image
        # znika, trzeba zrobic, zeby garbage colector nie usuwal zdjeć
        canvas.pack()
        game_window.update()
        figures[pre_first_row  - 1][i] = photo_image
        BOARD[pre_first_row  - 1][i] = w_pawn

    # white_rooks
    number_of_rooks = 4
    for i in range(number_of_rooks):
        if i == 0:
            row = 8
            col = 1
            file = 'w_rook.png'
        if i == 1:
            row = 8
            col = 8
            file = 'w_rook.png'
        if i == 2:
            row = 1
            col = 1
            file = 'b_rook.png'
        if i == 3:
            row = 1
            col = 8
            file = 'b_rook.png'

        square_coords = canvas.coords(SQUARES[row - 1][col-1])
        square_coords_x1 = square_coords[0]
        square_coords_y1 = square_coords[1]
        square_coords_x2 = square_coords[2]
        square_coords_y2 = square_coords[3]

        photo_image = PhotoImage(master=game_window, file=file)
        image_height = photo_image.height()
        image_width = photo_image.width()
        figure_coords_x = (square_coords_x1 + square_coords_x2 - image_width) / 2
        figure_coords_y = (square_coords_y1 + square_coords_y2 - image_height) / 2
        rook: object = canvas.create_image(figure_coords_x, figure_coords_y, image=photo_image, anchor=NW)
        canvas.photo_image = photo_image
        # znika, trzeba zrobic, zeby garbage colector nie usuwal zdjeć
        canvas.pack()
        game_window.update()
        figures[row- 1][col-1] = photo_image
        BOARD[row - 1][col-1] = rook

        # zrobić funkcję z tego co się powiela i argumentem będzie obraz oraz wiersz, kolumna
        '''







    # tutaj zaladujemy do listy figures jako cale obiekty wraz z koordynatami
    # a nastepnie dodamy je do Boarda w odpowiednie poczatkowe miejsca juz jako obiekty canvas
    pass


'''
def divide_image(image_path, tiles_numberX, tiles_numberY):
    # Open the image
    image = Image.open(image_path)

    # Get the dimensions of the image
    width, height = image.size

    # Calculate the number of tiles horizontally and vertically
    tile_sizeX = width // tiles_numberX
    tile_sizeY = height // tiles_numberY

    # Divide the image into tiles
    tiles = []
    for y in range(0,tiles_numberY):
        for x in range(0,tiles_numberX):
            # Calculate coordinates for the current tile
            left = x * tile_sizeX
            upper = y * tile_sizeY
            right = left + tile_sizeX
            lower = upper + tile_sizeY
            # Crop the tile from the image and append it to the list
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)
    for i, tile in enumerate(tiles):
        # Example: Display each tile
        tile.show()
    return tiles
'''

def menu():
    global menu_window
    menu_window = Tk()
    menu_window.title("Chess")
    menu_window.resizable(False, False)

    canvas = Canvas(menu_window, width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()

    background_photo = PhotoImage(file='tlo2.png')
    background = canvas.create_image(0, 0, image=background_photo, anchor=NW)
    canvas.coords(background, 0, 100)

    image_size = canvas.bbox(background)
    end_of_backgroundY = image_size[3]

    game_Name = "CHESS GAME"
    font_size = 25
    game_label = canvas.create_text(GAME_WIDTH / 2, 0 + font_size, text=game_Name, font=("Roboto:", font_size),
                                    fill="green")

    button1 = Button(menu_window, text="Start the game",
                     font=("Roboto"),
                     command=startTheGame,
                     fg="#00FF00",
                     bg="black",
                     borderwidth=5,
                     relief="raised")
    button2 = Button(menu_window, text="Exit",
                     font=("Roboto"),
                     command=exitGame,
                     fg="#00FF00",
                     bg="black", )
    button1.pack()
    button2.pack()
    menu_window.update()

    width_button1 = button1.winfo_width()
    height_button1 = button1.winfo_height()
    width_button2 = button2.winfo_width()

    end_of_button1Y = end_of_backgroundY + height_button1

    start_of_button2Y = end_of_button1Y + 5

    button1.place(x=(GAME_WIDTH - width_button1) / 2, y=end_of_backgroundY)  # Adjust the coordinates (x, y) as needed
    button2.place(x=(GAME_WIDTH - width_button2) / 2, y=start_of_button2Y)  # Adjust the coordinates (x, y) as needed

    menu_window.mainloop()

def drawBoard(window,canvas):
    numbersLabel = []
    lettersLabel = []
    for number in range(1,SIZE+1):
        label = Label(window, text=str(number),
                              font="Roboto")
        numbersLabel.append(label)

    for number in range(0,SIZE):
        ascii_value = ord('A') + number
        letter = chr(ascii_value)
        label = Label(window, text=str(letter),
                              font="Roboto")
        lettersLabel.append(label)

    for row in range(0, SIZE):
        y1 = row * SPACE_SIZE + BOARD_PADY
        y2 = y1 + SPACE_SIZE
        numbersLabel[row].pack()
        window.update()
        label_width = numbersLabel[row].winfo_width()
        label_length = numbersLabel[row].winfo_height()
        numberCoordX = (BOARD_PADX-label_width)/2
        numberCoordY = (y1+y2-label_length)/2
        numbersLabel[row].place(x=numberCoordX, y=numberCoordY)
        for col in range(0, SIZE):
            if((row + col) %2 == 0):
                color = SQUARES_COLORS[0]
            else:
                color = SQUARES_COLORS[1]
            x1 = col * SPACE_SIZE + BOARD_PADX
            x2 = x1 + SPACE_SIZE
            SQUARES[row][col] = canvas.create_rectangle(x1,
                                                        y1,
                                                        x2,
                                                        y2,
                                                        fill=color)
    for col in range(0, SIZE):
        lastRow = 8
        lettersLabel[col].pack()
        window.update()
        width_of_letter = lettersLabel[col].winfo_width()
        heigth_of_letter = lettersLabel[col].winfo_height()
        squareCoords = canvas.coords(SQUARES[lastRow-1][col])
        squareCoordsx1 = (squareCoords[0])
        squareCoordsy1 = (squareCoords[1])
        squareCoordsx2 = (squareCoords[2])
        squareCoordsy2 = (squareCoords[3])
        x1 = (squareCoordsx1 + squareCoordsx2 - width_of_letter)/2
        below_board = 0.5
        y1 = squareCoordsy2 + below_board
        lettersLabel[col].place(x=x1, y=y1)

    canvas.pack()
    # iterujemy po boardzie, jeśli miejsce = 0 to pass, a jesli nie to wyswietlamy figurę

def drawFigures():
    pass

def startTheGame():
    global game_window
    game_window = Tk()
    menu_window.destroy()
    game_window.title("GAME")
    game_window.resizable(False, False)
    canvas = Canvas(game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
    drawBoard(game_window, canvas)
    loadFigures(canvas)
    drawFigures()

    game_window.mainloop()

def exitGame():
    menu_window.destroy()



menu()

