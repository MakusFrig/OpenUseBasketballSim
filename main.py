import random

from players import *

from game import *

"""
#five out dictionary

{

"LC": Player("H1"),
"RC": Player("H2"),
"LW": Player("H3"),
"RW": Player("H4"),
"T": Player("H5"),
"P": None

}
"""

def main():

    #five out dictionary {"LC", Player("H1"),}

    myTeam = {""}

    myGame = Game({

    "LC": Player("H1"),
    "RC": Player("H2"),
    "LW": Player("H3"),
    "RW": Player("H4"),
    "T": Player("H5"),
    "P": None

    },

    {

    "LC": Player("A1"),
    "RC": Player("A2"),
    "LW": Player("A3"),
    "RW": Player("A4"),
    "T": Player("A5"),
    "P": None

    })

    myGame.createGame()



main()
