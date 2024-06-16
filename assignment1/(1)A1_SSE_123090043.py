import random
from random import choice


def intro():
    # introduction of this game
    print("Welcome to Kinley’s puzzle game, you will be prompted: ")
    print("The Kinley’s puzzle game is a classic puzzle that consists of a 3x3 grid with eight\
numbered square tiles and an empty space. ")
    print("You need to sliding one adjacent tile into the empty space until all numbers appear sequentially,\
ordered from left to right and top to bottom.")


def enter_letters(moves,move_representation):
    movesinput=input("Enter the four letters used for left, right, up and down move:")
    count=0
    moveset=[[0,1],[0,-1],[1,0],[-1,0]]
    # check if the input is vaild.Repeated letters,too many or too few letters, non-letter characters are invaild.
    for i in movesinput:
        if i.isalpha():
            if i.upper() not in moves and i.lower() not in moves:
                moves[i]=moveset[count]
                move_representation.append(i)#arrow directions are determined by the entered letters.
                count+=1
    if count<4:  #tackle invalid input
        print("invalid input, please try again!")
        return False
    else:
        return True


def generate_new_puzzle():
    while True:
        puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # 生成新的游戏拼图
        random.shuffle(puzzle)  # 随机打乱拼图
        if is_solvable(puzzle):  # 检查拼图是否可解
            return puzzle


def is_solvable(puzzle):
    count = 0
    for i in range(0, 9):
        for j in range(i+1, 9):
            if puzzle[i] > puzzle[j]:
                count += 1
    return count % 2 == 0  # 如果逆序数为偶数，则拼图可解，否则不可解

def print_puzzle(puzzle):
    # print the checkerboard
    for i in  range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j]!=0:
                print(puzzle[i][j],end=" ")
            else:
                print(" ",end=" ")
        print()
    print()


def person_input(puzzle,moves,empty,move_representation,new_empty):
    # let the user know what positions can he moves to.
    possilbe_solution = "Enter your move (left-" + move_representation[0] + ", right-" + move_representation[1] + \
                        ", up-" + move_representation[2] + ", down-" + move_representation[3] + ") >"
    # judge if the move can be done. If not, delete the move.
    if empty[1] == len(puzzle) - 1:
        possilbe_solution = possilbe_solution.replace("left-" + move_representation[0] + ", ", "")
    if empty[1] == 0:
        possilbe_solution = possilbe_solution.replace("right-" + move_representation[1] + ", ", "")
    if empty[0] == len(puzzle) - 1:
        possilbe_solution = possilbe_solution.replace("up-" + move_representation[2] + ", ", "")
    if empty[0] == 0:
        possilbe_solution = possilbe_solution.replace(", down-" + move_representation[3], "")
    solution = input(possilbe_solution)
    global flag
    try:
        if_valid=moves[solution]
    except:
        print("invalid input, please try again!")
        return False
    try:
        new_empty[0]= empty[0] + moves[solution][0]
        new_empty[1] = empty[1] + moves[solution][1]
    except:
        print("invalid input, please try again!")
        return False
    if new_empty[0]>2 or new_empty[0]<0 or new_empty[1]>2 or new_empty[1]<0:
        print("invalid input, please try again!")
        return False
    return True


def person_move(puzzle,empty,new_empty):
    # change the position of the number.
    puzzle[empty[0]][empty[1]] = puzzle[new_empty[0]][new_empty[1]]
    puzzle[new_empty[0]][new_empty[1]] = 0
    print_puzzle(puzzle)


def person_choice():
    #When the game finishes, let the player to choose whether start a new game or quite the game.
    person_choice=input("Enter “n” for another game, or “q” to end the game >")
    if person_choice=="n":
        main()
    elif person_choice=="q":
        return True
    else:
        print("invalid input, please try again!")
        return False


def check_win(puzzle):
    # generate the final checkerboard to compare with the current one.
    checking=[[0 for i in range(len(puzzle))] for j in range(len(puzzle[0]))]
    count=0
    for i in range(len(checking)):
        for j in range(len(checking[i])):
            count+=1
            checking[i][j]=count
    checking[len(puzzle)-1][len(puzzle[0])-1]=0
    if checking==puzzle:
        return True
    else:
        return False


def main():
    # introduction of this game
    intro()
    # let the user enter 4 letters representing 4 directions.
    #moves={}#connect the directions with the entered letters.
    #move_representation=[]
    flag1=False# The flag is used to indicate whether the player has entered the appropriate 4 letters.
    while flag1==False:# If the player entered the invalid letter(s), then they should enter again.
        moves = {}#connect the directions with the entered letters.
        move_representation = []#store the entered letters.
        flag1=enter_letters(moves,move_representation)
    #set the size of the puzzle
    originpuzzle=generate_new_puzzle()
    len_board=3
    puzzle = [[originpuzzle[i*len_board+j] for i in range(len_board)] for j in range(3)]
    print(puzzle)
    puzzle[len(puzzle)-1][len(puzzle[0])-1]=0# the initial space represented by zero is in the place of number nine
    empty = [len(puzzle)-1 for i in range(len(puzzle)-1)]# the position of the initial empty
    count=0#Total steps calculation
    # the process of the game
    while not check_win(puzzle):
        new_empty=[0,0]
        flag=False# The flag is used to indicate whether the player has entered the appropriate direction to move.
        while flag==False:# If the player entered the invalid directions or meaningless words, then they should enter again.
            new_empty = [0, 0]
            # let the user know what positions can he moves to.
            flag=person_input(puzzle,moves, empty, move_representation,new_empty)
        person_move(puzzle,empty,new_empty)
        count+=1
        empty[0] = new_empty[0]
        empty[1] = new_empty[1]
    # thus the puzzle is solved (distinguish sigular and plural cases).
    if count==1:
        print("Congratulations! You solved the puzzle in %d move!" % (count))
    else:
        print("Congratulations! You solved the puzzle in %d moves!"%(count))
    flag3=False
    while flag3==False:
        flag3=person_choice()
    return


#start the program
main()


