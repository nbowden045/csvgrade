# CSVGrader for MyPhysics\

Annoyed by MyPhisics rubric grading being f******* annoying? Want an easy way to go through a graphical interface that organizes submissions
by timestamp, displays the rubric as a clickable menu, and allows grades to be assigned on a group basis? Well this is the project for you! 

In its current form you can select a gradebook file with rubric definitions as well as a directory of submissions and it will allow you to 
click rubric categories, enter comments, assign groups, and it will automagically assign the grade to everyone in that group. There is a 
graphical group editor that can import and export group defs as CSV files, assign students to groups either by submission or by entering netID,
and add/remove groups and students. 

This program is still early in development and as a result lacks automation. For instance, there is no class roster display or gradebook 
display capability. There are a list of features I would like to add described below and if you would like to help out feel free to work on 
any of them, or if there is a feature not suggested that you would like to add feel free to implement it and submit a pull request!

Note that this **only** works with rubric definitions (i.e. no numeric grading), and does not support multiple rubric versions in a CSV file (yet) or entering 0 grades.

You can run this software from `src/csvgrade/mainGUI.py` as the entry point. 


## Prospectus

- Store correspondence data between student NetID and groups DONE
- Import `class` class with that data DONE
- Gradebook should be compatible csv with the myphysics platform PARTIAL
- folder import of submissions DONE
- assignments imported DONE

## Features I want (so far)
- Rubric version selection 
- Group information display in Student Info pane
- Class roster display with search by name capability
   - Currently I'm only using Pandas and a database of some form would undoubtedly be more efficent
   - This would also allow easier group editing
   - Could be easily expanded to include a graphical gradebook display
- Grade by student
    - Go by NetID in gradebook and allow assigning ABS/EX/0 grades to each student
- Dynamic line wrapping based on window resize in the rubric section
- Scrollbar in rubric pane
- First/last name display/add by capability in group editor




## Installation

Can be installed after cloning the repo using
`pip install <clone dir>`

Please note that this requires python >3.7 and has not been tested on less than 3.13!

## Developers
You can install the package as editable using the `-e` flag in pip
