import durak
import anytree
import copy
import pprint

class GameStateNode(durak.GameState,anytree.NodeMixin):
  def __init__(self, player1, player2, table=None, parent=None):
    super(durak.GameState, self).__init__()
    durak.GameState.__init__(self,player1,player2,table)
    self.parent = parent
    self.history = ["Created"]

  def __repr__(self):
    return "Player 1: {} Player 2: {} Table: {} Last: {}".format(self.player1, self.player2, self.table, self.last_move)

  def createChildren(self):

## quick check
#    if "clear" in self.last_move or "bounce" in self.last_move:   
#      return

##    
    for child in self.children:
      child.parent = None
    template = copy.deepcopy(self)

    for card_index in range(len(self.attacker)):
      temp = copy.deepcopy(template)
      if temp.attack(card_index):
        temp.parent = self 
        temp.history.append("attack " + str(card_index))

    for defender_card_index in range(len(self.defender)):
      for attacker_card_index in range(len(self.table.keys())):
        temp = copy.deepcopy(template)
        if temp.defend(defender_card_index,attacker_card_index):
          temp.parent = self 
          temp.history.append("defend " + str(defender_card_index) + " " + str(attacker_card_index))

    if None in self.table.values(): 
      temp = copy.deepcopy(template)
      if temp.pickup():
        temp.parent = self 
        temp.history.append("pickup")

    for card_index in range(len(self.defender)):
      temp = copy.deepcopy(template)
      if temp.bounce(card_index):
        temp.parent = self 
        temp.history.append("bounce " + str(card_index))

    temp = copy.deepcopy(template)
    if temp.clear():
        temp.parent = self 
        temp.history.append("clear")


  def createTree(self):
    self.createChildren()
    for node in self.children:
     # if len(node.path) < 10: 
      print "processing a node at depth "+str(len(node.path))
      if node.check_win():
        node.history.append(node.check_win() + " wins!")
        pprint.pprint(node.history)
      else: 
        pprint.pprint(node.history)
        node.createTree()    
