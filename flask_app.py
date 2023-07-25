from flask import Flask, render_template, request
from .game.board import Board, board_from_repr

app = Flask(__name__)
game_board = Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board')
def board():
    tableHTML = "<table class=\"mainBoard\">"

    for row in [0, 3, 6]:
        tableHTML += "<tr>"
        for col in range(3):
            macrocell = row + col 
            winner = game_board.subboard_winner(macrocell)

            if macrocell == game_board.current_board or (winner == None and game_board.current_board == -1):
                tableHTML += "<td class=\"currentBoard\">"
            else:
                tableHTML += "<td>"
            
            if winner != None:
                tableHTML += num_to_sym(winner)
            else:
                # This is terrible but it probably doesnt matter
                sboard = game_board.get_subboard(macrocell)
                tableHTML += "<table class=\"subboard\">"
                for srow in [0, 3, 6]:
                    tableHTML += "<tr>"
                    for scol in range(3):
                        microcell = srow + scol 
                        tableHTML += f"<td>{num_to_sym(sboard[microcell])}</td>"
                    tableHTML += '</tr>'
                tableHTML += '</table>'

            tableHTML += "</td>"
        tableHTML += "</tr>"
    tableHTML += "</table>"

    return tableHTML

def num_to_sym(num):
    match num:
        case 1:
            return 'X'
        case -1:
            return 'O'
    return ' '

@app.route('/update_board', methods=['POST'])
def updateBoard():
    global game_board
    board_repr = request.form.get('board_repr')
    
    if board_repr:
        # Do some processing with the input string (you can add your custom logic here)
        game_board = board_from_repr(board_repr)
        print(board_repr)
        return "Success"
    else:
        return "Please provide an input string."

if __name__ == '__main__':
    app.run(debug=True)
