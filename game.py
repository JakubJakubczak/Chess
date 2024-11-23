from Const import *
from board import *
from figures import *
from game_menu import *
from tkinter import *
from ai import *
from tkinter import messagebox
from Const import *
from menu import *
import time


class Game:
    def __init__(self, back_to_menu_callback):
        self.back_to_menu_callback = back_to_menu_callback
        self.depth = 2
        self.game_window = Tk()
        self.game_window.title("GAME")
        self.game_window.resizable(False, False)
        self.frame = Frame(self.game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.frame.pack()
        self.board = Board(self.frame, self)
        self.game_menu = Game_menu(self.frame, self)
        self.figures = Figures(self.board, self)
        self.ai = Ai()
        self.game_menu.display_score(self.board.score)
        evalu = self.ai.evaluate(self.board.engine)
        self.game_menu.display_eval(evalu)
        self.game_window.mainloop()


        if settings["AI"] == True and settings["TURN"] == False:
           random_move =  self.ai.generate_random_move(not settings["TURN"], self.board.engine)
           self.move(None, random_move[0], random_move[1], random_move[2], random_move[3])


    def handle_game_end(self):
        print("Game ended")
        result = self.board.get_result()
        # Handle game over logic here as before (message box or print)
        # from tkinter import messagebox
        # messagebox.showinfo("Game Over", f"Game Over: {result}")
        self.game_menu.display_result(result)

    def update(self, drag_data, x_start, y_start, x_end, y_end):
        promotion_val = None

        if self.board.engine.is_pawn_promotion(x_start, y_start, x_end, y_end):
            print("promotion")
            promotion_val = self.board.choose_piece()
            print(f"value {promotion_val}")

        self.move(drag_data, x_start, y_start, x_end, y_end, promotion_val)
        self.board.white_turn = not self.board.white_turn
        self.board.engine.update_valid_moves()
        self.update_menu_and_highlight(x_start, y_start, x_end, y_end)
        self.board.check_game_state()



        if settings["AI"] and self.board.white_turn != settings["TURN"] and self.board.game_on:
            self.make_ai_move()
            self.update_menu_and_highlight(x_start, y_start, x_end, y_end)
            self.board.check_game_state()

        print(f"all_valid_moves {self.board.engine.all_valid_moves(False)}")


    def update_menu_and_highlight(self, x_start, y_start, x_end, y_end):
        self.board.add_to_history(x_start, y_start, x_end, y_end)
        self.game_menu.display_history(self.board.history)
        self.game_menu.display_score(self.board.info[10])
        eval = self.ai.evaluate(self.board.engine)
        self.game_menu.display_eval(eval)

        self.board.dehighlight_valid_moves()
        self.board.dehighlight_last_move()
        self.board.highlight_move()


    def make_ai_move(self):
        promotion_val = None

        ## RANDOM MOVE
        # random_move = self.ai.generate_random_move(not settings["TURN"], self.board.engine)
        # if len(random_move) == 5:
        #     promotion_val = random_move[4]
        #
        # self.move(None, random_move[0], random_move[1], random_move[2], random_move[3], promotion_val)
        # self.board.white_turn = not self.board.white_turn



        start_time = time.time()
        best_move = self.ai.find_best_move(DEPTH, -1, self.board.engine)
        end_time = time.time()



        elapsed_time = end_time - start_time
        print("Elapsed time:", elapsed_time, "seconds")

        if best_move is None:
            print("No valid moves found for AI.")
            return

        if len(best_move[0]) == 5:
            promotion_val = best_move[0][4]

        print(f"best move {best_move}")

        self.move(None, best_move[0][0], best_move[0][1], best_move[0][2], best_move[0][3], promotion_val)

        self.board.white_turn = not self.board.white_turn
        self.board.engine.update_valid_moves()

    def move(self, drag_data, x_start, y_start, x_end, y_end, promotion_val = None):
        self.board.engine.move_board(x_start, y_start, x_end, y_end, promotion_val)
        self.figures.move_images(drag_data, x_start, y_start, x_end, y_end)




    def surrender(self):
        self.board.result = -1 if self.board.white_turn else 1
        self.board.game_on = False
        self.handle_game_end()

    def back_to_menu(self):
        self.game_window.destroy()
        self.back_to_menu_callback()

