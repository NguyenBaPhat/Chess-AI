import chess
import PySimpleGUI as sg
from game.tile import Tile

PIECES = {'K': 'wk.png', 'Q': 'wq.png', 'B': 'wb.png', 'R': 'wr.png', 'N': 'wn.png', 'P': 'wp.png', 'k': 'bk.png',
              'q': 'bq.png', 'b': 'bb.png', 'r': 'br.png', 'n': 'bn.png', 'p': 'bp.png'}
BLANK = 'blank.png'

class ChessBoard(chess.Board):
    def __init__(self):
        super().__init__(chess960=False)
        self.table = [[Tile(file, rank) for file in range(8)] for rank in range(8)]
        #chứa các đối tượng Tile đại diện cho từng ô trên bàn cờ
        self.pending_move = []              #danh sách chứa các ô đang được chọn cho một nước đi
        self.available_squares = []         #danh sách các ô có thể di chuyển đến từ ô đang được chọn
        self.squares_in_danger = []         #danh sách các ô có khả năng bị ăn
        
 #tạo ra bố cục (layout) của bàn cờ trên giao diện người dùng.
    def get_layout(self):
        board_layout = []
        for rank in range(8):
            layout_row = [sg.Text(chess.RANK_NAMES[7 - rank])]
            for file in range(8):
                tile = self.table[rank][file]
                if self.piece_at(tile.square) is not None:
                    tile.set_image(PIECES[str(self.piece_at(tile.square))])
                layout_row.append(tile.button)
            board_layout.append(layout_row)
        file_names = [sg.Text(chess.FILE_NAMES[i].upper(
        ), expand_x=True, justification='center') for i in range(8)]
        board_layout.append(file_names)
        return board_layout
    
#trả về tên tệp hình ảnh của quân cờ tại một ô nhất định trên bàn cờ
    def get_piece_img(self, tile):
        if self.piece_at(tile.square):
            return PIECES[str(self.piece_at(tile.square))]
        else:
            return BLANK
        
# cập nhật giao diện bàn cờ 
    def update_display(self):
        for rank in self.table:
            for tile in rank:
                piece_img = self.get_piece_img(tile)
                self.highlight_tile(tile)
                tile.update_image(piece_img) 

# định nghĩa màu nền cho mỗi ô dựa trên trạng thái của nó, bao gồm việc chọn, di chuyển và có có khả năng bị ăn
    def highlight_tile(self, tile):
        if tile.name in self.pending_move:
            bg_color = 'yellow'
        elif tile.name in self.available_squares:
            if self.piece_at(tile.square) and self.is_attacked_by(self.turn, tile.square):
                bg_color = 'orange'
            else:
                bg_color = 'lime'
        elif tile.name + 'q' in self.available_squares:
            bg_color = 'purple'
        else:
            bg_color = tile.bgcolor
        if self.is_check() and tile.square == self.king(self.turn):
            bg_color = 'red'
        tile.change_bg_color(bg_color)

#  tìm và lưu trữ danh sách các ô có thể di chuyển từ một ô được chọn
    def get_available_squares(self, tile):
        legal_moves = [str(move) for move in self.legal_moves]
        for move in legal_moves:
            if move[:2] == tile.name:
                self.available_squares.append(move[2:])

# xử lý một nước đi trên bàn cờ.
    def handle_move(self, tile):
        if self.color_at(tile.square) == self.turn or len(self.pending_move) == 1:
            self.get_available_squares(tile)
            self.pending_move.append(tile.name)
        if len(self.pending_move) == 2:
            try:
                move = self.parse_uci(''.join(self.pending_move))
                self.push(move)
            except ValueError:
                try:
                    self.pending_move.append('q')
                    if self.parse_uci(''.join(self.pending_move)) in self.legal_moves:
                        promote_to = sg.Window("Choose Your Promotion", [[sg.Button('Queen'), sg.Button(
                            'Rook'), sg.Button('Bishop'), sg.Button('Knight')]]).read(close=True)[0]
                        if promote_to == 'Queen':
                            promote = 'q'
                        elif promote_to == 'Rook':
                            promote = 'r'
                        elif promote_to == 'Bishop':
                            promote = 'b'
                        elif promote_to == 'Knight':
                            promote = 'n'
                        self.pending_move[-1] = promote
                        move = self.parse_uci(''.join(self.pending_move))
                        self.push(move)
                except ValueError:
                    sg.PopupQuickMessage('Invalid Move!')
            self.available_squares = []
            self.pending_move = []
    