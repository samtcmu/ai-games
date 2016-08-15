import model

class ReinforcementLearningModel(model.Model):
    def __init__(self):
        q_matrix = None

    def __str__(self):
        raise Exception, "TODO(samtet)"

    def ActionForPosition(self, position):
        raise Exception, "TODO(samtet)"

    def Update(self, initial_position, action, final_position, reward, score):
        raise Exception, "TODO(samtet)"

    def Train(rows=10, columns=10, games=200, actions_per_game=200):
        raise Exception, "TODO(samtet)"
