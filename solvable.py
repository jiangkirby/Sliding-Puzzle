def solvable(number, tiles):
    '''
    Function: solvable
        Determines if tiles are in a solvalble order
    Parameters:
        number -- number of tiles the puzzle has
        tiles -- order in which tiles will be placed
    Returns True/False depending on if puzzle is solvable
    '''
    # inversions: occurrences in while tile number is before
    # another tild number that is lesser than it
    inversions = 0
    # counts the number of inversions
    for i in range(number - 1):
        for j in range(i + 1, number):
            if tiles[i] != number and tiles[j] != number \
                and tiles[i] > tiles[j]:
                inversions += 1

    # determines side length of puzzle and whether or not it is odd/even
    # will play a role in determining if puzzle is solvable or not
    if number % 2 == 1:
        return inversions % 2 == 0
    else:
        position = tiles.index(number)
        side = (number ** (1/2))
        if (side - (position // side)) % 2 == 0:
            return inversions % 2 == 1
        return inversions % 2 == 0
