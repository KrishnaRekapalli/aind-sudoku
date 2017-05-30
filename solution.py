assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values




def cross(A, B):
    return [s+t for s in A for t in B]
    "Cross product of elements in A and elements in B."
    pass


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units+ diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#print(diagonal_units)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"


    res = {}

    for i in boxes:
        index = boxes.index(i)

        if grid[index] == '.':
            res[i] = '123456789'
        else:
            res[i] = grid[index]


    return res

    pass


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

    pass


def eliminate(values):
    """
    If we have any cell having only one value, we just eliminate the possibility of that value in all its peers

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary after eliminating the posiibilities based on single valued cells.
    """

    for i in values:

        if len(values[i]) == 1:

            key_peers = list(peers[i])

            for j in key_peers:

                #values[j] = values[j].replace(values[i],'')
                assign_value(values, j, values[j].replace(values[i],''))



    return values

    pass

def only_choice(values):

    """
    For every cell, among its unit members we check if any of the possible values are unique to the cell
    If that is the case then we assign the unique value to the cell as only choice.
    This function considers every unit the cell is a member of and then checks if a possibility is only Choice

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with only choice vlaues assigned.

    """

    for i in values:

        cell_units = units[i]

        for j in cell_units:
            unit_vals = ''.join(values[k] for k in j)

            for l in values[i]:
                if unit_vals.count(l) == 1:
                    #values[i] = l
                    assign_value(values, i, l)


    return values

    pass




def naked_twins(values):

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """


    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for j in unitlist:
        # In every unit : square, row, column and diagonal, we search for naled twins
        # First we search for cells that have exactly two elements we call these cells target cells
        target_cells = [k for k in j if len(values[k]) == 2 ]
        # Now we find the values in these target cells

        target_cell_vals = [values[i] for i in target_cells]

        #
        if len(target_cells)>1:
            for cell_val in target_cell_vals:
                # Now in the target cell values we are specifically looking for naked twins

                if target_cell_vals.count(cell_val) == 2:
                    # If we found naked twins we then get their indices and also their content
                    naked_twin_indices = [i for i,val in enumerate(target_cell_vals) if val==cell_val]
                    naked_twin_cells = [target_cells[i] for i in naked_twin_indices]

                    naked_twin_content = list(values[naked_twin_cells[0]])

                    # Make a list of all other boxes in the unit
                    unit_compliment  = [i for i in j if i not in naked_twin_cells]
                    
                    # for every box other than twins remove the twin content from possible values
                    for twin_element in naked_twin_content:

                        for element in unit_compliment:

                            #values[element] = values[element].replace(twin_element,'')
                            assign_value(values, element, values[element].replace(twin_element,''))

    return values







        #solved_values = [box for box in values.keys() if len(values[box]) == 1]


def reduce_puzzle(values):

    """ Apply all the reduction strategies to a raw sudoku and return the reduced sudoku
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        The dictionary representation of the reduced sudoku grid. False if error. (error handling)

    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # : Use the Eliminate Strategy
        values = eliminate(values)

        # : Use the Only Choice Strategy

        values = only_choice(values)

        # : Use the Naked twins Strategy

        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

    pass

def search(values):

    """
    Search for a feasible solution given a values dictionaty

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists. (error handling)

    """

    values = reduce_puzzle(values)


    if values == False:
        return False

    else:
        # If all cells have one one value in them then sudoku is solved we return the solution
        if max([len(values[i]) for i in values.keys()]) == 1:

            return values
             # Solved!

        else:
            # If it is yet to be solved then we branc on unsolved cells

            toBeSolvedCells = []

            for i in values.keys():
                if len(values[i]) > 1:
                    toBeSolvedCells.append(i)

            # From the available cells that aren't solved we select one to branch on

            nodeCell = toBeSolvedCells.pop()


            for k in values[nodeCell]:

                newsudoku = values.copy()
                newsudoku[nodeCell] = k


                # Now we try to solve a reduced sudoku. This step will recursively take us to all possible sudokus and
                # return when it finds a feasible solution

                attempt = search(newsudoku)

                if attempt:
                    return attempt

    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)



    attempt = search(values)

    if attempt:
        return attempt
    else:
        return False




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
