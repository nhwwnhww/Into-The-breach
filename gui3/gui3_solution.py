import tkinter as tk
from tkinter import messagebox
from gui3_support import *

class TicTacToeView(AbstractGrid):
    def __init__(self, master):
        super().__init__(master, (3, 3), (300, 300))
        self._cache = {}

    def initial_redraw(self, board_state: list[list[Optional[str]]]) -> None:
        """ Task 1 version of redraw, which uses text annotations to represent markers. """
        self.clear()
        for i, row in enumerate(board_state):
            for j, marker in enumerate(row):
                text = marker if marker is not None else ''
                bbox = self.get_bbox((i, j))
                self.create_rectangle(*bbox)
                self.annotate_position((i, j), text)

    def _get_image_name(self, marker):
        if marker == 'X':
            return 'images/cross.png'
        elif marker == 'O':
            return 'images/naught.png'

    def redraw(self, board_state: list[list[Optional[str]]]) -> None:
        """ Task 2 version of redraw, which uses images to represent markers. """
        self.clear()
        for i, row in enumerate(board_state):
            for j, marker in enumerate(row):
                bbox = self.get_bbox((i, j))
                self.create_rectangle(*bbox)

                if marker is not None:
                    image_name = self._get_image_name(marker)
                    size = self.get_cell_size()
                    image = get_image(image_name, size, self._cache)
                    midpoint = self.get_midpoint((i, j))
                    self.create_image(midpoint, image=image)

class TicTacToe:
    def __init__(self, master):
        self._master = master
        master.title('Tic Tac Toe')

        self._model = TicTacToeModel()
        self._view = TicTacToeView(master)
        self._view.pack()

        self._view.redraw(self._model.get_board_state())
        self._view.bind('<Button-1>', self.attempt_move)
    
    def _handle_game_over(self, message: str) -> None:
        if messagebox.askyesno('Game Over', message):
            self._model.new_game()
            self._view.redraw(self._model.get_board_state())
        else:
            self._master.destroy()

    def attempt_move(self, event):
        cell = self._view.pixel_to_cell(event.x, event.y)
        if self._model.attempt_place_marker(cell):
            self._view.redraw(self._model.get_board_state())
            self._master.update()

            winner = self._model.get_winner()
            if winner is not None:
                self._handle_game_over(f'{winner} wins! Play again?')
            
            elif self._model.is_board_full():
                self._handle_game_over('Draw! Play again?')

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
