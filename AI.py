import copy
import soft_config_const as const
import Helper as Helper
import sys
import math

#orig_stdout = sys.stdout
#f = open('out.txt', 'w')
#sys.stdout = f


class Nod:
  '''
  Nod class. informatie contains the status of the board (the pieces positions and the rolls). Probability is the chance to 
  reach the node.
  '''
  def __init__(self, informatie, turn, color = None, probability = 0):
    self.informatie = informatie
    self.turn_ = turn
    self.probability = probability
    self.color_that_needs_to_play = color

  def __str__(self):
    return f"Informatie: {self.informatie}, Turn: {self.turn_}, Probability: {self.probability}, Culoarea: {self.color_that_needs_to_play}"

  def turn(self):
     return self.turn_
    
  def get_information(self):
     return self.informatie

  def get_player(self):
     return self.color_that_needs_to_play

  def get_chances(self):
     return self.probability
  

class Euristics():

   def endgame_simple_euristic(board):
      '''
      Simple euristic for the endgame. If the are no pieces that can capture each other under any circumstances
      then the whole game becomes a race, the way the pieces are placed on a position doesn't matter anymore, the only
      thing that is being rewarded is getting a piece out and having a piece in your home.
      '''
      value_max = 0
      value_min = 0
      white_pieces = 0
      black_pieces = 0
      for i in range(1, 25):
        if len(board[i]) > 0:
           if(board[i][0] == 'W'):
              segm = Euristics.get_segment_for_position(i, 'MAX')
              if segm >= 7:
                 value_max += 3
              white_pieces += len(board[i])
           else:
              segm = Euristics.get_segment_for_position(i, 'MIN')
              if segm >= 7:
                 value_min += 3
              black_pieces += len(board[i])
      
      value_max += (15- white_pieces) * 10
      value_min += (15- black_pieces) * 10

      return (value_max - value_min) * 0.01
 
   def get_segment_for_position(position, player):
      '''
      The board is separated into 8 equal segments. The first one is where the farthest pieces are situated, and the last one is 
      the most far away from the first one.
      '''
      start_1 = 24
      start_2 = 22
      value_assigned_to_segment = 0

      while not (position<=start_1 and position>=start_2):
            value_assigned_to_segment +=1
            start_1 -= 3
            start_2 -= 3

      if player == 'MAX':
         return value_assigned_to_segment
      else:
         return 7-value_assigned_to_segment


   def position_value(board):
    '''
    Main euristic used during the game. It takes in consideration the following:
      The risk of a piece being captured
      The way the pieces are structured on a position (e.g. tower of 2, tower of 3 )
      The number of pieces that are taken out
      The position of a piece (the segment where it is situated)
      The number of pieces taken out by the enemy, and the possibilites of it being able to get in home.

      I want to write a more in depth explication in the repository readme of the euristic.

    '''
    value_max = 0
    value_min = 0

    last_poz_white = 0  
    last_poz_black = 25
    white_pieces = 0
    black_pieces = 0
    for i in range(0, 26):
       if len(board[i]) > 0:
         if(board[i][0] == 'W'):
            white_pieces += len(board[i])
            last_poz_white = max(last_poz_white, i)
         else:
            black_pieces += len(board[i])
            last_poz_black = min(last_poz_black, i)

    if last_poz_black > last_poz_white:
      return Euristics.endgame_simple_euristic(board)
      
    value_max += 4 * (15 - white_pieces)  # Piese scoase
    value_min += 4 * (15 - black_pieces)
    
    risk = Euristics.get_risk(board) 

    for i in range(1, 25):
        if len(board[i]) > 0:
            if board[i][0] == 'W':
               segment = Euristics.get_segment_for_position(i, 'MAX')
               #print(f" {i} -- > {segment}")
               if len(board[i]) == 1:
                     #print(risk[i] * 0.5 * segment * math.log(segment+1))
                  value_max -= risk[i] * 0.2 * segment * math.log(segment+1)
               if len(board[i]) >= 2:
                  value_max += 3
                  if len(board[i]) > 4:
                        value_max -= 0.4*(len(board[i]) - 4)
                  
               value_max += segment * 0.25

            else:
                segment = Euristics.get_segment_for_position(i, 'MIN')
                #print(segment)
                if len(board[i]) == 1:
                  # print(risk[i] * 0.5 * segment * math.log(segment+1))
                   value_min -= risk[i] * 0.2 * segment * math.log(segment+1)

                if len(board[i]) >= 2:
                    value_min += 3
                    if len(board[i]) > 4:
                        value_min -= 0.4*(len(board[i]) - 4)

                value_min += segment * 0.25

    count_blocked_min = 0
    count_blocked_max = 0
    if len(board[0]) != 0:
       for i in range(1,7):
          if len(board[i]) > 1 and board[i][0] == 'W':
             count_blocked_min +=1

    if len(board[25]) != 0:
       for i in range(18,25):
          if len(board[i]) > 1 and board[i][0] == 'B':
             count_blocked_max +=1
    
    if count_blocked_max > 0:
      value_max -= len(board[25]) * count_blocked_max * math.log(count_blocked_max) * 1

    if count_blocked_min > 0:
      value_min -= len(board[0]) * count_blocked_min * math.log(count_blocked_min) * 1

    #print(f" max -> {count_blocked_max} min -> {count_blocked_min}")

    evaluation = (value_max - value_min) * 0.01
    #if ( evaluation > 100 ) or (evaluation < -100):
      #print(f"board: {board}, eval : {evaluation} maybe? {100 > float("inf")}")

    return evaluation

   def get_risk(board):
      '''
      Assignates a risk value for every piece on the board that is alone.
      '''
      risk_list = [0]
      for i in range(1,25):
         risk_value = 0
         if len(board[i]) > 0:
            if len(board[i]) == 1: #Not taking in consideration doubles like 5,5. If a roll like 5,5 is the only way for the piece to be captured, then the AI should take it as a viable move, because in real life sometimes it's better to assume this risk to develop faster
               if board[i][0] == 'B':
                  for j in range(i, min(26,i+12)):    
                     if len(board[j]) > 0 and board[j][0] != board[i][0]:
                        if abs(i-j) > 6:
                           risk_value += 0.5
                        else:
                           risk_value +=1
               else:
                  for j in range(max(0, i-12), i):
                     if len(board[j]) > 0 and board[j][0] != board[i][0]:
                        if abs(i-j) > 6:
                           risk_value += 0.5
                        else:
                           risk_value +=1
         risk_list.append(risk_value)
      return risk_list






class Graph_Class:
  def __init__(self, Info_Start_Node):
    '''
    The network. Virtual Assistant is a virtual instance of the Game that is used for its utilitary functions.
    '''
    self.Starting_Node = Nod(Info_Start_Node[0],Info_Start_Node[1],Info_Start_Node[2])
    self.Virtual_Assistant = Helper.Virtual_App()
    self.child_nodes = []

  def get_euristics(self, node): 
    '''
    return euristics for a node
    '''
    board = node.get_information()[0]

    return Euristics.position_value(board)
    #return self.ve[informatieNod]

  def scop(self, node):
     '''
     Check win condition
     '''
     board = node.get_information()[0]
     whites = 0
     blacks = 0
     for pieces in board:
         whites += pieces.count('W')
         blacks += pieces.count('B')
     
     return (whites == 0) or (blacks == 0)

  def succesori(self, node):
    '''
    Gets the succesors. For a CHANCE node, it generated the maximum or the minimum nodes that are to be followed.
    For a MIX/MAX chance it generates all the possibilites to roll the dice.
    '''
    self.child_nodes = []
    if node.turn() == 'CHANCE':
       for rolls in const.ALL_POSSIBLE_ROLLS:
          roll_probability = 1/18
          if len(rolls) == 4:
             roll_probability = 1/36
          info = node.get_information()
          board = info[0]
          incoming = 'MIN'
          if node.get_player() == 'W':
             incoming = 'MAX'
          New_Node = Nod((board,rolls),incoming, node.get_player(), roll_probability)
          self.child_nodes.append(New_Node)
    else:
       info = node.get_information()
       board = info[0]
       rolls = info[1]   
       incoming = 'CHANCE'
       next_player = 'W'
       if node.get_player() == 'W':
          next_player = 'B'
       for state in self.Virtual_Assistant.get_all_moves(board,node.get_player(),rolls):
          New_Node = Nod((state,rolls),incoming,next_player)
          self.child_nodes.append(New_Node)

    return self.child_nodes


class Engine():
  positive_infinity = float('inf')
  negative_infinity = float('-inf')
  def __init__(self, depth):
    '''
    The Engine which will basically be the AI. The algorithm will be here.
    '''
    self.DEPTH = depth
    pass
   
  def get_prediction_for(self, state, turn, piece_color, roll):
    '''
    Method for the exterior for its purpose to be called.
    '''
    self.Graph = Graph_Class(((state,roll),turn,piece_color))
    
    _, Optimal_Move = self.expectiminimax(self.Graph.Starting_Node, self.DEPTH)
    print(_)

    return Optimal_Move 

  def expectiminimax(self, node, depth):
    '''
    Expectiminimax. MAX/MIN node --> Get MAX/MIN from children
    CHANCE node --> SUM of the value returned from the child * the probability of reaching that child
    '''
    board_answer = node.get_information()[0]
    chil_length = 0
    if self.Graph.scop(node) == True or depth == 0:
        return self.Graph.get_euristics(node), node.get_information()[0]
    if node.turn() == 'MIN':
        α = Engine.positive_infinity
        for child in self.Graph.succesori(node):
            chil_length +=1
            Child_Minimax, Child_layout = self.expectiminimax(child, depth-1)
            if Child_Minimax < α and Child_Minimax != Engine.negative_infinity:
               α = Child_Minimax
               board_answer = Child_layout   
        if α == Engine.positive_infinity: # BAD STATE, NO POSSIBLE MOVES
            α = 10
    elif node.turn() == 'MAX':
        α = Engine.negative_infinity
        for child in self.Graph.succesori(node):
            chil_length += 1
            Child_Minimax, Child_layout = self.expectiminimax(child, depth-1)
            if Child_Minimax > α and Child_Minimax != Engine.positive_infinity:
               α = Child_Minimax
               board_answer = Child_layout   
        if α == Engine.negative_infinity:
           α = -10 #BAD STATE, NO POSSIBLE MOVES

        #if α == Engine.negative_infinity:
         #  α = 0
    else:
        α = 0
        for child in self.Graph.succesori(node):
            chil_length += 1
            α = α + (child.get_chances() * self.expectiminimax(child, depth-1)[0])
    #print(f"{depth} --> {node} --> {α} --> cu {chil_length} copii")
    return α, board_answer
  
#AI_MODEL = Engine(1)
#print(AI_MODEL.get_prediction_for([[], ['B'], [], [], [], ['W', 'W'], ['W', 'W', 'W'], ['B'], ['W', 'W', 'W', 'W'], [], [], [], ['B', 'B', 'B'], ['W', 'W', 'W','W'], [], [], ['B'], ['B', 'B', 'B', 'B'], [], ['B', 'B', 'B', 'B', 'B'], [], [], [], [], ['W', 'W'], []], 'MAX', 'W', [2,6]))

#sys.stdout = orig_stdout
#f.close()

board_1 = [['B'], ['W','W'], ['W'], ['W','W'], [], [], ['W', 'W'], ['B','B'], ['W', 'W'], ['W','W'], [], [], ['B','B','B'], ['W', 'W'], [], [], [], ['B'], ['W'], ['B', 'B'], ['B'], ['B','B'], ['B'], ['B','B'], ['W'], []]


board_2 = [['B','B'], ['W'], ['W','W'], ['W','W'], [], [], ['W', 'W'], ['B','B'], ['W', 'W'], ['W','W'], [], [], ['B','B','B'], ['W', 'W'], [], [], [], ['W'], [], ['B', 'B'], ['B'], ['B','B'], ['B'], ['B','B'], ['W'], []]
print(f"Board 1 : {Euristics.position_value(board_1)}, Board 2: {Euristics.position_value(board_2)}")