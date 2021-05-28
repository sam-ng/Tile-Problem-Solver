# Tile-Problem-Solver
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/>

A solver for the 8-puzzle and 15-puzzle tile problems that applies A* search with number of misplaced tiles and sum of manhattan distances heuristics as well as the RBFS algorithm.

## Problem
The 8-puzzle problem consists of a 3-by-3 grid with 8 tiles numbered from 1-8 and a single empty tile. Legal moves consist of switching any adjacent tile with the empty tile. The goal state is to arrange all the tiles in number order with the empty tile in the bottom rightmost slot. Likewise, the 15-puzzle problem is the same with the exception of a larger 4-by-4 grid an 15 tiles numbered from 1-15.

## Instructions on Running the Program
Make sure all .py files are in the same directory. Puzzle files should be .txt files with numbers representing the tiles. Tiles in the same row are separated by commas, and rows are separated by new line characters.

Example:
1,2,3
4,5,6
,7,8

`python puzzleSolver.py A N H`

`A` is 1 for A* search and 2 for RBFS.
`N` is 3 for 8-puzzle and 4 for 15-puzzle.
`H` is 1 for the misplaced tiles heuristic and 2 for the manhattan distance heuristic.

Python version: 3.8.8
