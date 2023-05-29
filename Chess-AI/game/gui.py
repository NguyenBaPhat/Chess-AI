import PySimpleGUI as sg
from game.board import ChessBoard
from game.searching import calculateMove
import chess

class ChessGUI(sg.Window):
    def __init__(self, title):
        self.board = ChessBoard()
        self.status_msg = 'None'
        super().__init__(title, self.get_layout())

    def get_layout(self):
        layout = [[sg.Text('Chess ', auto_size_text=True,
                           key='-STATUS-', font='Default 20')]]
        layout += self.board.get_layout()
        layout += [[sg.Button('New Game', size=(8, 1), key='-RESTART-'),
            sg.Button('Play AI', size=(8, 1), key='-PLAYAI-'),
            sg.Button('Exit', size=(8, 1), key='-EXIT-')]]
        
        return layout

    def update_status(self):
        msg = f'{"WHITE" if self.board.turn else "BLACK"} to move..'

        if self.board.is_game_over():
            if self.board.is_checkmate():
                winner = 'WHITE' if self.board.outcome().winner else 'BLACK'
                msg = f'CHECKMATE!!! {winner} wins!'
            elif self.board.is_stalemate():
                msg = 'Draw by STALEMATE!'
            elif self.board.is_insufficient_material():
                msg = 'Draw by INSUFFICIENT MATERIAL!'

        self.status_msg = msg
        self['-STATUS-'].update(self.status_msg)

    def update_board(self, event):
        if event == '-RESTART-':
            self.board.reset()
        elif event == '-PLAYAI-':
            self.play_ai()
        for rank in self.board.table:
            for tile in rank:
                if tile.key == event:
                    self.board.handle_move(tile)
        self.board.update_display()
    
    def play_ai(self):
        while not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                event, values = self.read()
                if event in (sg.WIN_CLOSED, 'Exit', '-EXIT-'):
                    break
                self.update_board(event)
                self.update_status()
                self.refresh()
            else:
                move = calculateMove(self.board)
                if move is not None:
                    self.board.push(move)
                    self.board.update_display()
                    self.update_status()
                    self.refresh()

        self.update_status()
        self.refresh()
