'''
File: railyard.py
Author: Cole Suddarth
Purpose: To create a game simulating a railyard. This game opens a user file,
    and asks user for commands in order to play the game, printing out the
    railyard at each step.
Course: CSC120 Summer21
'''

class ListNode:
    # !!taken directly from Russ' ListNode class!!
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        vals = []
        objs = set()
        curr = self
        while curr is not None:
            curr_str = str(curr.val)
            if curr in objs:
                vals.append("{} -> ... (to infinity and beyond)".format(curr_str))
                break
            else:
                vals.append(curr_str)
                objs.add(curr)
            curr = curr.next
        return " -> ".join(vals)

def read_file(file):
    '''
    Reads the file containing the tracks and the cars/locomotives
    into linked lists, such that each linked list represents a track
    and creates an array containing the heads of each track
    Arguments: file is the contents of a file, following track creation
    Return: header_array which contains the headers for each track
        length_array which contains each tracks car-length(num of cars\locos)
        track_lengths array containg length of each track(not including '-'
        at begining and end)
    Assumptions: File has the contents in a way that follows spec
    '''
    header_array = []
    length_array = []
    track_lengths = []
    for line in file:
        line = line.lstrip().rstrip()
        track_lengths.append(len(line) - 2)
        i = -2  # start at second from last in line
        head = None

        while line[i] != '-':  # while not end of cars
            # if not header create one of type ListNode
            if head is None:
                head = ListNode(line[i])
                cur = head
            # if header exists, the next points to a newly created node
            else:
                cur.next = ListNode(line[i])
                cur = cur.next
            i -= 1

        cur.next = None  # ends linked list
        length_array.append(calc_track_car_length(head))
        header_array.append(head)
    return header_array, length_array, track_lengths

def calc_track_car_length(head):
    '''
    Calculates the length of the cars/locos of a track
    Arguments: head is the head pointer of a linked list, representing cars
    Return: length is an integer representing length of cars
    Assumptions: head is a start of linked list, if head==None, no length
    '''
    cur = head
    length = 0
    while cur is not None:
        cur = cur.next
        length += 1
    return length

def count_locos(header_array):
    '''
    Counts the number of locomotives still in the railyard
    Arguments: header_array, array of heads representing linked list of tracks
    Return: count is an integer representing the number of locomotives
    Assumptions: a locomotive is represented by a 'T'
    '''
    count = 0
    for head in header_array:
        # loops through each head in the array
        if head is not None and head.val == 'T':
            # checks if the head exists and if it is a 'T' and increments
            count += 1
    return count

def count_destinations(header_array):
    '''
    Counts the number of destinations that are on the railyard
    Arguments: header_array, array of heads representing linked list of tracks
    Returns: integer representing the number of destinations remaining
    Assumptions: 'T', locomotive not counted as a destination
    '''
    destinations = set()
    for head in header_array:
        cur = head
        while cur is not None:
            if cur.val not in destinations:
                destinations.add(cur.val)
            cur = cur.next
        if 'T' in destinations:
            destinations.remove('T')
    return len(destinations)

def print_track(header_array, length_array, track_lengths):
    '''
    Prints the railyard and each track with its cars
    Arguments: header_array, array of heads representing linked list of tracks
        length_array which contains each tracks car-length(num of cars\locos)
        track_lengths array containg length of each track(not including '-'
        at begining and end)
    Returns: None, but prints out railyard
    Assumptions: An empty spot on the track is represented by a '-'
    '''
    for i in range(len(header_array)):
        print(i + 1, ':', '-' + '-' * (track_lengths[i] - length_array[i]),
              end='')
        # prints dashes leading toward end of list
        cur = header_array[i]
        printed_string = ''
        while cur is not None:
            # create a string using the values from linked list
            printed_string += cur.val
            cur = cur.next
        print(printed_string[::-1], end='')  # print string in reverse
        print('-')  # ending dash that always is on right side

def error_checking(command, header_array, length_array, track_lengths):
    '''
    Checks for the errors which may come from a command
    Arguments: command is an array of length 4
        header_array, array of heads representing linked list of tracks
        length_array which contains each tracks car-length(num of cars\locos)
        track_lengths array containg length of each track(not including '-'
        at begining and end)
    Return: False if there is no errors, true if there is an error
    Assumptions: None
    '''
    # checks if command input is in valid format
    if len(command) != 4 or command[0] != 'move':
        print("ERROR: The only valid command formats are (where each X \
represents an integer):\nmove X X X\nquit\n")
        return True
    # checks if count part of command can be converted to an integer
    try:
        temp = int(command[1])
    except ValueError:
        print(f"ERROR: Could not convert the 'count' value to an integer:\
 '{command[1]}'\n")
        return True
    # checks if from-track can be converted to an integer
    try:
        temp = int(command[2])
    except ValueError:
        print(f"ERROR: Could not convert the 'from-track' value to an integer:\
 '{command[2]}'\n")
        return True
    # checks if to-track can be converted to an integer
    try:
        temp = int(command[3])
    except ValueError:
        print(f"ERROR: Could not convert the 'to-track' value to an integer:\
 '{command[3]}'\n")
        return True
    # checks if to and from track are valid/in range
    if int(command[2]) < 1 or int(command[3]) < 1 or int(command[2]) >\
       len(header_array) or int(command[3]) > len(header_array):
        print(f"\nERROR: The to-track or from-track number is invalid.")
        return True
    # check if moving cars have a locomotive
    if header_array[int(command[2]) - 1] is not None and \
       header_array[int(command[2])-1].val != 'T':
        print(f"ERROR: Cannot move from track {command[2]} because it \
doesn't have a locomotive.")
        return True
    # check if destination track already has a locomotive
    if header_array[int(command[3]) - 1] is not None and \
       header_array[int(command[3])-1].val == 'T':
        print(f"ERROR: Cannot move to track {command[3]} because it already \
has a locomotive.")
        return True
    # check if there is enough cars to move on moving track
    if int(command[1]) > (calc_track_car_length(header_array[
       int(command[2])-1])-1):
        print(f"ERROR: Cannot move {command[1]} cars from track {command[2]} \
because it doesn't have that many cars.")
        return True
    # check if there is enough room to move cars to destination track
    if int(command[1]) + calc_track_car_length(header_array[
       int(command[3])-1]) > (track_lengths[int(command[3])-1] - 1):
        print(f"ERROR: Cannot move {command[1]} cars to track {command[3]} \
because it doesn't have enough space.")
        return True
    return False

def preform_command(command, header_array, length_array, track_lengths):
    '''
    Performs a command, by first checking if it is valid, if it is not returns.
    If valid adjusts the linked lists, and arrays to accurately depict the move
    Arguments: command, is an array such like so ['move', '', '0', '0', '0']
        header_array, array of heads representing linked list of tracks
        length_array which contains each tracks car-length(num of cars\locos)
        track_lengths array containg length of each track(not including '-'
        at begining and end)
    Return: Returns if an error is found in the command
    Assumptions: command has two spaces between move and <count>
    '''
    # command = move  <count> <from> <to>
    i = 0
    command.pop(1)  # removes extra space in move
    # if an error is found, return
    if error_checking(command, header_array, length_array, track_lengths):
        return

    cur = header_array[int(command[2])-1]
    while i < int(command[1]):  # loco not in count
        cur = cur.next
        i += 1
    new_from_head = cur.next  # temp of new header of train being taken from
    cur.next = header_array[int(command[3]) - 1]
    # end of moved train attached to beginning of <to> train
    header_array[int(command[3])-1] = header_array[int(command[2])-1]
    # <to> train head becomes <from> head
    header_array[int(command[2])-1] = new_from_head
    # <from> head becomes temp new_from_head

    # calculate lengths again
    length_array[int(command[2])-1] = length_array[int(command[2])-1]\
        - int(command[1]) - 1
    length_array[int(command[3])-1] = length_array[int(command[3])-1]\
        + int(command[1]) + 1

    print(f"\nThe locomotive on track {command[2]} moved {command[1]} cars to track \
{command[3]}.\n")

def check_track(track_number, track_heads):
    '''
    Checks if train on track can depart
    Arguments: track_number is an integer greater than 0
        track_heads is an array of heads of linked list for tracks
    Returns: True if all cars following locomotive are same val
        False if no locomotive, or not all same value
    Assumptions: Cars follow ListNode class
    '''
    if track_heads[track_number - 1] is None or \
       track_heads[track_number - 1].next is None:
        return False
    cur = track_heads[track_number - 1].next
    # cur is the first car not including locomotive
    previous = cur  # previous is the first car
    while cur is not None:
        if cur.val != previous.val:
            return False
        previous = cur
        cur = cur.next
    return True

def leaving_station(command, header_array, length_array):
    '''
    Determines the destination of leaving cars, and prints that they
    are leaving. Adjusts the header and length array to account for
    the leaving cars, and checks if the last locomotive has left and
    prints that there is no more remaining
    Arguments: command, is an array such like so ['move', '', '0', '0', '0']
        header_array, array of heads representing linked list of tracks
        length_array which contains each tracks car-length(num of cars\locos)
    Return: None
    Assumptions: Only called when a track can have cars depart
    '''
    # if track can leave determines destination, says its leaving
    destination = header_array[int(command[3]) - 1].next.val
    print(f"*** ALERT***  The train on track {command[3]}, which had \
{length_array[int(command[3])-1] - 1} cars, departs for destination \
{destination}.\n")
    # adjusts the header and length array to reflect change
    header_array[int(command[3]) - 1] = None
    length_array[int(command[3]) - 1] = 0
    if count_locos(header_array) == 0:
        # if no more locomotives prints no more locomotives
        print('The last locomotive has departed!\n')

def main():
    '''
    Asks user for a file, opens it and then prints out the initial
    track and initial locomtives and destinations. Then loops till
    'quit' is entered or no more locomotives in car asking user
    for a command.
    Returns: returns if quit is entered stopping program
    '''
    print('Please give the yard file:')
    file_name = input()
    try:
        file = open(file_name)
    except FileNotFoundError:
        print('File not found')
        return

    header_array, length_array, track_lengths = read_file(file)
    print_track(header_array, length_array, track_lengths)
    print('Locomotive count:', str(count_locos(header_array)))
    print('Destination count:', str(count_destinations(header_array)))
    print()

    while count_locos(header_array) > 0:
        print('What is your next command?')
        command = input()
        command = command.lstrip().rstrip()
        command = command.split(' ')
        if command == ['quit']:
            print('Quitting!')
            return
        preform_command(command, header_array, length_array, track_lengths)
        print_track(header_array, length_array, track_lengths)
        if len(command) > 3 and command[3].isnumeric():
            # only runs when command has enough length to prevent crashing
            if check_track(int(command[3]), header_array):
                # if track can leave determines destination, says its leaving
                leaving_station(command, header_array, length_array)
                print_track(header_array, length_array, track_lengths)
        print('Locomotive count:', str(count_locos(header_array)))
        print('Destination count:', str(count_destinations(header_array)))
        print()

main()