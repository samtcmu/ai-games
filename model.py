import picking_cans_board

class Model:
    def __str__(self):
        raise Exception, "Model subclasses must implement __str__."

    def SaveToFile(self, filename):
        raise Exception, "Model subclasses must implement SaveToFile."

    def LoadFromFile(self, filename):
        raise Exception, "Model subclasses must implement LoadFromFile."

    def ActionForState(self, state):
        raise Exception, "Model subclasses must implement ActionForState."

    def Update(self, initial_position, action, final_position, reward, score):
        raise Exception, "Model subclasses must implement Update."
