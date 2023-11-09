import random

AND1COF = 0.5

DISTANCES = [4, 10, 15, 24]

DISTANCES_WEIGHT = [0.2, 0.2, 0.3, 0.3]



"""

We will need formations

5-out will be a dictionary with 6 positions, all around the perimeter and the paint

{"LC":Player1, "P", None} like this

"""
def average(values):

    total = 0
    for i in values:

        total += i

    return total / len(value)

def getDribbleAt(position):

    #this function gets the possible positions that one can dribbble at if they have the ball

    #this is only for a 5 out though

    if position == "T":

        return ["LW", "RW"]

    elif position == "LW":

        return ["LC", "T"]

    elif position == "RW":

        return ["RC", "T"]

    elif position == "LC":

        return ["LW"]

    elif position == "RC":

        return ["RW"]

def shotDistance():

    global DISTANCES, DISTANCES_WEIGHT

    return random.choices(DISTANCES, weights=DISTANCES_WEIGHT)[0]

class Game:
    """
    This class will be the one that does everything to do with the Game

    It will keep record of all the players and hopefully create a game log

    Create a third program to read game logs

    """


    def __init__(self, team1, team2):

        #the following will be dictionaries with
        #the keys being the positions on the basketball court and the value being the players

        self.score1 = 0

        self.score2 = 0

        self.team1 = team1

        self.team2 = team2

        self.team1["T"].hasBall = True

        self.team2["T"].guardingBall = True

        self.quarter = 1

        #each action that a player makes will take a set amount of time off the clock

        #this could mean that a pass could take anywhere from 2-4 seconds which will be determined randomly

        self.time = 12*60 #12 minutes by 60 seconds

        self.shotclock = 24

    def __str__(self):

        finalString = ""

        for i in list(self.team1.keys()):
            if self.team1[i] != None:

                if self.team1[i].hasBall:
                    finalString += i+"\t:"+self.team1[i].tag+"\t*\n"
                else:
                    finalString += i+"\t:"+self.team1[i].tag+"\n"



        for i in list(self.team2.keys()):
            if self.team2[i] != None:
                if self.team2[i].hasBall:
                    finalString += i+"\t:"+self.team2[i].tag+"\t*\n"
                else:
                    finalString += i+"\t:"+self.team2[i].tag+"\n"

        return finalString

    def passBall(self, position1, position2, team):

        if team == 1:

            self.team1[position1].hasBall = False
            self.team2[position1].guardingBall = False

            self.team1[position2].hasBall = True
            self.team2[position2].guardingBall = True

        else:

            self.team2[position1].hasBall = False
            self.team1[position1].guardingBall = False

            self.team2[position2].hasBall = True
            self.team1[position2].guardingBall = True

    def switchPosession(self, position1, position2):

        if self.team1[position1].hasBall:

            #team1 has the ball and we need to switch

            self.team1[position1].hasBall = False
            self.team1[position1].guardingBall = True

            self.team2[position2].hasBall = True
            self.team2[position2].guardingBall = False

        else:

            self.team2[position1].hasBall = False
            self.team2[position1].guardingBall = True

            self.team1[position2].hasBall = True
            self.team1[position2].guardingBall = False

    def switchPositions(self, position1, position2, team):

        #this function switches the positions of players,
        #usefuil for after a pass or dribble at

        if team == 1:

            #we are switching players on team1

            tempPlayer = self.team1[position1]

            self.team1[position1] = self.team1[position2]

            self.team1[position2] = tempPlayer

        else:

            tempPlayer = self.team2[position1]

            self.team2[position1] = self.team2[position2]

            self.team2[position2] = tempPlayer

    def fill(self):

        #this function will fill the sots by rotating the wheel

        #first we need to check if there is someone in the post position

        for p in list(self.team1.keys()):

            if self.team1[p] != None:

                pass

        pass

    def printScore(self):

        print("Home: "+self.score1+" Away: "+self.score2)

    def createGame(self):

        #potentially used to create a random game
        for i in range(4):
            while self.time > 0:
                self.shotclock = 24

                reset = False
                while self.shotclock > 0:


                    for p in list(self.team1.keys()): #iterating through the positions

                        if self.team1[p] == None: #this si in case there is a blank spot

                            continue

                        if self.team1[p].hasBall == True:
                            #first we get the probable action of the player with the ball
                            #then we need to adjust the defenders actions

                            #obviously the defender cant steal when shooting, but he can try to block

                            #this means rewriting the defenders options in the player file
                            atkAction = self.team1[p].onBallAtk()
                            #now we need to evaluate the attacking options

                            if atkAction[0] == "SH":

                                #he is shooting

                                defAction = self.team2[p].shotDefense()

                                if defAction[0] == "M":

                                    #the defender missed the block and the player is free to shoot

                                    d = shotDistance()

                                    if self.team1[p].makeShotDistance(distance = d):

                                        #the player scores
                                        if d >= 23.5:
                                            self.score1 += 3
                                        else:
                                            self.score1 += 2

                                    else:

                                        #the player missed and lets assume its going the other way



                                        self.switchPosession(p, p)

                                elif defAction[0] == "F":



                                    #the defender fould the player while shooting

                                    if self.team1[p].makeShot(AND1COF):


                                        # we are assuming they make the free throw for now

                                        self.score1 +=2
                                        if self.team1[p].makeShotDistance(15):

                                            self.score1 += 1



                                    else:

                                        #the player misses and shoots free throws


                                        if self.team1[p].makeShotDistance(15):

                                            self.score1 += 1

                                        if self.team1[p].makeShotDistance(15):

                                            self.score1 += 1


                                        self.switchPosession(p, p)

                                elif defAction[0] == "B":
                                    #the shot was blocked and the ball gets turned over
                                    self.switchPosession(p, p)

                                self.shotclock = 0

                                self.time -=3

                                reset = True

                                break

                            elif atkAction[0] == "P":

                                #they passed the ball

                                #we need to change who has the ball

                                # we need to swap the post with the player who passed the ball
                                passReceiver = random.choice(getDribbleAt(p))
                                self.passBall(p, passReceiver, 1)

                                self.switchPositions(p, passReceiver, 1)
                                self.shotclock -= 3
                                self.time -=3

                            elif atkAction[0] == "D": #this function works right now
                                #they are going to do a dribble at
                                #the player dribbled at need to go to the post
                                #basically swap positions around



                                dribbleReceiever = random.choice(getDribbleAt(p))

                                self.switchPositions(dribbleReceiever, p, 1)



                                #dont forget to change the position of the opponents as well

                                self.switchPositions(dribbleReceiever, p, 2)



                                #from here we also need to move the other players around the court

                                #TODO
                                self.shotclock -= 3
                                self.time -=3

                            else:

                                #they turn over the ball



                                #we just need to switch possessions here

                                self.switchPosession(p, p)

                                self.shotclock = 0

                                reset = True
                                self.time -= 3

                                break







                            #from here we need to evaluate how the two correspond
                            #i.e.
                    if reset: #this is to stop a shot clock going on if there is a change of possessions

                        break
                    for p in list(self.team2.keys()): #iterating through the positions for the second team now

                        if self.team2[p] == None: #this si in case there is a blank spot

                            continue

                        if self.team2[p].hasBall == True:
                            #first we get the probable action of the player with the ball
                            #then we need to adjust the defenders actions

                            #obviously the defender cant steal when shooting, but he can try to block

                            #this means rewriting the defenders options in the player file
                            atkAction = self.team2[p].onBallAtk()
                            #now we need to evaluate the attacking options

                            if atkAction[0] == "SH":

                                #he is shooting

                                defAction = self.team1[p].shotDefense()

                                if defAction[0] == "M":

                                    #the defender missed the block and the player is free to shoot
                                    d = shotDistance()
                                    if self.team2[p].makeShotDistance(distance = d):

                                        #the player scores
                                        if d >= 23.5:
                                            self.score2 += 3

                                        else:
                                            self.score2 += 2

                                    else:

                                        #the player missed and lets assume its going the other way

                                        self.switchPosession(p, p)

                                elif defAction[0] == "F":



                                    #the defender fould the player while shooting

                                    if self.team2[p].makeShot(AND1COF):


                                        # we are assuming they make the free throw for now

                                        self.score2 +=2
                                        if self.team2[p].makeShotDistance(15):
                                            #this is to make the extra free throw

                                            self.score2 += 1


                                    else:

                                        #the player misses and shoots free throws


                                        madefirst = False
                                        if self.team2[p].makeShotDistance(15):

                                            self.score2 += 1




                                        if self.team2[p].makeShotDistance(15):


                                            self.score2 += 1

                                        self.switchPosession(p, p)

                                elif defAction[0] == "B":
                                    #the shot was blocked and the ball gets turned over
                                    self.switchPosession(p, p)

                                self.shotclock = 0
                                self.time -=3



                                break

                            elif atkAction[0] == "P":

                                #they passed the ball

                                #we need to change who has the ball

                                # we need to swap the post with the player who passed the ball
                                passReceiver = random.choice(getDribbleAt(p))
                                self.passBall(p, passReceiver, 1)

                                self.switchPositions(p, passReceiver, 1)
                                self.shotclock -= 3
                                self.time -= 3

                            elif atkAction[0] == "D": #this function works right now
                                #they are going to do a dribble at
                                #the player dribbled at need to go to the post
                                #basically swap positions around



                                dribbleReceiever = random.choice(getDribbleAt(p))

                                self.switchPositions(dribbleReceiever, p, 1)



                                #dont forget to change the position of the opponents as well

                                self.switchPositions(dribbleReceiever, p, 2)



                                #from here we also need to move the other players around the court

                                #TODO
                                self.shotclock -= 3
                                self.time -= 3

                            else:

                                #they turn over the ball



                                #we just need to switch possessions here

                                self.switchPosession(p, p)

                                self.shotclock = 0
                                self.time -=3






                            #from here we need to evaluate how the two correspond
                            #i.e.
            self.time = 12*60







        #print the score at the end of every play

        print("Home: "+str(self.score1) + "|||Away: "+str(self.score2))



        return
