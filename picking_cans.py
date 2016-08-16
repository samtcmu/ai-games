import genetic_algorithm_model
import picking_cans_board
import reinforcement_learning_model

def genetic_algorithm(actions=None):
    if actions is None:
        print genetic_algorithm_model.Train(
            rows=10,
            columns=10,
            generations=500,
            population_size=200,
            games=200,
            actions_per_game=200)
    else:
        model = genetic_algorithm_model.GeneticAlgorithmModel(actions=actions)
        board = picking_cans_board.Board(10, 10)
        board.Randomize()
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)

def reinforcement_learning(train_model=True, q_matrix=None):
    if train_model:
        print reinforcement_learning_model.Train(
            rows=10,
            columns=10,
            games=1000000,
            actions_per_game=200,
            learning_rate=0.1,
            discount_rate=0.99,
            verbose=True)
    else:
        if q_matrix:
            model = reinforcement_learning_model.ReinforcementLearningModel(
                0.1, 1.0, q_matrix=q_matrix)
        else:
            model = reinforcement_learning_model.ReinforcementLearningModel(0.1, 1.0)
        board = picking_cans_board.Board(10, 10)
        board.Randomize()
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)
