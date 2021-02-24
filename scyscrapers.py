"""
This module contains read_input, left_to_right_check, check_not_finished_board,
check_uniqueness_in_board, check_horizontal_visibility, row_visiability,
check_columns, trans_board, check_skyscapers functions
"""
def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    """
    list_of_lines = []
    with open(path, "r") as file:
        for line in file.readlines():
            list_of_lines.append(line.strip("\n"))
    return list_of_lines

def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible \
    looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if int(input_line[0]) != pivot:
        return False

    check_line = input_line[1:-1]
    count = 1
    max_height = int(check_line[0])
    for index in range(1, len(check_line)):
        if int(check_line[index]) > max_height:
            max_height = int(check_line[index])
            count += 1
    return count == pivot

def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the \
    game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', \
'*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', \
'*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', \
'*35214*', '*41532*', '*2*1***'])
    False
    """
    for item in board:
        if "?" in item:
            return False
    return True

def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215',\
'*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', \
'*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', \
'*35214*', '*41532*', '*2*1***'])
    False
    """
    for r_ind in range(1, len(board)-1):
        row = board[r_ind][1:-1]
        for check in row:
            if row.count(check) != 1:
                return False
    return True

def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    def row_visiability(board_row: str) -> int:
        row = board_row[1: -1]
        vis = 1
        max_h = int(row[0])
        for ind in range(1, len(row)):
            if max_h <= int(row[ind]):
                vis += 1
                max_h = int(row[ind])
        return vis

    for r_ind in range(1, len(board)-1):
        if board[r_ind][0] != "*":
            l_vis = row_visiability(board[r_ind])
            if l_vis != int(board[r_ind][0]):
                return False
        if board[r_ind][-1] != "*":
            r_vis = row_visiability(board[r_ind][::-1])
            if r_vis != int(board[r_ind][-1]):
                return False
    return True


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings\
    of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical
    \case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', \
'*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
'*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', \
'*41532*', '*2*1***'])
    False
    """
    def trans_board(board):
        t_board = []
        for r_ind in range(len(board)):
            line = ""
            for c_ind in range(len(board)):
                line += board[c_ind][r_ind]
            t_board.append(line)
        return t_board

    t_board = trans_board(board)
    return check_horizontal_visibility(t_board)

def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    """
    board = read_input(input_path)
    if not check_not_finished_board(board):
        return False
    if not check_uniqueness_in_rows(board):
        return False
    if not check_horizontal_visibility(board):
        return False
    if not check_columns(board):
        return False
    return True
