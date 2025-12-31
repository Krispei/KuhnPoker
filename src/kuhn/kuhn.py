class KuhnPoker:

  def __init__(self): 
    
    self.cards = [0,1,2] #three cards, Jack, Queen, or King

    self.actions = ['p', 'b'] #two actions, passing/folding or bet/calling

  def isGameFinished(self, history):

    if history == 'bb' : return True 
    if history == 'pp' : return True
    if history == 'pbb' : return True
    if history == 'bp' : return True
    if history == 'pbp' : return True

    return False

  def getPlayerToAct(self, history):

    if len(history) == 0 or len(history) == 2 : return 0
    if len(history) == 1: return 1

  def getPayouts(self, history, cards): 

    if self.isGameFinished(history):

      # Uncontested cases
      if history == 'bp': return 1
      if history == 'pbp': return -1

      #showdown cases
      p1_card = cards[0]
      p2_card = cards[1]

      if history == 'pp' : return 1 if p1_card > p2_card else -1
      if history == 'bb' or history == 'pbb' : return 2 if p1_card > p2_card else -2

    return 0

  def getActions(self):

    return self.actions
