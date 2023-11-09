import random

class Player:

    def __init__(self, tag, ):

        self.tag = tag

        self.hasBall = False

        self.gaurdingBall = False

        #we also need to know the position of players at all time, we can assume several formations
        #TODO

        #the following are percentages of things once the player decides on an action

        self.shotPct = 0.5

        self.passPct = 0.95

        self.dribblePct = 0.95

        """
        Players will need several attributes

        The atrributes will represent the probability of various actions occuring

        Speed variable

        Shot pct variable

        Blk percentage variable

        Steal percentage

        Pass percentage

        Some attributes will not rely on a percent but in fact a number like

        Speed

        PAce

        IQ smt like this
        """

        #the following are the various actions a player could make on attack

        self.shoot = 0.15

        self.pass_ = 0.55

        self.dribble = 0.2

        self.turnover = 0.1

        self.atkOptions = [
            1, #1.0 shoot
            1-self.shoot, #0.7 pass
            1-self.shoot-self.pass_, #0.3 steal
            1-self.shoot-self.pass_-self.dribble #0.1 turnover i.e. guarding player steals
        ]

        #the following are the various actions a player could make on defense

        self.guard = 0.7

        self.steal = 0.2

        self.foul = 0.1

        self.defOptions = [
            1, #continue quarding
            1-self.guard, #steal
            1-self.guard-self.steal #commit a foul
        ]

        #the following are options for when the defending player wants to block a shot

        self.block = 0.05

        self.foul = 0.1

        self.miss = 0.85

        self.blockOptions = [
            1, #block the shot
            1-self.block, #foul the shooter
            1-self.block-self.foul #miss entirely

        ]

    #the following four functions have to determine what a player does on defense

    def onBallAtk(self):

        action = random.random()

        if (action < self.atkOptions[3]):

            return ["T", self.turnover]

        elif (action < self.atkOptions[2]):

            return ["D", self.dribble]

        elif (action < self.atkOptions[1]):

            return ["P", self.pass_]

        else:

            return ["SH", self.shoot]

    def shotDefense(self):

        action = random.random()

        if action < self.blockOptions[2]:
            #miss
            return ["M",self.miss]

        elif action < self.blockOptions[1]:

            #fouled the player while shooting

            return ["F", self.foul]

        else:

            #they actually blocked the shot

            return ["B", self.block]

    def notOnBallAtk(self):
        #not dealing with this yet
        return 0

    def onBallDef(self):
        action  = random.random()

        if action < self.defOptions[2]:

            return "F"

        elif action < self.defOptions[1]:

            return "ST"

        else:

            return "G" #this basically means they just follow the player


    def notOnBallDef(self):

        return 0

    def makeShotDistance(self, distance = 23.5, cof = 0.5):

        #we are going to follow y = 0.15 (distance+1)^cof

        prob = 1-0.15 * (distance + 1)**cof
        if random.random() > prob:
            return True
        return False

    def makeShot(self, cof=1):

        if (random.random() > self.shotPct * cof):

            return True

        return False
