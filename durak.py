#!/usr/bin/python

class Card(object):
  def __init__(self, rank, suit):
    """
    Suit 0 (zero) is trump, other values represent other suits without restriction.
    Ranks must be able to be compared with < and >, therefor eintegers are recommended: J is 11, Q is 12, and so on...
    The Jokers are Card(15,0) and Card(16,0).
    """
    self.rank = rank
    self.suit = suit

  def __repr__(self):
    return "|{} of suit {}|".format(self.rank, self.suit)

class GameState(object):
  def __init__(self, player1, player2, table=None):
    self.player1 = player1
    self.player2 = player2
    self.attacker = self.player1
    self.defender = self.player2
    if table is None:
      table = {}
    self.table = table

  def is_attacker(self, player):
    if player is self.attacker:
      return "*"
    else:
      return ""

  def __repr__(self):
    return "{}Player 1: {} Player 2: {} Table: {}".format(self.is_attacker(self.player1), self.player1, self.is_attacker(self.player2), self.player2 ,self.table)

  def attack(self, index):
    if len(self.table) >= 6 or len(self.table) >= len(self.defender):
      return False
    if self.table == {} or self.attacker[index].rank in [card.rank for card in self.table.keys()] or self.attacker[index].rank in [card.rank for card in filter(lambda card: card is not None,self.table.values())]:
      self.table[self.attacker.pop(index)] = None 
      return True

  def _end_turn(self):
      if self.attacker is self.player1:
        self.attacker = self.player2
        self.defender = self.player1
      else:
        self.attacker = self.player1
        self.defender = self.player2

  def defend(self, defending_index, attacking_index):
    if None in self.table.values():
      attacking_card = self.table.keys()[attacking_index]
      defending_card = self.defender[defending_index]
      if (self.table[attacking_card] == None) and (defending_card.suit == attacking_card.suit or attacking_card.suit > 0 and defending_card.suit == 0 ) and defending_card.rank > attacking_card.rank:
        self.table[attacking_card] = defending_card
        self.defender.remove(defending_card)
        return True
      else:
        return False
    else:
      return False

  def pickup(self):
    if len(self.table) > 0:
      self.defender.extend(self.table.keys())
      self.defender.extend(filter(lambda card: card is not None,self.table.values()))
      self.table = {}
      return True
    else:
      return False

  def clear(self):
    if (None not in self.table.values()) and (self.table <> {}):
      self.table = {}
      self._end_turn()
      return True
    else:
      return False
      
  def bounce(self,index):
    bounce_card = self.defender[index]
    if self.table <> {} and False not in [card.rank == bounce_card.rank and self.table[card] == None for card in self.table.keys()] and len(self.table) < self.attacker:
      self.table[bounce_card] = None
      self.defender.remove(bounce_card)
      self._end_turn()
      return True
    else:
      return False

  def check_win(self):
    if len(self.player1) == 0:
      return "Player1"
    elif len(self.player2) == 0:
      return "Player2"
    else:
      return None
    
    
