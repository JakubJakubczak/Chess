from tkinter import *
from figures import *

GAME_WIDTH = 700
GAME_HEIGHT = 620
BOARD_PADX = 30
BOARD_PADY = 30




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






menu()

