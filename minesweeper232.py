
# Final Project

import pygame
import time
import random
import sys
from collections import deque


#create a board list which contain mines in random position
def create_board(row,col):
    board_list = []#create a initial board
    random_list = ["MINE"]*mine_num+[None]*(row*col-mine_num)# create a list which contain enough mines
    random.shuffle(random_list)#random the index of the mines
    #transform this random list into the board so that we can use the index as the row and col of the positions.
    for i in range(row):
        each_row_list = []
        board_list.append(each_row_list)
        for l in range(col):
            each_row_list.append(random_list[0])
            random_list.pop(0)   
    return board_list


#make a list which contain the index of all the mines
def get_mine(board):
    mines = []
    for a, line in enumerate(board):
        for b, mine in enumerate(line):
            if mine == "MINE":
                mines.append([a,b])
    return mines

#find how many mines around the pressed location
def num_mines(p_row,p_col,board): 
    #to get the range of the index of eight positions around the pressed location
    row_start = p_row - 1 if p_row - 1 >= 0 else p_row
    row_stop = p_row + 2 if p_row + 1 <= row - 1 else p_row + 1
    col_start = p_col - 1 if p_col - 1 >= 0 else p_col
    col_stop = p_col + 2 if p_col + 1 <= col - 1 else p_col + 1
    
    mine_num = 0
    for i in range(row_start, row_stop):
        for j in range(col_start, col_stop):
            #search how many mines around the pressed location
            if board[i][j] == 'MINE':
                mine_num += 1
    board[p_row][p_col] = mine_num # save the mines amount into the board_list

#display the base and num when you open a gird according the information in the board list
def show_base_num(row,col,board):
        #display the base image
        screen.blit(pic_base,((col+1.5)*size, (row+2.5)*size))
        pygame.display.update()
        #check the number of the grid on the board list, and display the number image
        if board[row][col] == 1:
            screen.blit(pic_1, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 2:
            screen.blit(pic_2, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 3:
            screen.blit(pic_3, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 4:
            screen.blit(pic_4, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 5:
            screen.blit(pic_5, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 6:
            screen.blit(pic_6, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 7:
            screen.blit(pic_7, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()
        if board[row][col] == 8:
            screen.blit(pic_8, ((col+1.5)*size, (row+2.5)*size))
            pygame.display.update()

#display all the mines when the player clicks on the mine.
def show_all_mines(board_list):        
    for i in get_mine(board_list):
        screen.blit(pic_mine, ((i[1]+1.5)*size, (i[0]+2.5)*size))
        pygame.display.update()

#when player click on an empty grid, this will search the non-mine area around the empty grid
def find_empty(board, pos, point_x_range,point_y_range):
    x = pos[0]#x-position of the click
    y = pos[1]#y-pos of the click
    Empty,num,used = [],[],[]#lists for empty grids; grids contains numbers; and searched grids
    queue = [x-1,y],[x,y-1],[x,y+1],[x+1,y],[x-1,y-1],[x+1,y-1],[x+1,y+1],[x-1,y+1]#index list, 8 grids around the click
    q = deque() #FIFO queue, to save the grids that going to check
    for o in queue:
        q.append(o)
    while q != deque([]): #while dequeue not empty
        v = q.popleft() #a list that has x and y index component
        used += [v] # record the checked grids
        if v != None:
            w ,r = v[0],v[1] #w as index in x-axis,r as index in y-axis
            if w < point_x_range[0] or r<point_y_range[0] or w >point_x_range[1] or r>point_y_range[1]:#avoid index out of range
                continue
            if board[w][r] == 0: #this is an empty grid
                Empty += [v] #same the index point
                subque = [w-1,r],[w,r-1],[w,r+1],[w+1,r],[w-1,r-1],[w+1,r-1],[w+1,r+1],[w-1,r+1] #grids around the checked grid
                for p in subque:
                    if p not in q and p not in Empty and p not in num and p != v and p not in used: #if never checked, add into q
                        q.append(p)
            elif board[v[0]][v[1]] != 'MINE': #grids contain numbers
                num += [v]
    return Empty, num

            
#right click
def right_click(pos,poss,board_list,uncovered_grids,remain_mine): 
    if pos not in uncovered_grids:
        n_pos = poss.count(pos)
        if remain_mine == 0:
            if n_pos%2 == 0:# if it is the second time the player click the right_click, delete the flag
                if pos in poss:
                    remain_mine += 1 #number of remaining flags, the number on the left top of the game
                    poss.remove(pos)
                    poss.remove(pos)
                    screen.blit(pic_top, ((pos[1]+1.5)*size, (pos[0]+2.5)*size))
                    pygame.display.update()
            else:
                poss.remove(pos)
        else:
            if n_pos%2 == 0:# if it is the second time the player click the right_click, delete the flag
                remain_mine += 1 #number of remaining flags, the number on the left top of the game
                poss.remove(pos)
                poss.remove(pos)
                screen.blit(pic_top, ((pos[1]+1.5)*size, (pos[0]+2.5)*size))
                pygame.display.update()
            elif remain_mine > 0: # first right_click, plant the flag,can only plant flag if there is remaining
                remain_mine -= 1 #number of remaining flags
                screen.blit(pic_flag, ((pos[1]+1.5)*size, (pos[0]+2.5)*size))
                pygame.display.update()
    return remain_mine #update the number of flags

#left click
def left_click(pos,poss,board,uncovered_grids,remain_mine):
    if pos not in uncovered_grids: #check the click is on a covered grid (not showing empty grid, number)
        if pos in get_mine(board) and poss.count(pos)%2 == 0: #if play click on mine and there is no flag
            #mines all shown and player lose
            show_all_mines(board)
            pygame.time.wait(2000)
            screen = pygame.display.set_mode((500, 500))
            screen.blit(pic_lose,(0,0))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        else: #click on empty or number grids
            n_pos = poss.count(pos) 
            if n_pos%2 == 0: #if the grid has no flag on it
                x = pos[0]
                y = pos[1]
                uncovered_grids += [pos]
                show_base_num(x,y,board) #uncover the grid
                if board[x][y] == 0: #if grid is empty
                    Empty, num = find_empty(board, pos,point_x_range,point_y_range)
                    allgrid = Empty + num #all uncovered grids in one click
                    uncovered_grids +=allgrid # collect all uncovered grids
                    for i in allgrid:#show all empty and number grids around the click
                        if poss.count(i)%2 != 0:#when the grid has a flag on it, add the flag back and uncover the grid
                            remain_mine += 1
                        show_base_num(i[0],i[1],board)
    return remain_mine

#Record all the unfind mines after the player find a mine.
def get_all_mine(pos, poss, mine_list, mine_detected):
    #when the player put a flag on the same position of the mine, remove this mine from the mine list, add the pos to detected list
    if pos in mine_list and poss.count(pos)%2 != 0:
        mine_detected.append(pos)
        mine_list.remove(pos)
    # if the flag is removed, add back the mine position to mine list and remove it from detected
    elif pos in mine_detected and poss.count(pos)%2 == 0:
        mine_list.append(pos)
        mine_detected.remove(pos)
#        
#
#main part of the game

pygame.init()
pygame.display.init()
#set three levels of game which have diiferent requirement of screen and board and ask the player to choose the difficulty level
while True:
    difficulty = input("Select the difficulty (easy/medium/hard):")
    if difficulty == "easy":
        w = 600
        h = 600
        row = 9
        col = 9
        size = 50
        text_size = 20
        mine_num = 10
        point_x_range = [0, 8]
        point_y_range = [0, 8]
        break
    if difficulty == "medium":
        w = 665
        h = 665
        row = 16
        col = 16
        size = 35
        text_size = 20
        mine_num = 40
        point_x_range = [0, 15]
        point_y_range = [0, 15]
        break
    if difficulty == "hard":
        w = 1155
        h = 665
        row = 16
        col = 30
        size = 35
        text_size = 25
        mine_num = 99
        point_x_range = [0, 15]
        point_y_range = [0, 29]
        break
    else:
        print('incorrect command, try again')
        continue
#set the initial screen of the game    
screen = pygame.display.set_mode((w, h))
screen.fill("white")
pygame.display.update()
pygame.display.set_caption("minesweeper")

#load all the pictures we needs to the game and tansform to the size we want
pic_base = pygame.image.load("resource/base.bmp")
pic_base = pygame.transform.scale(pic_base,(size,size))

pic_flag = pygame.image.load("resource/flag.bmp")
pic_flag = pygame.transform.scale(pic_flag,(size,size))

pic_mine = pygame.image.load("resource/mine.bmp")
pic_mine = pygame.transform.scale(pic_mine,(size,size))

pic_top = pygame.image.load("resource/top.bmp")
pic_top = pygame.transform.scale(pic_top,(size,size))

pic_1 = pygame.image.load("resource/1.bmp")
pic_1 = pygame.transform.scale(pic_1,(size,size))

pic_2 = pygame.image.load("resource/2.bmp")
pic_2 = pygame.transform.scale(pic_2,(size,size))

pic_3 = pygame.image.load("resource/3.bmp")
pic_3 = pygame.transform.scale(pic_3,(size,size))

pic_4 = pygame.image.load("resource/4.bmp")
pic_4 = pygame.transform.scale(pic_4,(size,size))

pic_5 = pygame.image.load("resource/5.bmp")
pic_5 = pygame.transform.scale(pic_5,(size,size))

pic_6 = pygame.image.load("resource/6.bmp")
pic_6 = pygame.transform.scale(pic_6,(size,size))

pic_7 = pygame.image.load("resource/7.bmp")
pic_7 = pygame.transform.scale(pic_7,(size,size))

pic_8 = pygame.image.load("resource/8.bmp")
pic_8 = pygame.transform.scale(pic_8,(size,size))

pic_win = pygame.image.load("resource/win.bmp")
pic_win = pygame.transform.scale(pic_win,(500,500))

pic_lose = pygame.image.load("resource/lose.bmp")
pic_lose = pygame.transform.scale(pic_lose,(500,500))

pic_white = pygame.image.load("resource/white.bmp")
pic_white= pygame.transform.scale(pic_white,(size*2.5,size*2))

# create a board list
board = create_board(row,col)


#请勿商用#仅供娱乐#No commercial use allowed            
#display the game board on the screen 
for a,line in enumerate(board):
    for b,num in enumerate(line):
        screen.blit(pic_top,((b+1.5)*size, (a+2.5)*size))
        pygame.display.update()
#calculate the number of mines aroud each grid and update this information to the board list
for i in range(row):
    for j in range(col):
        if board[i][j] != 'MINE':
            num_mines(i,j,board)



mine_list = get_mine(board)#the index of all the mines
mine_detected = list() # mine's position index list that has flag on it
poss = [] # position collection of flags
uncovered_grids = [] # uncovered grids, to prevent repetition

#set the limit side of the board for mouse click
a_side_limit_top, a_side_limit_bottom= size*2.5, size*(2.5+row)
b_side_limit_left,b_side_limit_right = size*1.5, size*(1.5+col)

#load font we need to the game and transform to the size we want
font = pygame.font.Font('resource/Number.ttf', size * 2)
font_s = pygame.font.Font('resource/Text.ttf', text_size)
f_width, f_height = font.size('999')
orange = (255, 165, 0)
purple = (205, 205, 255)
black = (100, 100, 100)

#set a timer
elapsed_time = 0
last_time = time.time()
start_record_time = False    
clock = pygame.time.Clock()
remain_mine = mine_num


while True:
    if difficulty == "easy":
        explain_text_1 = """The number represents the number of"""
        explain_1 = font_s.render(explain_text_1, True, black)
        screen.blit(explain_1, (125, 0))
        explain_text_2 = """mines in the 8 grids around this grid."""
        explain_2 = font_s.render(explain_text_2, True, black)
        screen.blit(explain_2, (125, 20))
        explain_text_3 = """Flag all mines to win,"""
        explain_3 = font_s.render(explain_text_3, True, black)
        screen.blit(explain_3, (125, 40))
        explain_text_4 = """click mines will lose."""
        explain_4 = font_s.render(explain_text_4, True, black)
        screen.blit(explain_4, (125, 60))
        explain_text_5 = """Difficulty can be increased by"""
        explain_5 = font_s.render(explain_text_5, True, black)
        screen.blit(explain_5, (125, 80))
        explain_text_6 = """adding mines."""
        explain_6 = font_s.render(explain_text_6, True, black)
        screen.blit(explain_6, (125, 100))
        pygame.display.update()
    elif difficulty == "medium":
        explain_text_1 = """The number represents the number of mines in"""
        explain_1 = font_s.render(explain_text_1, True, black)
        screen.blit(explain_1, (110, 0))
        explain_text_2 = """the 8 grids around this grid."""
        explain_2 = font_s.render(explain_text_2, True, black)
        screen.blit(explain_2, (110, 20))
        explain_text_3 = """Flag all mines to win, click mines will lose."""
        explain_3 = font_s.render(explain_text_3, True, black)
        screen.blit(explain_3, (110, 40))
        explain_text_4 = """Left click for click, right click for flag."""
        explain_4 = font_s.render(explain_text_4, True, black)
        screen.blit(explain_4, (110, 60))
        pygame.display.update()
    elif difficulty == "hard":
        explain_text_1 = """The number represents the number of mines in the 8 grids around this grid."""
        explain_1 = font_s.render(explain_text_1, True, black)
        screen.blit(explain_1, (150, 5))
        explain_text_2 = """Flag all mines to win, click mines will lose."""
        explain_2 = font_s.render(explain_text_2, True, black)
        screen.blit(explain_2, (150, 25))
        explain_text_3 = """Left click for click, right click for flag."""
        explain_3 = font_s.render(explain_text_3, True, black)
        screen.blit(explain_3, (150, 45))
        pygame.display.update()
    
    #display the number of remain mines at the top of the screen
    if remain_mine >= 0: #only show numbers when there are remain flags
        mine_text = font.render('%02d' % (remain_mine), True, orange)
        screen.blit(pic_white, (0,0))
        screen.blit(mine_text, (30, (size * 2 - f_height) // 2 - 2))
        pygame.display.update()

    #display the time 
    if start_record_time and time.time() - last_time >= 1:
        elapsed_time += 1
        last_time = time.time()
    mine_text = font.render('%03d' % elapsed_time, True, purple)
    screen.blit(pic_white, (w - f_width - 30 ,(size * 2 - f_height) // 2 - 2))
    screen.blit(mine_text, (w - f_width - 30, (size * 2 - f_height) // 2 - 2))
    clock.tick(60)
    pygame.display.update()

    #get the action from the player
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
            b1, b2, b3 = pygame.mouse.get_pressed()# left click, middle click, and right click status of the mouse
            pos = pygame.mouse.get_pos() # get a (x,y) coordinate of the click
            b,a = pos # col and row coordinates
            #check the click is inside the board
            if a_side_limit_top <= a <= a_side_limit_bottom and b_side_limit_left <= b <= b_side_limit_right:
                b =(b)/size-1.5 # col
                a =(a)/size-2.5 # row
                a,b = int(a),int(b)
                pos = [a,b] # same as the index in board
                start_record_time = True
                if b1 and not b2 and not b3:  # left click
                    remain_mine = left_click(pos,poss,board,uncovered_grids,remain_mine)    
                elif not b1 and not b2 and b3:  # right click
                    poss+= [pos]
                    remain_mine = right_click(pos,poss,board,uncovered_grids,remain_mine)
                    get_all_mine(pos,poss,mine_list,mine_detected) # calcuate how many mines left
                    
                    
        #when the player find all the mines, show the win image and quit the game
        elif len(mine_list) == 0:
            pygame.time.wait(2000)
            screen = pygame.display.set_mode((500, 500))
            screen.blit(pic_win,(0,0))
            pygame.display.update()
            pygame.time.wait(2000) 
            pygame.quit()
            sys.exit()
            

