# Skeleton Program for the AQA A1 Summer 2019 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 environment

# Version number: 0.1.3


# - Constants and stuff
SPACE = '     '
UNUSED = 'XXXXX'

BOARD_SIZE = 8
NUMBER_OF_PIECES = 12
MAX_MOVES = 50
ROW = 0
COLUMN = 1
DAME = 2


class MoveRecord:
    def __init__(self):  # - Assigns attributes to an object (each piece) in ListPossibleMoves
        self.Piece = ''
        self.NewRow = -1
        self.NewColumn = -1
        self.CanJump = False


def LoadPieces(FileHandle, PlayersPieces):
    for Index in range(NUMBER_OF_PIECES + 1):
        PlayersPieces[Index][ROW] = int(FileHandle.readline())  # - Reads first number in sequence to be number
        # of moves then after first iteration reads to be row and adds to PlayerPieces
        PlayersPieces[Index][COLUMN] = int(FileHandle.readline())  # - Reads second number in sequence to be
        # number of dames then after first iteration reads to be column and adds to PlayerPieces
        PlayersPieces[Index][DAME] = int(FileHandle.readline())  # - Reads third number to be unused then after first
        # iteration reads to be dame status and adds to PlayerPieces list
    return PlayersPieces  # - Returns back into SetUpBoard


def CreateNewBoard(Board):
    for ThisRow in range(BOARD_SIZE):
        for ThisColumn in range(BOARD_SIZE):
            if (ThisRow + ThisColumn) % 2 == 0:
                Board[ThisRow][ThisColumn] = UNUSED  # - Places unused using this rule
            else:
                Board[ThisRow][ThisColumn] = SPACE  # - Places spaces if not unused
    return Board


def AddPlayerA(Board, A):
    for Index in range(1, NUMBER_OF_PIECES + 1):  # - Starts at 1 to jump stats index
        PieceRow = A[Index][ROW]  # - Extracts piece row from list A
        PieceColumn = A[Index][COLUMN]  # - Extracts piece column from list A
        PieceDame = A[Index][DAME]  # - Extracts dame status from list A
        if PieceRow > -1:  # - Adds if piece is in play
            if PieceDame == 1:
                Board[PieceRow][PieceColumn] = 'A' + str(Index)  # - Capitalises if piece is a Dame
            else:
                Board[PieceRow][PieceColumn] = 'a' + str(Index)  # - Else a regular piece
    return Board


def AddPlayerB(Board, B):
    for Index in range(1, NUMBER_OF_PIECES + 1):  # - Starts at 1 to jump stats index
        PieceRow = B[Index][ROW]  # - Extracts piece row from list A
        PieceColumn = B[Index][COLUMN]  # - Extracts piece column from list A
        PieceDame = B[Index][DAME]  # - Extracts dame status from list A
        if PieceRow > -1:
            if PieceDame == 1:
                Board[PieceRow][PieceColumn] = 'B' + str(Index)  # - Capitalises if piece is a Dame
            else:
                Board[PieceRow][PieceColumn] = 'b' + str(Index)  # - Else a regular piece
    return Board


def DisplayErrorCode(ErrorNumber):
    print('Error ', ErrorNumber)


def SetUpBoard(Board, A, B, FileFound):
    FileName = 'game1.txt'  # - Game that is loaded at default
    Answer = input('Do you want to load a saved game? (Y/N): ')  # - Prompts user to load saved game
    if Answer == 'Y' or Answer == 'y':
        FileName = input('Enter the filename: ')  # - Prompts user to enter name of saved game
    try:
        FileHandle = open(FileName, 'r')  # - Opens file in read mode (goes to exception if it cannot be opened)
        FileFound = True  # - Boolean value if file can be opened
        A = LoadPieces(FileHandle, A)  # - Loads Player A pieces from File
        B = LoadPieces(FileHandle, B)  # - Loads Player B pieces from File
        FileHandle.close()  # - Closes File
        Board = CreateNewBoard(Board)  # - Fills board with unused spaces and empty spaces
        Board = AddPlayerA(Board, A)  # - Places Player A's pieces on board
        Board = AddPlayerB(Board, B)  # - Places Player B's pieces on board
    except:
        DisplayErrorCode(4)  # - If the file does not exist, this procedure is called
    return Board, A, B, FileFound


def PrintHeading():
    print('    ', end='')
    for BoardColumn in range(BOARD_SIZE):
        print('{0:3}'.format(BoardColumn), end='   ')  # - Places numbers up to 7, formatted to be within 3 spaces
    print()


def PrintRow(Board, ThisRow):
    print('   |', end='')
    for BoardColumn in range(BOARD_SIZE):  # -  0 to 7
        if Board[ThisRow][BoardColumn] == UNUSED:
            print(Board[ThisRow][BoardColumn], end='|')  # - Puts unused if unused
        else:
            print(SPACE, end='|')  # - Puts space if space
    print()


def PrintMiddleRow(Board, ThisRow):
    print('{0:>2}'.format(ThisRow), end=' |')  # - Centers the row number to right of two spaces with an end statement
    for BoardColumn in range(BOARD_SIZE):
        if Board[ThisRow][BoardColumn] == UNUSED or Board[ThisRow][BoardColumn] == SPACE:
            print(Board[ThisRow][BoardColumn], end='|')  # - If a piece is not there, this end is printed this way
        else:
            print('{0:>4}'.format(Board[ThisRow][BoardColumn]), end=' |')  # - Else the piece is centered in the
            # right of 4 spaces
    print()


def PrintLine():
    print('   ', end='')
    for BoardColumn in range(BOARD_SIZE):
        print('------', end='')  # - Once end is reached, prints dashes 7 times
    print('-')


def DisplayBoard(Board):
    PrintHeading()  # Prints numbers 1 to 7
    PrintLine()  # - Prints dashes
    for ThisRow in range(BOARD_SIZE):  # - 0 to 7
        PrintRow(Board, ThisRow)  # - Deals with unused and used spaces on top
        PrintMiddleRow(Board, ThisRow)  # - Puts piece if present or does same thing as print row
        PrintRow(Board, ThisRow)  # - Deals with unused and used spaces on top
        PrintLine()  # - Prints dashes


def PrintPlayerPieces(A, B):
    print()
    print('Player A:')
    print(A)
    print('Player B:')
    print(B)
    print()


def ClearList(ListOfMoves):
    for Index in range(MAX_MOVES):
        ListOfMoves[Index].Piece = ''
        ListOfMoves[Index].NewRow = -1
        ListOfMoves[Index].NewColumn = -1
        ListOfMoves[Index].CanJump = False
    return ListOfMoves


def ValidMove(Board, NewRow, NewColumn):
    Valid = False
    if NewRow in range(BOARD_SIZE) and NewColumn in range(BOARD_SIZE):  # Checks if position exists in board
        if Board[NewRow][NewColumn] == SPACE:
            Valid = True  # - If move location is a space then it is valid
    return Valid


def ValidJump(Board, PlayersPieces, Piece, NewRow, NewColumn):
    Valid = False
    MiddlePiece = ''
    Player = Piece[0].lower()
    Index = int(Piece[1:])  # - Strips first piece number
    if Player == 'a':
        OppositePiecePlayer = 'b'
    else:
        OppositePiecePlayer = 'a'
    if NewRow in range(BOARD_SIZE) and NewColumn in range(BOARD_SIZE):  # - Checks if position is in board
        if Board[NewRow][NewColumn] == SPACE:  # - Checks if position is empty
            CurrentRow = PlayersPieces[Index][ROW]  # - Takes index from piece and fetches its row on the board
            CurrentColumn = PlayersPieces[Index][COLUMN]  # - Takes index from piece and fetches its column on the board
            MiddlePieceRow = (CurrentRow + NewRow) // 2  # - Averages rows to get middle row
            MiddlePieceColumn = (CurrentColumn + NewColumn) // 2  # - Averages columns to get middle column
            MiddlePiece = Board[MiddlePieceRow][MiddlePieceColumn]  # - Fetches the piece located at these coordinates
            MiddlePiecePlayer = MiddlePiece[0].lower()  # - Sets up for comparison
            if MiddlePiecePlayer != OppositePiecePlayer and MiddlePiecePlayer != ' ':  # -  If the middle piece does
                # not belong to the opposition and it is not a space then it is valid
                Valid = True
    return Valid


def ListPossibleMoves(Board, PlayersPieces, NextPlayer, ListOfMoves):
    if NextPlayer == 'a':
        Direction = 1  # - Sets direction based on player
    else:
        Direction = -1
    NumberOfMoves = 0  # - Counter
    for i in range(1, NUMBER_OF_PIECES + 1):  # - Loops through each piece
        Piece = NextPlayer + str(i)  # - Sets piece based on i
        CurrentRow = PlayersPieces[i][ROW]  # - Fetches row of piece
        CurrentColumn = PlayersPieces[i][COLUMN]  # - Fetches column of piece
        if PlayersPieces[i][DAME] == 1:
            Piece = Piece.upper()  # - Capitalises if piece is a dame
        NewRow = CurrentRow + Direction  # - Finds new possible row of piece
        LeftColumn = CurrentColumn - 1  # - Finds new possible left column
        RightColumn = CurrentColumn + 1  # - Finds new possible right column
        if ValidMove(Board, NewRow, LeftColumn):  # - Checks if the left column move is a space or exists on board
            print(Piece, ' can move to ', NewRow, ' , ', LeftColumn)
            NumberOfMoves += 1  # - Updates counter
            ListOfMoves[NumberOfMoves].Piece = Piece  # - Adds piece for this move
            ListOfMoves[NumberOfMoves].NewRow = NewRow  # - Adds row for this move
            ListOfMoves[NumberOfMoves].NewColumn = LeftColumn  # - Adds column for this move
            ListOfMoves[NumberOfMoves].CanJump = False  # - Adds jump status (unable)
        if ValidMove(Board, NewRow, RightColumn):  # - Checks if the right column move is a space or exists on board
            print(Piece, ' can move to ', NewRow, ' , ', RightColumn)
            NumberOfMoves += 1  # - Updates counter
            ListOfMoves[NumberOfMoves].Piece = Piece  # - Adds piece for this move
            ListOfMoves[NumberOfMoves].NewRow = NewRow  # - Adds row for this move
            ListOfMoves[NumberOfMoves].NewColumn = RightColumn  # - Adds column for this move
            ListOfMoves[NumberOfMoves].CanJump = False  # - Adds jump status (unable)
        JumpRow = CurrentRow + Direction + Direction  # - Sets jump row, two rows ahead in relative direction
        JumpLeftColumn = CurrentColumn - 2  # - Sets jump column, two columns to the left
        JumpRightColumn = CurrentColumn + 2  # - Sets jump column, two columns to the right
        if ValidJump(Board, PlayersPieces, Piece, JumpRow, JumpLeftColumn):  # - Checks if the jump can be made on
            # left column
            print(Piece, ' can jump to ', JumpRow, ' , ', JumpLeftColumn)
            NumberOfMoves += 1  # - Updates counter
            ListOfMoves[NumberOfMoves].Piece = Piece  # - Adds piece for this jump
            ListOfMoves[NumberOfMoves].NewRow = JumpRow  # - Adds row for this jump
            ListOfMoves[NumberOfMoves].NewColumn = JumpLeftColumn  # - Adds column for this jump
            ListOfMoves[NumberOfMoves].CanJump = True  # - Adds jump status (able)
        if ValidJump(Board, PlayersPieces, Piece, JumpRow, JumpRightColumn):  # - Checks if the jump can be made on
            # right column
            print(Piece, ' can jump to ', JumpRow, ' , ', JumpRightColumn)
            NumberOfMoves += 1  # - Updates counter
            ListOfMoves[NumberOfMoves].Piece = Piece  # - Adds piece for this jump
            ListOfMoves[NumberOfMoves].NewRow = JumpRow  # - Adds row for this jump
            ListOfMoves[NumberOfMoves].NewColumn = JumpRightColumn  # - Adds column for this jump
            ListOfMoves[NumberOfMoves].CanJump = True  # - Adds jump status (able)
    print('There are ', NumberOfMoves, ' possible moves')
    return ListOfMoves


def ListEmpty(ListOfMoves):
    if ListOfMoves[1].Piece == '':  # - Checks if first possible move has been entered
        return True
    else:
        return False


def SelectMove(ListOfMoves):
    ValidPiece = False
    while not ValidPiece:
        Found = False
        EndOfList = False
        Piece = input('Which piece do you want to move? ')  # - Prompts user which piece to move
        Index = 0  # - Used as counter
        if Piece == '':  # - Checks if nothing was entered
            EndOfList = True
        while not Found and not EndOfList:
            print(Index)
            Index += 1
            if ListOfMoves[Index].Piece == Piece:  # - Loops through list of moves to find if it has a possible move
                Found = True
            elif ListOfMoves[Index].Piece == '':  # - Checks if at end of list of moves to determine it does not have
                # a possible move
                EndOfList = True
                DisplayErrorCode(1)  # - Piece cannot move
        if Found:
            ValidPiece = True
    ChosenPieceIndex = Index
    ValidMove = False
    while not ValidMove:
        RowString = input('Which row do you want to move to? ')  # - Prompts to enter row
        ColumnString = input('Which column do you want to move to? ')  # - Prompts to enter column
        try:
            NewRow = int(RowString)  # - Converts row to integer
            NewColumn = int(ColumnString)  # Converts column to integer
            Found = False
            EndOfList = False
            Index = ChosenPieceIndex - 1  # Sets new range within list of moves (first occurrence of piece to end)
            while not Found and not EndOfList:
                Index += 1  # - Used as counter
                if ListOfMoves[Index].Piece != Piece:  # - Finds end of last occurrence of piece (Piece moves are next
                    # to each other) to determine the move is not possible
                    EndOfList = True
                    DisplayErrorCode(2)  # - Piece is found but invalid move
                elif ListOfMoves[Index].NewRow == NewRow and ListOfMoves[Index].NewColumn == NewColumn:  # - Confirms
                    # coordinates to make selection valid
                    Found = True
            ValidMove = Found
        except:
            DisplayErrorCode(3)  # - Triggered if row and column prompts are not integers
    return Index


def MoveDame(Board, Player, NewRow, NewColumn):
    if Player == 'a':
        for i in [1, 3, 5, 7]:  # - Checks positions on board with spaces on it (when set up)
            if Board[0][i] == SPACE:  # - Checks if it is a space
                NewColumn = i  # - Sets new column
                NewRow = 0  # - Sets to beginning of board
                break
    else:
        for i in [0, 2, 4, 6]:  # - Checks positions on board with spaces on it (when set up)
            if Board[BOARD_SIZE - 1][i] == SPACE:  # - Checks if it is a space
                NewColumn = i  # - Sets new column
                NewRow = BOARD_SIZE - 1  # - Sets to end of board
                break
    return NewRow, NewColumn


def MovePiece(Board, PlayersPieces, ChosenPiece, NewRow, NewColumn):
    Index = int(ChosenPiece[1:])  # -  Strips for the piece number
    CurrentRow = PlayersPieces[Index][ROW]  # - Fetches the row from player pieces
    CurrentColumn = PlayersPieces[Index][COLUMN]  # - Fetches the column from player pieces
    Board[CurrentRow][CurrentColumn] = SPACE  # - Changes the position of the piece to a space

    if NewRow == BOARD_SIZE - 1 and PlayersPieces[Index][DAME] == 0:  # - Checks if piece is at the end of of the
        # board to make it a dame
        Player = 'a'
        PlayersPieces[0][1] += 1  # - Adds one to number of dames in stats
        PlayersPieces[Index][DAME] = 1  # - Updates dame status on piece
        ChosenPiece = ChosenPiece.upper()  # - Capitalises piece
        NewRow, NewColumn = MoveDame(Board, Player, NewRow, NewColumn)
    elif NewRow == 0 and PlayersPieces[Index][DAME] == 0:  # - Checks if piece is at the end of of the
        # board to make it a dame
        Player = 'b'
        PlayersPieces[0][1] += 1  # - Adds one to number of dames in stats
        PlayersPieces[Index][DAME] = 1  # - Updates dame status on piece
        ChosenPiece = ChosenPiece.upper()  # - Capitalises piece
        NewRow, NewColumn = MoveDame(Board, Player, NewRow, NewColumn)  # - Moves dame back to start of board
    PlayersPieces[Index][ROW] = NewRow  # - Puts the piece in the new row
    PlayersPieces[Index][COLUMN] = NewColumn  # - Puts the piece in the new column
    Board[NewRow][NewColumn] = ChosenPiece  # - Puts piece in new position on board
    return Board, PlayersPieces


def MakeMove(Board, PlayersPieces, OpponentsPieces, ListOfMoves, PieceIndex):
    PlayersPieces[0][0] += 1  # - Adds to number of moves in stats
    if PieceIndex > 0:
        Piece = ListOfMoves[PieceIndex].Piece  # - Fetches the piece of the selected move index
        NewRow = ListOfMoves[PieceIndex].NewRow  # - Fetches the row of the selected move index
        NewColumn = ListOfMoves[PieceIndex].NewColumn  # - Fetches the column of the selected move index
        PlayersPieceIndex = int(Piece[1:])  # - Strips to get piece number
        CurrentRow = PlayersPieces[PlayersPieceIndex][ROW]  # - Fetches the current row of piece
        CurrentColumn = PlayersPieces[PlayersPieceIndex][COLUMN]  # - Fetches the current column of piece
        Jumping = ListOfMoves[PieceIndex].CanJump  # - Checks if the piece can jump
        Board, PlayersPieces = MovePiece(Board, PlayersPieces, Piece, NewRow, NewColumn)  # - Manipulates board to
        # move pieces
        if Jumping:
            MiddlePieceRow = (CurrentRow + NewRow) // 2  # - Averages rows to find the middle row
            MiddlePieceColumn = (CurrentColumn + NewColumn) // 2  # - Averages columns to find the middle column
            MiddlePiece = Board[MiddlePieceRow][MiddlePieceColumn]  # - Fetches the piece from the board
            print('jumped over ', MiddlePiece)
    return Board, PlayersPieces, OpponentsPieces


def SwapPlayer(NextPlayer):
    if NextPlayer == 'a':
        return 'b'
    else:
        return 'a'


def PrintResult(A, B, NextPlayer):
    print('Game ended')
    print(NextPlayer, ' lost this game as they cannot make a move')  # - Chooses current player to win
    PrintPlayerPieces(A, B)


def Game():
    A = [[0, 0, 0] for Piece in range(NUMBER_OF_PIECES + 1)]  # - Creates 3 element lists for Player A's statistics
    # [Number of Moves. Number of Dames, Empty] and each piece [Dame status, Row, Column]
    B = [[0, 0, 0] for Piece in range(NUMBER_OF_PIECES + 1)]  # - Creates 3 element lists for Player B's statistics
    # [Number of Moves. Number of Dames, Empty] and each piece [Dame status, Row, Column]
    Board = [['' for Column in range(BOARD_SIZE)] for Row in
             range(BOARD_SIZE)]  # - Creates board out of row and columns
    ListOfMoves = [MoveRecord() for Move in range(MAX_MOVES)]  # - Creates lists for moves 50 times
    GameEnd = False  # - Boolean value for end of game
    FileFound = False  # - Boolean value for file found
    NextPlayer = 'a'  # - Starts game with player A by default
    Board, A, B, FileFound = SetUpBoard(Board, A, B, FileFound)  # - Loads game if existing and loads pieces onto Board
    if not FileFound:
        GameEnd = True
    while not GameEnd:
        PrintPlayerPieces(A, B)  # - Prints Player A's and Player B's stats and pieces
        DisplayBoard(Board)  # - Prints board by places items from Board with formatting
        print('Next Player: ', NextPlayer)  # - States next player
        ListOfMoves = ClearList(ListOfMoves)  # - Clears list of ListOfMoves from previous move
        if NextPlayer == 'a':
            ListOfMoves = ListPossibleMoves(Board, A, NextPlayer, ListOfMoves)  # - Generates all the possible moves
            # each piece can make
            if not ListEmpty(ListOfMoves):  # - Checks if a move can be made
                PieceIndex = SelectMove(ListOfMoves)  # - Validates and chooses move
                Board, A, B = MakeMove(Board, A, B, ListOfMoves, PieceIndex)  # - Moves the piece to selected move
                NextPlayer = SwapPlayer(NextPlayer)  # - Swaps player for next turn
            else:
                GameEnd = True  # If no list of moves is empty, the end of the game is reached
        else:
            ListOfMoves = ListPossibleMoves(Board, B, NextPlayer, ListOfMoves)  # - Checks if a move can be made
            if not ListEmpty(ListOfMoves):
                PieceIndex = SelectMove(ListOfMoves)  # - Validates and chooses move
                Board, B, A = MakeMove(Board, B, A, ListOfMoves, PieceIndex)  # - Moves the piece to selected move
                NextPlayer = SwapPlayer(NextPlayer)  # - Swaps player for next turn
            else:
                GameEnd = True  # If no list of moves is empty, the end of the game is reached
    if FileFound:
        PrintResult(A, B, NextPlayer)


if __name__ == "__main__":  # - Makes the game executable only when it is run independently
    Game()
