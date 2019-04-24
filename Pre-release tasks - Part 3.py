# Skeleton Program for the AQA A1 Summer 2019 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 environment

# Version number: 0.1.3
import os

SPACE = '     '
UNUSED = 'XXXXX'

BOARD_SIZE = 8
NUMBER_OF_PIECES = 12
MAX_MOVES = 50
ROW = 0
COLUMN = 1
DAME = 2


class MoveRecord:
    def __init__(self):
        self.Piece = ''
        self.NewRow = -1
        self.NewColumn = -1
        self.CanJump = False


def LoadPieces(FileHandle, PlayersPieces):
    for Index in range(NUMBER_OF_PIECES + 1):
        PlayersPieces[Index][ROW] = int(FileHandle.readline())
        PlayersPieces[Index][COLUMN] = int(FileHandle.readline())
        PlayersPieces[Index][DAME] = int(FileHandle.readline())
    return PlayersPieces


def CreateNewBoard(Board):
    for ThisRow in range(BOARD_SIZE):
        for ThisColumn in range(BOARD_SIZE):
            if (ThisRow + ThisColumn) % 2 == 0:
                Board[ThisRow][ThisColumn] = UNUSED
            else:
                Board[ThisRow][ThisColumn] = SPACE
    return Board


def AddPlayerA(Board, A):
    for Index in range(1, NUMBER_OF_PIECES + 1):
        PieceRow = A[Index][ROW]
        PieceColumn = A[Index][COLUMN]
        PieceDame = A[Index][DAME]
        if PieceRow > -1:
            if PieceDame == 1:
                Board[PieceRow][PieceColumn] = 'A' + str(Index)
            else:
                Board[PieceRow][PieceColumn] = 'a' + str(Index)
    return Board


def AddPlayerB(Board, B):
    for Index in range(1, NUMBER_OF_PIECES + 1):
        PieceRow = B[Index][ROW]
        PieceColumn = B[Index][COLUMN]
        PieceDame = B[Index][DAME]
        if PieceRow > -1:
            if PieceDame == 1:
                Board[PieceRow][PieceColumn] = 'B' + str(Index)
            else:
                Board[PieceRow][PieceColumn] = 'b' + str(Index)
    return Board


def DisplayErrorCode(ErrorNumber):
    print('Error ', ErrorNumber)


def SetUpBoard(Board, A, B, FileFound):
    FileName = 'game1.txt'
    Answer = input('Do you want to load a saved game? (Y/N): ')
    if Answer == 'Y' or Answer == 'y':
        FileName = input('Enter the filename: ')
    try:
        FileHandle = open(FileName, 'r')
        FileFound = True
        A = LoadPieces(FileHandle, A)
        B = LoadPieces(FileHandle, B)
        FileHandle.close()
        Board = CreateNewBoard(Board)
        Board = AddPlayerA(Board, A)
        Board = AddPlayerB(Board, B)
    except:
        DisplayErrorCode(4)
    return Board, A, B, FileFound


def PrintHeading():
    print('    ', end='')
    for BoardColumn in range(BOARD_SIZE):
        print('{0:3}'.format(BoardColumn), end='   ')
    print()


def PrintRow(Board, ThisRow):
    print('   |', end='')
    for BoardColumn in range(BOARD_SIZE):
        if Board[ThisRow][BoardColumn] == UNUSED:
            print(Board[ThisRow][BoardColumn], end='|')
        else:
            print(SPACE, end='|')
    print()


def PrintMiddleRow(Board, ThisRow):
    print('{0:>2}'.format(ThisRow), end=' |')
    for BoardColumn in range(BOARD_SIZE):
        if Board[ThisRow][BoardColumn] == UNUSED or Board[ThisRow][BoardColumn] == SPACE:
            print(Board[ThisRow][BoardColumn], end='|')
        else:
            print('{0:>4}'.format(Board[ThisRow][BoardColumn]), end=' |')
    print()


def PrintLine():
    print('   ', end='')
    for BoardColumn in range(BOARD_SIZE):
        print('------', end='')
    print('-')


def DisplayBoard(Board):
    PrintHeading()
    PrintLine()
    for ThisRow in range(BOARD_SIZE):
        PrintRow(Board, ThisRow)
        PrintMiddleRow(Board, ThisRow)
        PrintRow(Board, ThisRow)
        PrintLine()


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
    if NewRow in range(BOARD_SIZE) and NewColumn in range(BOARD_SIZE):
        if Board[NewRow][NewColumn] == SPACE:
            Valid = True
    return Valid


def ValidJump(Board, PlayersPieces, Piece, NewRow, NewColumn):
    Valid = False
    MiddlePiece = ''
    Player = Piece[0].lower()
    Index = int(Piece[1:])
    if Player == 'a':
        OppositePiecePlayer = 'b'
    else:
        OppositePiecePlayer = 'a'
    if NewRow in range(BOARD_SIZE) and NewColumn in range(BOARD_SIZE):
        if Board[NewRow][NewColumn] == SPACE:
            CurrentRow = PlayersPieces[Index][ROW]
            CurrentColumn = PlayersPieces[Index][COLUMN]
            MiddlePieceRow = (CurrentRow + NewRow) // 2
            MiddlePieceColumn = (CurrentColumn + NewColumn) // 2
            MiddlePiece = Board[MiddlePieceRow][MiddlePieceColumn]
            MiddlePiecePlayer = MiddlePiece[0].lower()
            if MiddlePiecePlayer != ' ' or MiddlePiecePlayer == OppositePiecePlayer:
                Valid = True
    return Valid


def ListPossibleMoves(Board, PlayersPieces, NextPlayer, ListOfMoves):
    if NextPlayer == 'a':
        Direction = 1
    else:
        Direction = -1
    NumberOfMoves = 0
    move = []  # new for storing moves instead of printing
    jump = []  # new for storing jumps instead of printing
    take = []  # new for storing takes instead of printing
    multiTakeLeft = []
    multiTakeRight = []
    for i in range(1, NUMBER_OF_PIECES + 1):
        Piece = NextPlayer + str(i)
        CurrentRow = PlayersPieces[i][ROW]
        CurrentColumn = PlayersPieces[i][COLUMN]
        if PlayersPieces[i][DAME] == 1:
            Piece = Piece.upper()
        NewRow = CurrentRow + Direction
        LeftColumn = CurrentColumn - 1
        RightColumn = CurrentColumn + 1

        if ValidMove(Board, NewRow, LeftColumn):
            move.append([Piece, NewRow, LeftColumn])  # new for adding moves to list
        if ValidMove(Board, NewRow, RightColumn):
            move.append([Piece, NewRow, RightColumn])  # new for adding moves to list

        JumpRow = CurrentRow + Direction + Direction
        JumpLeftColumn = CurrentColumn - 2
        JumpRightColumn = CurrentColumn + 2


        if ValidJump(Board, PlayersPieces, Piece, JumpRow, JumpLeftColumn):
            JumpedOver = Board[NewRow][LeftColumn]
            jump.append([Piece, JumpRow, JumpLeftColumn])
            if JumpedOver[0] != Piece[0]:
                take.append([Piece, JumpRow, JumpLeftColumn])
            while JumpedOver[0] != Piece[0] and ValidJump(Board, PlayersPieces, Piece, JumpRow + Direction,
                                                          JumpLeftColumn - 1):
                JumpRow += Direction
                JumpLeftColumn -= 1
                JumpedOver = Board[NewRow + Direction][JumpLeftColumn - 1]
                multiTakeLeft.append([Piece, JumpRow, JumpLeftColumn])

        if ValidJump(Board, PlayersPieces, Piece, JumpRow, JumpRightColumn):
            JumpedOver = Board[NewRow][RightColumn]
            jump.append([Piece, JumpRow, JumpRightColumn])
            if JumpedOver[0] != Piece[0]:
                take.append([Piece, JumpRow, JumpRightColumn])
                while JumpedOver[0] != Piece[0] and ValidJump(Board, PlayersPieces, Piece, JumpRow + Direction,
                                                              JumpRightColumn + 1):
                    JumpRow += Direction
                    JumpRightColumn += 1
                    JumpedOver = Board[NewRow + Direction][JumpRightColumn + 1]
                    multiTakeRight.append([Piece, JumpRow, JumpRightColumn])

    if len(take) > 0 or len(multiTakeLeft) > 0 or len(multiTakeRight) > 0:  # new check to see if any takes
        for each in take:  # new loop through takes
            NumberOfMoves += 1
            print(each[0], ' can take and move to ', each[1], ' , ', each[2])
            ListOfMoves[NumberOfMoves].Piece = each[0]
            ListOfMoves[NumberOfMoves].NewRow = each[1]
            ListOfMoves[NumberOfMoves].NewColumn = each[2]
            ListOfMoves[NumberOfMoves].CanJump = True
        if len(multiTakeLeft) > 0:
            print(multiTakeLeft[-1][0], ' can take and move to ', multiTakeLeft[-1][1], ' , ', multiTakeLeft[-1][2])
            ListOfMoves[NumberOfMoves].Piece = multiTakeLeft[-1][0]
            ListOfMoves[NumberOfMoves].NewRow = multiTakeLeft[-1][1]
            ListOfMoves[NumberOfMoves].NewColumn = multiTakeLeft[-1][2]
            ListOfMoves[NumberOfMoves].CanJump = True
        if len(multiTakeRight) > 0:
            print(multiTakeRight[-1][0], ' can take and move to ', multiTakeRight[-1][1], ' , ', multiTakeRight[-1][2])
            ListOfMoves[NumberOfMoves].Piece = multiTakeRight[-1][0]
            ListOfMoves[NumberOfMoves].NewRow = multiTakeRight[-1][1]
            ListOfMoves[NumberOfMoves].NewColumn = multiTakeRight[-1][2]
            ListOfMoves[NumberOfMoves].CanJump = True
    elif len(move) > 0 or len(jump) > 0:  # new check to see if any moves or jumps
        for each in move:  # loop through moves
            NumberOfMoves += 1
            print(each[0], ' can move to ', each[1], ' , ', each[2])
            ListOfMoves[NumberOfMoves].Piece = each[0]
            ListOfMoves[NumberOfMoves].NewRow = each[1]
            ListOfMoves[NumberOfMoves].NewColumn = each[2]
            ListOfMoves[NumberOfMoves].CanJump = False
        for each in jump:  # loop through jumps
            NumberOfMoves += 1
            print(each[0], ' can jump to ', each[1], ' , ', each[2])
            ListOfMoves[NumberOfMoves].Piece = each[0]
            ListOfMoves[NumberOfMoves].NewRow = each[1]
            ListOfMoves[NumberOfMoves].NewColumn = each[2]
            ListOfMoves[NumberOfMoves].CanJump = True
    print('There are ', NumberOfMoves, ' possible moves')
    return ListOfMoves


def ListEmpty(ListOfMoves):
    if ListOfMoves[1].Piece == '':
        return True
    else:
        return False


def SelectMove(ListOfMoves):
    ValidPiece = False
    while not ValidPiece:
        Found = False
        EndOfList = False
        Piece = input('Which piece do you want to move? ')
        Index = 0
        if Piece == '':
            EndOfList = True
        while not Found and not EndOfList:
            Index += 1
            if ListOfMoves[Index].Piece == Piece:
                Found = True
            elif ListOfMoves[Index].Piece == '':
                EndOfList = True
                DisplayErrorCode(1)
        if Found:
            ValidPiece = True
    ChosenPieceIndex = Index
    ValidMove = False
    while not ValidMove:
        RowString = input('Which row do you want to move to? ')
        ColumnString = input('Which column do you want to move to? ')
        try:
            NewRow = int(RowString)
            NewColumn = int(ColumnString)
            Found = False
            EndOfList = False
            Index = ChosenPieceIndex - 1
            while not Found and not EndOfList:
                Index += 1
                if ListOfMoves[Index].Piece != Piece:
                    EndOfList = True
                    DisplayErrorCode(2)
                elif ListOfMoves[Index].NewRow == NewRow and ListOfMoves[Index].NewColumn == NewColumn:
                    Found = True
            ValidMove = Found
        except:
            DisplayErrorCode(3)
    return Index


def MoveDame(Board, Player, NewRow, NewColumn):
    if Player == 'a':
        for i in [1, 3, 5, 7]:
            if Board[0][i] == SPACE:
                NewColumn = i
                NewRow = 0
                break
    else:
        for i in [0, 2, 4, 6]:
            if Board[BOARD_SIZE - 1][i] == SPACE:
                NewColumn = i
                NewRow = BOARD_SIZE - 1
                break
    return NewRow, NewColumn


def MovePiece(Board, PlayersPieces, ChosenPiece, NewRow, NewColumn):
    Index = int(ChosenPiece[1:])
    CurrentRow = PlayersPieces[Index][ROW]
    CurrentColumn = PlayersPieces[Index][COLUMN]
    Board[CurrentRow][CurrentColumn] = SPACE

    if NewRow == BOARD_SIZE - 1 and PlayersPieces[Index][DAME] == 0:
        Player = 'a'
        PlayersPieces[0][1] += 1
        PlayersPieces[Index][DAME] = 1
        ChosenPiece = ChosenPiece.upper()
        NewRow, NewColumn = MoveDame(Board, Player, NewRow, NewColumn)
    elif NewRow == 0 and PlayersPieces[Index][DAME] == 0:
        Player = 'b'
        PlayersPieces[0][1] += 1
        PlayersPieces[Index][DAME] = 1
        ChosenPiece = ChosenPiece.upper()
        NewRow, NewColumn = MoveDame(Board, Player, NewRow, NewColumn)
    PlayersPieces[Index][ROW] = NewRow
    PlayersPieces[Index][COLUMN] = NewColumn
    Board[NewRow][NewColumn] = ChosenPiece
    return Board, PlayersPieces


def MakeMove(Board, PlayersPieces, OpponentsPieces, ListOfMoves, PieceIndex):
    PlayersPieces[0][0] += 1
    if PieceIndex > 0:
        Piece = ListOfMoves[PieceIndex].Piece
        NewRow = ListOfMoves[PieceIndex].NewRow
        NewColumn = ListOfMoves[PieceIndex].NewColumn
        PlayersPieceIndex = int(Piece[1:])
        CurrentRow = PlayersPieces[PlayersPieceIndex][ROW]
        CurrentColumn = PlayersPieces[PlayersPieceIndex][COLUMN]
        Jumping = ListOfMoves[PieceIndex].CanJump
        Board, PlayersPieces = MovePiece(Board, PlayersPieces, Piece, NewRow, NewColumn)
        if Jumping:
            MiddlePieceRow = (CurrentRow + NewRow) // 2
            MiddlePieceColumn = (CurrentColumn + NewColumn) // 2
            MiddlePiece = Board[MiddlePieceRow][MiddlePieceColumn]
            if Piece[0] != MiddlePiece[0]:  # new if pieces belong to different people
                Board[MiddlePieceRow][
                    MiddlePieceColumn] = ' '  # new set piece to empty ######note this is not '' it is ' '
                OpponentsPiece = int(MiddlePiece[1:])  # new find out the piece index
                OpponentsPieces[OpponentsPiece][ROW] = -1  # new set row to -1 meaning off board
                OpponentsPieces[OpponentsPiece][COLUMN] = -1  # new set column to -1 meaning off board
                print('took ', MiddlePiece)  # new say took instead of jumped
            else:  # new otherwise
                print('jumped over ', MiddlePiece)  # new say jumped
    return Board, PlayersPieces, OpponentsPieces


def SwapPlayer(NextPlayer):
    if NextPlayer == 'a':
        return 'b'
    else:
        return 'a'


def PrintResult(A, B, NextPlayer):
    print('Game ended')
    print(NextPlayer, ' lost this game as they cannot make a move')
    PrintPlayerPieces(A, B)


def Game():
    A = [[0, 0, 0] for Piece in range(NUMBER_OF_PIECES + 1)]
    B = [[0, 0, 0] for Piece in range(NUMBER_OF_PIECES + 1)]
    Board = [['' for Column in range(BOARD_SIZE)] for Row in range(BOARD_SIZE)]
    ListOfMoves = [MoveRecord() for Move in range(MAX_MOVES)]
    GameEnd = False
    FileFound = False
    NextPlayer = 'a'
    Scrape()
    Board, A, B, FileFound = SetUpBoard(Board, A, B, FileFound)
    if not FileFound:
        GameEnd = True
    while not GameEnd:
        PrintPlayerPieces(A, B)
        DisplayBoard(Board)
        print('Next Player: ', NextPlayer)
        ListOfMoves = ClearList(ListOfMoves)
        if NextPlayer == 'a':
            ListOfMoves = ListPossibleMoves(Board, A, NextPlayer, ListOfMoves)
            if not ListEmpty(ListOfMoves):
                PieceIndex = SelectMove(ListOfMoves)
                Board, A, B = MakeMove(Board, A, B, ListOfMoves, PieceIndex)
                NextPlayer = SwapPlayer(NextPlayer)
            else:
                GameEnd = True
        else:
            ListOfMoves = ListPossibleMoves(Board, B, NextPlayer, ListOfMoves)
            if not ListEmpty(ListOfMoves):
                PieceIndex = SelectMove(ListOfMoves)
                Board, B, A = MakeMove(Board, B, A, ListOfMoves, PieceIndex)
                NextPlayer = SwapPlayer(NextPlayer)
            else:
                GameEnd = True
    if FileFound:
        PrintResult(A, B, NextPlayer)


def Scrape():
    games = []

    directory = os.getcwd()
    contents = os.listdir(directory)

    for game in contents:
        if "game" in game:
            games.append(game)

    if len(games) == 0:
        DisplayErrorCode(5)

    for counter in range(0, len(games)):
        File = []
        FileHandle = open(games[counter], 'r')
        for row in FileHandle:
            File.append(row.strip())
        number = str(counter + 1)
        print(number + ") " + games[counter], '{0:^3}'.format("###"), "A/moves:", '{0:>2}'.format(File[0]),
              "A/Dames: " + '{0:>2}'.format(File[1]), "B/moves: " + '{0:>2}'.format(File[0]), "B/Dames: " +
              '{0:>2}'.format(File[1]))


if __name__ == "__main__":
    Game()
