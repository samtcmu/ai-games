class Model:
    def __str__(self):
        raise Exception, "Model subclasses must implement __str__."

    def ActionForPosition(self, position):
        raise Exception, "Model subclasses must implement ActionForCurrentPosition."

    def Update(self, initial_position, action, final_position, reward, score):
        raise Exception, "Model subclasses must implement Update."
