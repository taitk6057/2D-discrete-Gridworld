import numpy as np
import math
import random
import matplotlib
import matplotlib.pyplot as plt

# main function
# read in map, starting state, inputs, p_e
# from map read x_max, y_max, obstacles
# run function, returns outputs

# GLOBALS
p_e = 0  # probability of error
x_max = 5  # bounds of map
y_max = 5
o_max = math.ceil(np.sqrt(x_max ** 2 + y_max ** 2))

R_D = [2, 2]  # ice cream shop locations
R_S = [2, 0]
obstacles = [[1, 1], [2, 1], [1, 3], [2, 3]]  # obstacles


#---------------------
#Things the simulation can access

action_space = ['L', 'R', 'U', 'D', 'S']
state_space = [[x,y] for x in range(x_max) for y in range(y_max)]
observation_space = range(0,o_max+1)
# check if the resulting movement is allowable
def isValid(current_state):
    # check for edges
    if current_state[0] >= x_max or current_state[1] >= y_max or current_state[0] < 0 or current_state[1] < 0:
      #print("bound")
      return False

    # check for obstacles
    if current_state in obstacles:
     #print("obstacle")
      return False

    # if you get here it is valid
    return True


def P(nextState, currentState, action):
  actionToMove = [[-1,0], [1,0], [0,1], [0,-1], [0,0]]
  if not isValid(nextState): # neccesary because of math
    #add probability to stay still 
    return 0
  if action == 'S' and nextState == 'currentState':
    return 1
  elif action =='S':
    return 0
  movement = np.subtract(nextState,currentState)
  if(movement[0] > 1 or movement[1] > 1):
    return 0
  index = action_space.index(action)
  if (movement[0] == actionToMove[index][0] and movement[1] == actionToMove[index][1]):
    return 1-p_e
  else:
     return p_e/4

# returns observation
# TODO: incorporate the rounding
def O(state):

    # need to make sure we aren't dividing by zero
    if state == R_S:
        inverse_d_S = 0
    else:
        # python handles ^2 differently than **2
        inverse_d_S = 1 / (np.sqrt((state[0] - R_S[0]) ** 2 + (state[1] - R_S[1]) ** 2))
    if state == R_D:
        inverse_d_D = 0
    else:
        inverse_d_D = 1 / (np.sqrt((state[0] - R_D[0]) ** 2 + (state[1] - R_D[1]) ** 2))
    h = 2 / (inverse_d_S + inverse_d_D)
    o = 0
    # move some of this
    rand = random.random()
    if (rand <= 1 - (math.ceil(h) - h)):
        o = math.ceil(h)
    else:
        o = math.floor(h)
    return o
#--------------------------


#---------------------
#The simulation

def getNextState(action, currentState):
  total = 0
  x = random.random() 
  print(x)
  for item in state_space:
    prob = P(item, currentState, action)
    if prob != 0:
      total += prob
      if total > x: #using cdf: if total passes the randomly generated value, then return for that specific item value- this is the next state
        return item
  return currentState # neeed to remove

#TODO
def getNextObservation(action, currentState):
  total = 0
  x = random.random() 
  print(x)
  for item in state_space:
    prob = P(item, currentState, action)
    if prob != 0:
      total += prob
      if total > x: #using cdf: if total passes the randomly generated value, then return for that specific item value- this is the next state
        return item
  return currentState #need to removee
  

def runSimulation():
  state = [0, 0]
  while 1:
      userInput = input("Where you want to move: ")
      
      state = getNextState(userInput, state)
      output = O(state)
      #return [state,output]
      print(state)
      print(output)
      
def AutoRunSimulation(userInput, state):
  state = getNextState(userInput, state)
  output = O(state)
  return [state,output]
      
 
def runMultipleTimes():
  state = [0, 0]
  userInput = "RRURUUL"
  actualStateX = [0]
  actualStateY = [0]
  actualOutput = []
  
  #grid = [[0,0,0,0,0]
          #[0,0,0,0,0]
          #[0,0,0,0,0]
          #[0,0,0,0,0]
          #[0,0,0,0,0]] """
  number = len(userInput)
  for x in userInput:
    state = getNextState(x, state)
    actualStateX.append(state[0])
    actualStateY.append(state[1])
    actualOutput.append(O(state))
  
  fig = plt.figure(1)
  plt.xlim(0,4)
  plt.ylim(0,4)
  plt.plot(actualStateX,actualStateY)
  fig.savefig("graph.png")
  plt.close(fig)  
    
      
#runSimulation()
runMultipleTimes()
