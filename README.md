# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

#### This is the first project of a series of projects in Artificial Intelligence Nanodegree with Udacity. 

#### I forked the existing code and implemented the following strategies
   elimination  
   only choice 
   naked twins
   search
   diagonal sudoku 
   
#### All the implementations are in solution.py




# Naked Twins
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Similar to the elimination and only choice strategies, we use the naked twins strategy to reduce the sudoku to a simpler form. If in any unit i.e. square, row, column or diagonal there are two boxes with same probable twin values, then we have to eliminate the possibility of any of these two values from the rest of the boxes in the unit. This functionality is coded as a function 'naked_twins' and the function is executed in 'reduce_sudoku' function after the 'elimination' and 'only choice' strategies.

# Diagonal Sudoku
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Along with the square units, row and column units, now we will have diagonal units. We first create the diagonal units and then add them to the 'unitlist'. Now every cell in sudoku will have 26 peers. As the code is written in modular form, this change will be enough to make sure that we are solving the diagonal sudoku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

