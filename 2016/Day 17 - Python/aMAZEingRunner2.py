import hashlib
import queue


WIDTH = 4
HEIGHT = 4
startPos = [0,3]

SALT = "qtetzkpl"
#"qtetzkpl"
#"ulqzkmiv" 
#"kglvqrro" 
#"ihgpwlah"

class State:
	position = None #position = [x,y]
	path = ""
	hval = ""

	def __init__(self,position,path):
		self.position = position
		self.path = path
		self.hval = self.hash()

	def pathLength(self):
		return len(self.path)

	def isGoalState(self):
		return self.position[0] == 3 and self.position[1] == 0

	def nextStates(self):
		nextStates = list()
		
		#up
		if self.position[1] < 3 and self.hval[0] in ["b","c","d","e","f"]: #open
			nextStates.append(State([self.position[0], self.position[1] + 1], self.path + "U"))
		#down
		if self.position[1] > 0 and self.hval[1] in ["b","c","d","e","f"]: #open
			nextStates.append(State([self.position[0], self.position[1] - 1], self.path + "D"))
		#left
		if self.position[0] > 0 and self.hval[2] in ["b","c","d","e","f"]: #open
			nextStates.append(State([self.position[0] - 1, self.position[1]], self.path + "L"))
		#right
		if self.position[0] < 3 and self.hval[3] in ["b","c","d","e","f"]: #open
			nextStates.append(State([self.position[0] + 1, self.position[1]], self.path + "R"))

		return nextStates

	def hash(self):
	    m = hashlib.md5()
	    m.update(SALT.encode('utf-8'))
	    m.update(self.path.encode('utf-8'))
	    return str(m.hexdigest())

	def toStr(self):
		return "State at: ", self.position, " path: ", self.path, " hash: ", self.hash()[:4]

currState = State(startPos, "")

seen = dict()
paths = list()
longestState = currState
while currState is not None:

    if currState.isGoalState():
        if longestState.pathLength() < currState.pathLength():
            longestState = currState
            print("new longest path: ", longestState.pathLength())
    else:
        if not currState.hval in seen:
            seen[currState.hash()] = 1

            for state in currState.nextStates():
                paths.append(state)

    if len(paths) <= 0: #concurrent => the get function will just block and wait for input
        currState = None
    else:
        currState = paths.pop()


print(longestState.toStr())
print(longestState.pathLength())