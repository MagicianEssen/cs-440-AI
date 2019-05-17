from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        #self.startBoardIdx=4
        self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

        self.bmove = [0,0]
        self.clearboard=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]        


    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        
        #rule 1
        #max
        if (self.checkWinner()==1 and isMax):
            score = self.winnerMaxUtility
            return score
        #min
        if (self.checkWinner()==-1 and (not isMax)):
            score = self.winnerMinUtility
            return score
        #rule 2
        count1=0 #two in a row
        count2=0 #prevent two in a row
        if(isMax==True):#max
            for firstidx in self.globalIdx:
                x, y = firstidx
            #check row
    
                for i in range(3):
                    if(    ((self.board[x][y+i] == '_')and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.maxPlayer))
                        or ((self.board[x+1][y+i] == '_') and (self.board[x][y+i] == self.board[x+2][y+i] == self.maxPlayer)) 
                        or ((self.board[x+2][y+i] == '_') and (self.board[x][y+i] == self.board[x+1][y+i] == self.maxPlayer))):
                        count1+=1
                    elif(  ((self.board[x][y+i] == self.maxPlayer) and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.minPlayer))
                        or ((self.board[x+1][y+i] == self.maxPlayer) and (self.board[x][y+i] == self.board[x+2][y+i] == self.minPlayer)) 
                        or ((self.board[x+2][y+i] == self.maxPlayer) and (self.board[x][y+i] == self.board[x+1][y+i] == self.minPlayer))):
                        count2+=1
                #check column:
                for j in range(3):
                    if(    ((self.board[x+j][y] == '_') and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.maxPlayer))
                        or ((self.board[x+j][y+1] == '_') and (self.board[x+j][y] == self.board[x+j][y+2] == self.maxPlayer)) 
                        or ((self.board[x+j][y+2] == '_') and (self.board[x+j][y] == self.board[x+j][y+1] == self.maxPlayer))):
                        count1+=1
                    elif(  ((self.board[x+j][y] == self.maxPlayer) and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.minPlayer))
                        or ((self.board[x+j][y+1] == self.maxPlayer) and (self.board[x+j][y] == self.board[x+j][y+2] == self.minPlayer)) 
                        or ((self.board[x+j][y+2] == self.maxPlayer) and (self.board[x+j][y] == self.board[x+j][y+1] == self.minPlayer))):
                        count2+=1
                #check diagonal:
                if(   ((self.board[x][y] == '_') and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.maxPlayer)) 
                   or ((self.board[x+1][y+1] == '_') and (self.board[x][y] == self.board[x+2][y+2] == self.maxPlayer))
                   or ((self.board[x+2][y+2] == '_') and (self.board[x][y] == self.board[x+1][y+1] == self.maxPlayer))):
                    count1+=1
                if(   ((self.board[x+2][y] == '_') and (self.board[x+1][y+1] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x+1][y+1] == '_') and (self.board[x+2][y] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x][y+2] == '_') and (self.board[x+1][y+1] == self.board[x+2][y] == self.maxPlayer))):
                    count1+=1
                if( ((self.board[x][y] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.minPlayer)) 
                   or ((self.board[x+1][y+1] == self.maxPlayer) and (self.board[x][y] == self.board[x+2][y+2] == self.minPlayer))
                   or ((self.board[x+2][y+2] == self.maxPlayer) and (self.board[x][y] == self.board[x+1][y+1] == self.minPlayer))):
                    count2+=1
                if(((self.board[x+2][y] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x+1][y+1] == self.maxPlayer) and (self.board[x+2][y] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x][y+2] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x+2][y] == self.minPlayer))):
                    count2+=1
        
            score = self.twoInARowMaxUtility * count1 + self.preventThreeInARowMaxUtility * count2
        else: #min
            for firstidx in self.globalIdx:
                x, y = firstidx
                for i in range(3):
                    if(    ((self.board[x][y+i] == '_')and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.minPlayer))
                        or ((self.board[x+1][y+i] == '_') and (self.board[x][y+i] == self.board[x+2][y+i] == self.minPlayer)) 
                        or ((self.board[x+2][y+i] == '_') and (self.board[x][y+i] == self.board[x+1][y+i] == self.minPlayer))):
                        count1+=1
                    elif(  ((self.board[x][y+i] == self.minPlayer) and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.maxPlayer))
                        or ((self.board[x+1][y+i] == self.minPlayer) and (self.board[x][y+i] == self.board[x+2][y+i] == self.maxPlayer)) 
                        or ((self.board[x+2][y+i] == self.minPlayer) and (self.board[x][y+i] == self.board[x+1][y+i] == self.maxPlayer))):
                        count2+=1
                #check column:
                for j in range(3):
                    if(    ((self.board[x+j][y] == '_') and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.minPlayer))
                        or ((self.board[x+j][y+1] == '_') and (self.board[x+j][y] == self.board[x+j][y+2] == self.minPlayer)) 
                        or ((self.board[x+j][y+2] == '_') and (self.board[x+j][y] == self.board[x+j][y+1] == self.minPlayer))):
                        count1+=1
                    elif(  ((self.board[x+j][y] == self.minPlayer) and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.maxPlayer))
                        or ((self.board[x+j][y+1] == self.minPlayer) and (self.board[x+j][y] == self.board[x+j][y+2] == self.maxPlayer)) 
                        or ((self.board[x+j][y+2] == self.minPlayer) and (self.board[x+j][y] == self.board[x+j][y+1] == self.maxPlayer))):
                        count2+=1
                #check diagonal:
                if(   ((self.board[x][y] == '_') and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.minPlayer)) 
                   or ((self.board[x+1][y+1] == '_') and (self.board[x][y] == self.board[x+2][y+2] == self.minPlayer))
                   or ((self.board[x+2][y+2] == '_') and (self.board[x][y] == self.board[x+1][y+1] == self.minPlayer))):
                    count1+=1
                if(   ((self.board[x+2][y] == '_') and (self.board[x+1][y+1] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x+1][y+1] == '_') and (self.board[x+2][y] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x][y+2] == '_') and (self.board[x+1][y+1] == self.board[x+2][y] == self.minPlayer))):
                    count1+=1
                if( ((self.board[x][y] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.maxPlayer)) 
                   or ((self.board[x+1][y+1] == self.minPlayer) and (self.board[x][y] == self.board[x+2][y+2] == self.maxPlayer))
                   or ((self.board[x+2][y+2] == self.minPlayer) and (self.board[x][y] == self.board[x+1][y+1] == self.maxPlayer))):
                    count2+=1

                if(   ((self.board[x+2][y] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x+1][y+1] == self.minPlayer) and (self.board[x+2][y] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x][y+2] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x+2][y] == self.maxPlayer))):
                    count2+=1
            score = self.twoInARowMinUtility * count1 + self.preventThreeInARowMinUtility * count2
        if(score!=0):
            return score

        #rule 3
        
        count3= 0
        if(isMax == True):
            for firstidx in self.globalIdx:
                x, y = firstidx
                if(self.board[x][y] == self.maxPlayer):
                    count3+=1
                if(self.board[x+2][y] == self.maxPlayer):
                    count3+=1
                if(self.board[x][y+2] == self.maxPlayer):
                    count3+=1
                if(self.board[x+2][y+2] == self.maxPlayer):
                    count3+=1
            score = self.cornerMaxUtility * count3
        else:
            for firstidx in self.globalIdx:
                x, y = firstidx
                if(self.board[x][y] == self.minPlayer):
                    count3+=1
                if(self.board[x+2][y] == self.minPlayer):
                    count3+=1
                if(self.board[x][y+2] == self.minPlayer):
                    count3+=1
                if(self.board[x+2][y+2] == self.minPlayer):
                    count3+=1
            score =self.cornerMinUtility * count3
        return score


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        
        #rule 1
        #max
        if (self.checkWinner()==1 ):
            score = self.winnerMaxUtility
            return score
        #min
        if (self.checkWinner()==-1 ):
            score = self.winnerMinUtility
            return score
        #rule 2
        count1=0 #two in a row
        count2=0 #prevent two in a row
        if(isMax==True):#max
            for firstidx in self.globalIdx:
                x, y = firstidx
            #check row
    
                for i in range(3):
                    if(    ((self.board[x][y+i] == '_')and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.maxPlayer))
                        or ((self.board[x+1][y+i] == '_') and (self.board[x][y+i] == self.board[x+2][y+i] == self.maxPlayer)) 
                        or ((self.board[x+2][y+i] == '_') and (self.board[x][y+i] == self.board[x+1][y+i] == self.maxPlayer))):
                        count1+=1
                    elif(  ((self.board[x][y+i] == self.maxPlayer) and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.minPlayer))
                        or ((self.board[x+1][y+i] == self.maxPlayer) and (self.board[x][y+i] == self.board[x+2][y+i] == self.minPlayer)) 
                        or ((self.board[x+2][y+i] == self.maxPlayer) and (self.board[x][y+i] == self.board[x+1][y+i] == self.minPlayer))):
                        count2+=1
                #check column:
                for j in range(3):
                    if(    ((self.board[x+j][y] == '_') and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.maxPlayer))
                        or ((self.board[x+j][y+1] == '_') and (self.board[x+j][y] == self.board[x+j][y+2] == self.maxPlayer)) 
                        or ((self.board[x+j][y+2] == '_') and (self.board[x+j][y] == self.board[x+j][y+1] == self.maxPlayer))):
                        count1+=1
                    elif(  ((self.board[x+j][y] == self.maxPlayer) and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.minPlayer))
                        or ((self.board[x+j][y+1] == self.maxPlayer) and (self.board[x+j][y] == self.board[x+j][y+2] == self.minPlayer)) 
                        or ((self.board[x+j][y+2] == self.maxPlayer) and (self.board[x+j][y] == self.board[x+j][y+1] == self.minPlayer))):
                        count2+=1
                #check diagonal:
                if(   ((self.board[x][y] == '_') and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.maxPlayer)) 
                   or ((self.board[x+1][y+1] == '_') and (self.board[x][y] == self.board[x+2][y+2] == self.maxPlayer))
                   or ((self.board[x+2][y+2] == '_') and (self.board[x][y] == self.board[x+1][y+1] == self.maxPlayer))):
                    count1+=1
                if(   ((self.board[x+2][y] == '_') and (self.board[x+1][y+1] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x+1][y+1] == '_') and (self.board[x+2][y] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x][y+2] == '_') and (self.board[x+1][y+1] == self.board[x+2][y] == self.maxPlayer))):
                    count1+=1
                if( ((self.board[x][y] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.minPlayer)) 
                   or ((self.board[x+1][y+1] == self.maxPlayer) and (self.board[x][y] == self.board[x+2][y+2] == self.minPlayer))
                   or ((self.board[x+2][y+2] == self.maxPlayer) and (self.board[x][y] == self.board[x+1][y+1] == self.minPlayer))):
                    count2+=1
                if(((self.board[x+2][y] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x+1][y+1] == self.maxPlayer) and (self.board[x+2][y] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x][y+2] == self.maxPlayer) and (self.board[x+1][y+1] == self.board[x+2][y] == self.minPlayer))):
                    count2+=1
        
            score = self.twoInARowMaxUtility * count1 + self.preventThreeInARowMaxUtility * count2
        else: #min
            for firstidx in self.globalIdx:
                x, y = firstidx
                for i in range(3):
                    if(    ((self.board[x][y+i] == '_')and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.minPlayer))
                        or ((self.board[x+1][y+i] == '_') and (self.board[x][y+i] == self.board[x+2][y+i] == self.minPlayer)) 
                        or ((self.board[x+2][y+i] == '_') and (self.board[x][y+i] == self.board[x+1][y+i] == self.minPlayer))):
                        count1+=1
                    elif(  ((self.board[x][y+i] == self.minPlayer) and (self.board[x+1][y+i] == self.board[x+2][y+i] == self.maxPlayer))
                        or ((self.board[x+1][y+i] == self.minPlayer) and (self.board[x][y+i] == self.board[x+2][y+i] == self.maxPlayer)) 
                        or ((self.board[x+2][y+i] == self.minPlayer) and (self.board[x][y+i] == self.board[x+1][y+i] == self.maxPlayer))):
                        count2+=1
                #check column:
                for j in range(3):
                    if(    ((self.board[x+j][y] == '_') and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.minPlayer))
                        or ((self.board[x+j][y+1] == '_') and (self.board[x+j][y] == self.board[x+j][y+2] == self.minPlayer)) 
                        or ((self.board[x+j][y+2] == '_') and (self.board[x+j][y] == self.board[x+j][y+1] == self.minPlayer))):
                        count1+=1
                    elif(  ((self.board[x+j][y] == self.minPlayer) and (self.board[x+j][y+1] == self.board[x+j][y+2] == self.maxPlayer))
                        or ((self.board[x+j][y+1] == self.minPlayer) and (self.board[x+j][y] == self.board[x+j][y+2] == self.maxPlayer)) 
                        or ((self.board[x+j][y+2] == self.minPlayer) and (self.board[x+j][y] == self.board[x+j][y+1] == self.maxPlayer))):
                        count2+=1
                #check diagonal:
                if(   ((self.board[x][y] == '_') and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.minPlayer)) 
                   or ((self.board[x+1][y+1] == '_') and (self.board[x][y] == self.board[x+2][y+2] == self.minPlayer))
                   or ((self.board[x+2][y+2] == '_') and (self.board[x][y] == self.board[x+1][y+1] == self.minPlayer))):
                    count1+=1
                if(   ((self.board[x+2][y] == '_') and (self.board[x+1][y+1] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x+1][y+1] == '_') and (self.board[x+2][y] == self.board[x][y+2] == self.minPlayer))
                   or ((self.board[x][y+2] == '_') and (self.board[x+1][y+1] == self.board[x+2][y] == self.minPlayer))):
                    count1+=1
                if( ((self.board[x][y] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x+2][y+2] == self.maxPlayer)) 
                   or ((self.board[x+1][y+1] == self.minPlayer) and (self.board[x][y] == self.board[x+2][y+2] == self.maxPlayer))
                   or ((self.board[x+2][y+2] == self.minPlayer) and (self.board[x][y] == self.board[x+1][y+1] == self.maxPlayer))):
                    count2+=1

                if(   ((self.board[x+2][y] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x+1][y+1] == self.minPlayer) and (self.board[x+2][y] == self.board[x][y+2] == self.maxPlayer))
                   or ((self.board[x][y+2] == self.minPlayer) and (self.board[x+1][y+1] == self.board[x+2][y] == self.maxPlayer))):
                    count2+=1
            score = self.twoInARowMinUtility * count1 + self.preventThreeInARowMinUtility * count2
        #if(score!=0):
        #    return score

        #rule 3
        
        count3= 0

        for firstidx in self.globalIdx:
            x, y = firstidx
            if(self.board[x][y] == self.maxPlayer):
                count3+=1
            if(self.board[x+2][y] == self.maxPlayer):
                count3+=1
            if(self.board[x][y+2] == self.maxPlayer):
                count3+=1
            if(self.board[x+2][y+2] == self.maxPlayer):
                count3+=1
        #score = self.cornerMaxUtility * count3
        for firstidx in self.globalIdx:
            x, y = firstidx
            if(self.board[x][y] == self.minPlayer):
                count3-=1
            if(self.board[x+2][y] == self.minPlayer):
                count3-=1
            if(self.board[x][y+2] == self.minPlayer):
                count3-=1
            if(self.board[x+2][y+2] == self.minPlayer):
                count3-=1
        score =self.cornerMaxUtility * count3
        return score


    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in range(9):
            for j in range(9):
                if (self.board[i][j] == '_'):
                    return True
        movesLeft=False

        return movesLeft

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        for firstidx in self.globalIdx:
            x, y = firstidx
            #check row
            for i in range(3):
                if(self.board[x][y+i] == self.board[x+1][y+i] == self.board[x+2][y+i] == self.maxPlayer):
                    return 1
                elif(self.board[x][y+i] == self.board[x+1][y+i] == self.board[x+2][y+i] == self.minPlayer):
                    return -1
            #check column
            for j in range(3):
                if(self.board[x+j][y] == self.board[x+j][y+1] == self.board[x+j][y+2] == self.maxPlayer):
                    return 1
                elif(self.board[x+j][y] == self.board[x+j][y+1] == self.board[x+j][y+2] == self.minPlayer):
                    return -1
            #check diagonal 
            if((self.board[x][y] == self.board[x+1][y+1] == self.board[x+2][y+2] == self.maxPlayer) or 
               (self.board[x+2][y] == self.board[x+1][y+1] == self.board[x][y+2] == self.maxPlayer)):
                return 1
            elif((self.board[x][y] == self.board[x+1][y+1] == self.board[x+2][y+2] == self.minPlayer) or 
                 (self.board[x+2][y] == self.board[x+1][y+1] == self.board[x][y+2] == self.minPlayer)):
                return -1
        winner=0
        return 0


    def alphabetadesigned(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        #print("mine evaluated!!!!!!!!!!")
        if(depth == 3):
            return self.evaluateDesigned(not isMax)

        #calulate each level
        if(isMax== True):
            bestValue = -1000000.0
            y,x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        self.board[y+i][x+j]=self.maxPlayer
                        self.expandedNodes+=1
                        newvalue = self.alphabetadesigned(depth+1, (3*i+j),alpha, beta, not isMax)

                        if(newvalue>bestValue):
                            bestValue = newvalue
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                                #print("set new move")
                        alpha = max(alpha, newvalue)
                        self.board[y+i][x+j] = '_'
                        if(alpha>= beta):
                            break
        else:
            bestValue = 1000000.0
            y, x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        self.board[y+i][x+j]=self.minPlayer
                        self.expandedNodes+=1
                        newvalue = self.alphabetadesigned(depth+1, (3*i+j),alpha, beta, not isMax)
                        if(newvalue < bestValue):
                            bestValue = newvalue
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                        alpha = min(alpha, newvalue)
                        self.board[y+i][x+j] = '_'
                        if(alpha>=beta):
                            break
        return bestValue


    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if(depth == 3):
            return self.evaluatePredifined(not isMax)

        #calulate each level
        if(isMax== True):
            bestValue = -1000000.0
            y,x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        self.board[y+i][x+j]=self.maxPlayer
                        self.expandedNodes+=1
                        newvalue = self.alphabeta(depth+1, (3*i+j),alpha, beta, not isMax)

                        if(newvalue>bestValue):
                            bestValue = newvalue
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                                #print("set new move")
                        alpha = max(alpha, newvalue)
                        self.board[y+i][x+j] = '_'
                        if(alpha>= beta):
                            break
        else:
            bestValue = 1000000.0
            y, x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        self.board[y+i][x+j]=self.minPlayer
                        self.expandedNodes+=1
                        newvalue = self.alphabeta(depth+1, (3*i+j),alpha, beta, not isMax)
                        if(newvalue < bestValue):
                            bestValue = newvalue
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                        alpha = min(alpha, newvalue)
                        self.board[y+i][x+j] = '_'
                        if(alpha>=beta):
                            break
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        #bestValue=0.0

        #we only goes to the thrid level in recursion
        if(depth == 3):
            return self.evaluatePredifined(not isMax)

        #calulate each level
        if(isMax== True):
            #print(self.board)
            bestValue = -1000000.0
            y,x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        #print("cur best", bestValue)
                        self.board[y+i][x+j]=self.maxPlayer
                        self.expandedNodes+=1
                        #self.printGameBoard()
                        newvalue = self.minimax(depth+1, (3*i+j), not isMax)
                        #print("cur new move", newvalue, " ",x+i, y+j)
                        #print("depth now", depth)
                        #if(depth == 0):
                        #    print(newvalue, bestValue)
                        if(newvalue>bestValue):
                            bestValue = newvalue
                            #if(depth == 2):
                            #    print("update!!!!", bestValue)
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                                #print("set new move")
                        #self.printGameBoard()

                        self.board[y+i][x+j] = '_'
                        #print("goes here")
        else:
            bestValue = 1000000.0
            y, x = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if(self.board[y+i][x+j]=='_'):
                        self.board[y+i][x+j]=self.minPlayer
                        self.expandedNodes+=1
                        #self.printGameBoard()
                        newvalue = self.minimax(depth+1, (3*i+j), not isMax)
                        #if(depth == 1):
                        #    print("depth is 1",newvalue, bestValue)
                        if(newvalue < bestValue):
                            bestValue = newvalue
                            #print("depth now", depth)
                            if(depth == 0):
                                self.bmove = [y+i, x+j]
                        #self.printGameBoard()
                        self.board[y+i][x+j] = '_'


        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes=[]

        currBoardIdx = self.startBoardIdx

        if(maxFirst == True):
            self.currPlayer = True
        else:
            self.currPlayer = False

        while(True):
            #print("new step")

            if(self.checkMovesLeft == False):
                winner = self.checkWinner()
                break

            if((self.checkWinner() == 1) or (self.checkWinner() == -1)):
                winner = self.checkWinner()
                break
            #max's turn
            if(self.currPlayer == True):
                if(isMinimaxOffensive == True):
                    bvalue = self.minimax(0, currBoardIdx, self.currPlayer)
                    #print("here",self.printGameBoard())
                else:
                    bvalue = self.alphabeta(0, currBoardIdx, -10000000.0,10000000.0 , self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                print("bestmove max", bestMove)

                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #print("here")                
                #self.board[self.bmove[0]][self.bmove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer
                #print("print move", bestMove)
                #self.board = self.clearboard.copy()
                #for i in range(9):
                #    for j in range(9):
                #        self.board[i][j] = self.clearboard[i][j]

                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            else:
                if(isMinimaxDefensive == True):
                    bvalue = self.minimax(0, currBoardIdx, self.currPlayer)
                else:
                    bvalue = self.alphabeta(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #self.board[self.bmove[0]][self.bmove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer
                #print("print move", bestMove)

                #for i in range(9):
                #    for j in range(9):
                #        self.board[i][j] = self.clearboard[i][j]
                #self.printGameBoard()
            
                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            #sleep(1)
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self,maxFirst,ispreOffensive,ispreDefensive):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes=[]

        currBoardIdx = self.startBoardIdx

        if(maxFirst == True):
            self.currPlayer = True
        else:
            self.currPlayer = False

        while(True):
            #print("new step")

            if(self.checkMovesLeft == False):
                winner = self.checkWinner()
                break

            if((self.checkWinner() == 1) or (self.checkWinner() == -1)):
                winner = self.checkWinner()
                break
            #max's turn
            if(self.currPlayer == True):
                if(ispreOffensive == True):
                    #print("pre!!!")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0,10000000.0 , self.currPlayer)
                    #print("here",self.printGameBoard())
                else:
                    #print("not supposed to be pre")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0,10000000.0 , self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                print("bestmove max", bestMove)

                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #print("here")                
                #self.board[self.bmove[0]][self.bmove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer

                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            else:
                if(ispreDefensive == True):
                    #print("not suppose to be mine")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0,10000000.0 , self.currPlayer)
                else:
                    #print("mine")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #self.board[self.bmove[0]][self.bmove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer

            
                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            #sleep(1)
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameHuman(self,maxFirst,ishumanOffensive,ishumanDefensive):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes=[]

        currBoardIdx = self.startBoardIdx

        if(maxFirst == True):
            self.currPlayer = True
        else:
            self.currPlayer = False

        while(True):
            #print("new step")

            if(self.checkMovesLeft == False):
                winner = self.checkWinner()
                break

            if((self.checkWinner() == 1) or (self.checkWinner() == -1)):
                winner = self.checkWinner()
                break
            #max's turn
            if(self.currPlayer == True):
                if(ishumanOffensive == True):
                    #print("pre!!!")
                    bvalue = self.human(currBoardIdx)
                    #print("here",self.printGameBoard())
                else:
                    #print("not supposed to be pre")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0,10000000.0 , self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                print("bestmove max", bestMove)

                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #print("here")                
                #self.board[self.bmove[0]][self.bmove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer

                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            else:
                if(ishumanDefensive == True):
                    #print("not suppose to be mine")
                    bvalue = self.human(currBoardIdx)
                else:
                    #print("mine")
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #self.board[self.bmove[0]][self.bmove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer

            
                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            #sleep(1)
        return gameBoards, bestMove, expandedNodes, bestValue, winner
        #YOUR CODE HERE
        #bestMove=[]
        #gameBoards=[]
        #winner=0
        #return gameBoards, bestMove, winner

    def human(self, currBoardIdx):
        print("hey bro, your turn")
        print("you should play in block#", currBoardIdx)
        x = int(input(("Please enter x: ")))
        y = int(input(("Please enter y: ")))
        self.bmove =(x, y) 
        return 0



    def playGamePredifinedAgent_extracredit(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes=[]

        currBoardIdx = self.startBoardIdx

        if(maxFirst == True):
            self.currPlayer = True
        else:
            self.currPlayer = False

        while(True):
            #print("new step")
            winnermax_count = 0
            winnermin_count = 0
            if(self.checkMovesLeft == False):
                winner = self.checkWinner()
                break

            if((self.checkWinner() == 1)):
                winnermax_count +=1
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x
                fullblock = self.globalIdx[currBoardIdx]
                m,n = fullblock
                for i in range(3):
                    for j in range(3):
                        if(self.board[n+i][m+j] == '_'):
                            self.board[n+i][m+j] = '*'

                if(winnermax_count == 3):
                    winner = 1
                    break
            if((self.checkWinner() == -1)):
                winnermin_count -=1
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x
                fullblock = self.globalIdx[currBoardIdx]
                m,n = fullblock
                for i in range(3):
                    for j in range(3):
                        if(self.board[n+i][m+j] == '_'):
                            self.board[n+i][m+j] = '*'
                if(winnermin_count == 3):
                    winner = -1
                    break
             # if(self.checkWinner() == -1):
             #    winnermin_count -=1
             #    y,x = self.bmove
             #    while(True):
             #        if(y>=3):
             #            y=y-3
             #        if(x>=3):
             #            x=x-3
             #        if(x<3 and y<3):
             #            break
             #    currBoardIdx = 3*y+x
             #    removeidx = self.globalIdx(currBoardIdx)
             #    self.globalIdx.remove(removeidx)
             #    if(winnermin_count == 3):
             #        winner = -1
             #        break                   
            #max's turn
            if(self.currPlayer == True):
                if(isMinimaxOffensive == True):
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)
                    #print("here",self.printGameBoard())
                else:
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                print("bestmove max", bestMove)

                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #print("here")                
                #self.board[self.bmove[0]][self.bmove[1]] = self.maxPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer
                #print("print move", bestMove)
                #self.board = self.clearboard.copy()
                #for i in range(9):
                #    for j in range(9):
                #        self.board[i][j] = self.clearboard[i][j]

                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            else:
                if(isMinimaxDefensive == True):
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)
                else:
                    bvalue = self.alphabetadesigned(0, currBoardIdx, -10000000.0, 10000000.0, self.currPlayer)

                bestMove.append(self.bmove)
                expandedNodes.append(self.expandedNodes)
                bestValue.append(bvalue)
                y,x = self.bmove
                while(True):
                    if(y>=3):
                        y=y-3
                    if(x>=3):
                        x=x-3
                    if(x<3 and y<3):
                        break
                currBoardIdx = 3*y+x

                #self.board[self.bmove[0]][self.bmove[1]] = self.minPlayer
                gameBoards.append(self.board)
                self.currPlayer = not self.currPlayer
                #print("print move", bestMove)

                #for i in range(9):
                #    for j in range(9):
                #        self.board[i][j] = self.clearboard[i][j]
                #self.printGameBoard()
            
                if(maxFirst == True):
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.maxPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.minPlayer
                            i+=1
                else:
                    i=0
                    for [y,x] in bestMove:
                        if(i%2 == 0):
                            self.board[y][x] = self.minPlayer
                            i+=1
                        else:
                            self.board[y][x] = self.maxPlayer
                            i+=1
                self.printGameBoard()
            #sleep(1)
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def fake(self):
        self.board=[['0','*','X','_','X','0','0','*','X'],
                    ['*','X','*','_','_','_','*','*','X'],
                    ['X','*','0','_','_','0','0','*','X'],
                    ['X','_','_','_','0','_','_','_','_'],
                    ['_','_','_','_','_','_','0','_','_'],
                    ['_','_','0','_','_','_','_','_','X'],
                    ['X','*','0','_','_','_','0','X','0'],
                    ['*','X','*','_','_','_','X','X','0'],
                    ['0','*','X','_','_','X','X','0','0']]
        self.printGameBoard()
        return 1


if __name__=="__main__":
    uttt=ultimateTicTacToe()
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGameYourAgent(True,True,False)
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGameHuman(True,True,False)
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent_extracredit(True,False,False)
    winner= uttt.fake()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
