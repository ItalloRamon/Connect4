import curses
import sys
import os
from engine import *


empty_square = ['|-----', '|', '|', '|']
ball_extrmes = ' 000 '
ball_middle = '00000'

# Drawing grid
def draw_board(board, stdscr):
    for y in range(6):
        for x in range(7):
            stdscr.addstr((y+1)*4, x*6, empty_square[0])
            stdscr.addstr(1 + (y+1)*4, x*6, empty_square[1])
            stdscr.addstr(2 + (y+1)*4, x*6, empty_square[2])
            stdscr.addstr(3 + (y+1)*4, x*6, empty_square[3])
            
            if board[y, x] == 1:
                stdscr.addstr(1 + (y+1)*4, x*6+1, ball_extrmes, curses.color_pair(1))
                stdscr.addstr(2 + (y+1)*4, x*6+1, ball_middle, curses.color_pair(1))
                stdscr.addstr(3 + (y+1)*4, x*6+1, ball_extrmes, curses.color_pair(1))

            elif board[y, x] == 2:
                stdscr.addstr(1 + (y+1)*4, x*6+1, ball_extrmes, curses.color_pair(2))
                stdscr.addstr(2 + (y+1)*4, x*6+1, ball_middle, curses.color_pair(2))
                stdscr.addstr(3 + (y+1)*4, x*6+1, ball_extrmes, curses.color_pair(2))
            

            if x == 6:            
                stdscr.addstr((y+1)*4, x*6+6, '|')
                stdscr.addstr(1 + (y+1)*4, x*6+6, '|')
                stdscr.addstr(2 + (y+1)*4, x*6+6, '|')
                stdscr.addstr(3 + (y+1)*4, x*6+6, '|')
    
    stdscr.addstr(4 + (y+1)*4, 0, '|-----'*7 + '|')
    
    stdscr.addstr(6*5+2, 0, 'Press "q" to quit')



def drop_piece(stdscr, board, player, column):
    row = row_empty(board, column)
    play(board, row, column, player)
    
    if check_victory(board, player):
        stdscr.addstr(6*5, 0, f'PLAYER {player} WINS', curses.color_pair(player))
        stdscr.addstr(6*5+1, 0, 'Press "m" to return to the main menu')
        return True
    return False


def main_menu(stdscr): 
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)

    difficulty = 'Normal' 
    diff = 5

    cursor_y = 0

    k = 0
    while k != ord('q'):
        if k == curses.KEY_DOWN and cursor_y < 2:
            cursor_y += 1
        elif k == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1

        elif (k == curses.KEY_RIGHT or k == curses.KEY_LEFT)  and cursor_y == 2:
            if difficulty == 'Normal':
                difficulty = '  Hard'
                diff = 7
            else:
                difficulty = 'Normal'
                diff = 5

        elif k == 10:
            if cursor_y == 0:
                return play_game(stdscr)
            elif cursor_y == 1:
                return play_game(stdscr, game_mode='AI', diff=diff)


        if cursor_y == 0:
            stdscr.addstr(0, 0, "Play with a friend", curses.color_pair(4))
        else:
            stdscr.addstr(0, 0, "Play with a friend", curses.color_pair(3))

        if cursor_y == 1:
            stdscr.addstr(1, 0, "Play against AI", curses.color_pair(4))
        else:
            stdscr.addstr(1, 0, "Play against AI", curses.color_pair(3))
        
        if cursor_y == 2:
            stdscr.addstr(2, 0, f"AI difficulty: {difficulty}", curses.color_pair(4))
        else:
            stdscr.addstr(2, 0, f"AI difficulty: {difficulty}", curses.color_pair(3))
            

        stdscr.addstr(6*5+2, 0, 'Press "q" to quit')

        stdscr.refresh()
        k = stdscr.getch()


def init_game():
    return np.zeros((6, 7), int), False, 0, 0



def play_game(stdscr, game_mode='multiplayer', diff=5):
    board, game_over, turn, cursor_x = init_game()
    k = 0
    
    stdscr.clear()
    stdscr.refresh()
    
    while k != ord('q'):
        if game_over and k == ord('m'):
            return main_menu(stdscr)

        if not game_over:     
            stdscr.clear()
            if k == curses.KEY_RIGHT and cursor_x < 6:
                cursor_x += 1

            elif k == curses.KEY_LEFT and cursor_x > 0:
                cursor_x -= 1

            # Drop player chip
            elif k == 10:
                if valid_location(board, cursor_x):
                    game_over = drop_piece(stdscr, board, turn+1, cursor_x) 
                    turn += 1
                    turn %= 2
                
                if game_mode == 'AI':
                    draw_board(board, stdscr)   
                    stdscr.refresh()

                    col, minnimax_score = minimax(board, diff, -math.inf, math.inf, True)
                    if valid_location(board, col):
                        game_over = drop_piece(stdscr, board, turn+1, col)
                        turn += 1
                        turn %= 2


            # Draw player piece for selecting column
            stdscr.addstr(0, cursor_x * 6 + 1, ball_extrmes, curses.color_pair(turn+1))
            stdscr.addstr(1, cursor_x * 6 + 1, ball_middle, curses.color_pair(turn+1))
            stdscr.addstr(2, cursor_x * 6 + 1, ball_extrmes, curses.color_pair(turn+1))
        
        # Draw game board
        draw_board(board, stdscr)   

        stdscr.refresh()
        k = stdscr.getch()



def main():
    curses.wrapper(main_menu)



if __name__ == '__main__':
    main()
