'''
File: maze_solver.py
Author: Cole Suddarth
Purpose: To create a program which solves a reasonably established maze
   with no loops. It prints the position and maze at each move until the
   end has been reached, using the left hand rule.
Course: CSC120 Summer21
'''

def read_file():
    '''
    This function asks a user for a file to open, and opens it. Then it reads
    the file and appends each character to an array, and then appends that
    array to another array in order to create a 2D grid such that
    columns[y][x] represents an (x, y) location in the maze
    Arguments: None
    Return: Columns is a 2D-Array illustrating maze file
    Assumptions: The file exists, the contents of the file are a reasonable
        maze displayed in such a way that matches the spec
    '''
    print('Please give the maze file:')
    file_name = input()
    file_name = file_name.lstrip().rstrip()
    file = open(file_name)  # opens user file
    columns = []
    line_length = []

    for line in file:  # loops through each line
        line = line.strip('\n')  # strips new lines
        row = []
        for char in line:  # appends each character to list
            row.append(char)
        line_length.append(len(line))  # append length of line
        columns.append(row)  # creates 2d list
    
    return columns, line_length

def scan_for_start(maze_contents):
    '''
    This function moves through the 2D-Array representing the maze and
    searches for the starting position. It then cycles through some statements
    to determine the starting direction of solver pointer.
    Arguments: maze_contents is a 2D-Array representing a maze
    Return: x and y are integers representing position
        direction is a single character representing the pointer direction
    Assumptions: the file contains exactly one starting point, and the x and y
        coordinates are starting from 0,0
    '''
    y = 0
    for row in range(len(maze_contents)):
        x = 0
        # loops through each character in each row to find Start, 'S'
        for char in range(len(maze_contents[0])):
            if maze_contents[y][x] == 'S':  # if starting character is found
                if y != 0 and maze_contents[y-1][x] == '#': 
                    # if not top row and wall above, direction is North
                    maze_contents[y][x] = '^'
                    direction = 'N'
                elif x != 0 and maze_contents[y][x-1] == '#':
                    # if not far left and wall on left, start West
                    maze_contents[y][x] = '<'
                    direction = 'W'
                elif y != (len(maze_contents) - 1)\
                     and maze_contents[y+1][x] == '#':
                    # if not bottom and wall below, direction is South
                    maze_contents[y][x] = 'v'
                    direction = 'S'
                else:
                    # if not previous directions, it starts at East
                    maze_contents[y][x] = '>'
                    direction = 'E'
                return(x, y, direction)
            x += 1
        y += 1


def solve_maze(maze_contents):
    '''
    This function is the main solver. It first prints the starting maze and
    location. Then loops until the maze has been solved printing the maze, 
    position, and direction at every step of the way
    Arguments: maze_contents is a 2D-Array which containing characters 
        representing a maze
    Return: None
    Assumptions: The maze has an end that can be reasonably reached using the
    left hand rule(follow wall with left hand)
    '''
    # gets and prints initial position, direction and maze
    x, y, direction = scan_for_start(maze_contents)
    print_maze(maze_contents)
    print(f"\nCurrent Position:  {x},{y}\nCurrent Direction: {direction}\n")

    while True:
        if check_for_end(x, y, direction, maze_contents):
            # check if found the end if so break loop
            break
        # move the pointer using move_pointer
        x, y, direction = move_pointer(x, y, direction, maze_contents)
        # reprints the board and current position/direction
        print_maze(maze_contents)
        print(f"\nCurrent Position:  {x},{y}\nCurrent Direction: \
{direction}\n")

    print('Solution Found!')

def check_for_end(x, y, direction, maze_contents):
    '''
    Checks to see if the current position is the end of the puzzle
    Arguments: x & y are integers, represent previous coordinates of pointer
        direction is a character string representing direction of solver
        maze_contents is a 2D array of character strings representing maze
    Return: True if the end of the maze is reached in next move, False if not
    Assumptions: x and y can be validly used to index into maze_contents
    '''
    # only change x and y locally in this part here
    if direction == 'N':
        y -= 1
    elif direction == 'E':
        x += 1
    elif direction == 'S':
        y += 1
    else:
        x -= 1
    # moved to check if next move will be end

    if maze_contents[y][x] == 'E':
        return True
    return False

def move_pointer(x, y, direction, maze_contents):
    '''
    This function changes the previous move to a '.', then determines the new
    current x and y based on the direction. It then checks to see what the new
    direction should be, using if statements.
    Arguments: x & y are integers, represent previous coordinates of pointer
        direction is a character string representing direction of solver
        maze_contents is a 2D array of character strings representing maze
    Return: x and y are integers of the updated solver location
        direction is a character string represents updated direction of solver
    '''
    maze_contents[y][x] = '.'  # change previous position to a '.'
    
    # adjust current coordinates to be at the new point
    if direction == 'N':
        y -= 1
    elif direction == 'E':
        x += 1
    elif direction == 'S':
        y += 1
    else:
        x -= 1
    
    if direction == 'N':  # current direction is North
        if x != 0 and maze_contents[y][x-1] != ' ':  # check for left turn
            direction = 'W'
        elif y != 0 and maze_contents[y-1][x] != ' ':  # check straight path
            direction = 'N'
        elif x != (len(maze_contents[0]) - 1) and \
             maze_contents[y][x+1] != ' ':  # check if we can go right
            direction = 'E'
        else:  # otherwise turn around
            direction = 'S'
    
    elif direction == 'E':  # current direction is east
        if y != 0 and maze_contents[y-1][x] != ' ':  # check for left turn
            direction = 'N'
        elif x != (len(maze_contents[0]) - 1) and \
             maze_contents[y][x+1] != ' ':  # check for straight path
            direction = 'E'
        elif y != (len(maze_contents) - 1) and \
             maze_contents[y+1][x] != ' ':  # check if we can go right
            direction = 'S'
        else:  # otherwise turn around
            direction = 'W'
    
    elif direction == 'S':  # current direction is south
        if x != (len(maze_contents[0]) - 1) and \
           maze_contents[y][x+1] != ' ':  # check for left turn
            direction = 'E'
        elif y != (len(maze_contents) - 1)  and \
             maze_contents[y+1][x] != ' ':  # check for straight path
            direction = 'S'
        elif x != 0 and maze_contents[y][x-1] != ' ':  # check for right path
            direction = 'W'
        else:  # otherwise turn around
            direction = 'N'
    
    elif direction == 'W':  # current direction is west
        if y != (len(maze_contents) - 1) and maze_contents[y+1][x] != ' ': 
            # check if we can turn left
            direction = 'S'
        elif x != 0 and maze_contents[y][x-1] != ' ':  # check straight path
            direction = 'W'
        elif y != 0 and maze_contents[y-1][x] != ' ':  # check for right path
            direction = 'N'
        else:  # otherwise turn around
            direction = 'E'
    
    # reflect new direction on the array/map
    if direction == 'N':
        maze_contents[y][x] = '^'
    elif direction == 'E':
        maze_contents[y][x] = '>'
    elif direction == 'S':
        maze_contents[y][x] = 'v'
    else:
        maze_contents[y][x] = '<'
    
    return x, y, direction

def print_maze(maze_contents):
    '''
    This function prints the maze, with the arrow indicating the current 
    player position and '.' indicating where the position has already been.
    Arguments: maze_contents is a 2D-array containing the contents of the maze
    Return: None
    Assumptions: None
    '''
    for row in maze_contents:
        for char in row:
            print(char, end='')  # prints each character, end with nothing
        print('\n', end='')  # print new line after each row finished

def main():
    '''
    This calls the read file function to read the contents of a file and 
    then calls the solve maze function to solve the maze
    Arguments: None
    Return: None
    Assumptions: None
    '''
    maze, line_length = read_file()
    # loop though maze and make sure all lines are the same length, 
    # if not append ' ' till they are
    for row in maze:
        while len(row) != max(line_length):
            row.append(' ')

    solve_maze(maze)

main()