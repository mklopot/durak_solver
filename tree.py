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
      card = str(self.attacker[card_index])
      if self.is_attacker(self.player1):
        player = "Player1"
      else:
        player = "Player2"
      if temp.attack(card_index):
        temp.parent = self 
        temp.history.append(player + " attacks with " + card)

    for defender_card_index in range(len(self.defender)):
      for attacker_card_index in range(len(self.table.keys())):
        defender_card = str(self.defender[defender_card_index])
        attacker_card = str(self.table.keys()[attacker_card_index])
        if self.is_attacker(self.player1):
          player = "Player2"
        else:
          player = "Player1"
        temp = copy.deepcopy(template)
        if temp.defend(defender_card_index,attacker_card_index):
          temp.parent = self 
          temp.history.append(player + " defends with " + defender_card + " against " + attacker_card)

    if None in self.table.values(): 
      temp = copy.deepcopy(template)
      if self.is_attacker(self.player1):
          player = "Player2"
      else:
          player = "Player1"
      if temp.pickup():
        temp.parent = self 
        temp.history.append(player + " picks up")

    for card_index in range(len(self.defender)):
      temp = copy.deepcopy(template)
      bounce_card = str(self.defender[card_index])
      if self.is_attacker(self.player1):
          player = "Player2"
      else:
          player = "Player1"
      if temp.bounce(card_index):
        temp.parent = self 
        temp.history.append(player + " bounces with " + bounce_card)

    temp = copy.deepcopy(template)
    if self.is_attacker(self.player1):
        player = "Player1"
    else:
        player = "Player2"
    if temp.clear():
        temp.parent = self 
        temp.history.append(player + " calls clear")


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
