import sys
import board

def main():
    testBoard = board.Board([[1,2,3,4],[5,6,7,8],[9,10,11,0]])
    print(testBoard)
    
    next_moves = testBoard.get_moves()
    print(next_moves)
    
    children = testBoard.get_children()
    for child in children:
        print(child[0])
        print(child[1])
        print(child[1].get_children())
    

if __name__ == "__main__":
    main()