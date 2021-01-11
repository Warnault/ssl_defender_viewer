import abc


class AlgoSolver(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def solver(self):
    pass

  def chercheDefenders(self, tabDef):
    res = []
    for defender in tabDef:
      res.append(self.list_name_of_defencers.get(defender))
    return res

  def createListKickAndDef(self):
    for key in self.dictNeighbors :
      if "D" in key : 
        self.list_defender.append(key)
      elif "T" in key:
        self.list_kick.append(key)
      else :
        self.list_goal.append(key)