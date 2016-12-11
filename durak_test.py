import durak

def gameflow_test():
  player1 = [durak.Card(13,0), durak.Card(7,1), durak.Card(7,2)]
  player2 = [durak.Card(6,0), durak.Card(8,1), durak.Card(9,2)]
  game = durak.GameState(player1, player2)

  assert game.table == {}
  assert game.attack(1) == True 
  assert len(game.table.keys()) == 1
  assert game.attack(1) == True
  assert len(game.table.keys()) == 2

  defending_suit = game.table.keys()[0].suit
  defending_card = filter(lambda card: card.suit is defending_suit,player2)[0]
  defending_index = player2.index(defending_card)
  assert game.defend(defending_index,0) == True
  assert len(filter(lambda card: card is not None, game.table.values())) == 1
  assert game.defend(1,1) == True
  assert len(filter(lambda card: card is not None, game.table.values())) == 2
  assert game.attack(0) == False
  assert len(game.table.keys()) == 2
  assert game.clear() == True
  assert game.table == {}
  assert game.attacker == player2
  assert game.attack(0) == True
  assert len(game.table.keys()) == 1
  assert player2 == []
  
def test_pickup():
  player3 = [durak.Card(13,0), durak.Card(7,1), durak.Card(7,2)]
  player4 = [durak.Card(6,0), durak.Card(8,1), durak.Card(9,2)]
  game1 = durak.GameState(player3, player4)
  assert game1.attack(1) == True
  assert game1.attack(1) == True
  assert game1.pickup() == True
  assert player3.__repr__() == "[|13 of suit 0|]"
  assert game1.table == {}

def test_bounce():
  player5 = [durak.Card(13,0), durak.Card(7,1), durak.Card(7,2)]
  player6 = [durak.Card(6,0), durak.Card(7,3), durak.Card(9,2)]
  game2 = durak.GameState(player5, player6)

  game2.attack(1)
  game2.attack(1)
  assert game2.bounce(0) == False
  assert game2.bounce(1) == True


  
