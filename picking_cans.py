import genetic_algorithm_model
import picking_cans_board
import reinforcement_learning_model

def genetic_algorithm(model_file=None, positions=None):
    if model_file is None:
        print genetic_algorithm_model.Train(
            rows=10,
            columns=10,
            generations=500,
            population_size=200,
            games=200,
            actions_per_game=200)
    else:
        if positions is None:
            model = genetic_algorithm_model.GeneticAlgorithmModel(
                filename=model_file)
            board = picking_cans_board.Board(10, 10)
            board.Randomize()
            board.RandomizeCurrentPosition()
            print "score: %d" % (board.PickCansWithModel(
                model, actions_per_game=200, verbose=True),)
        else:
            model = genetic_algorithm_model.GeneticAlgorithmModel(
                filename=model_file)
            board = picking_cans_board.Board(10, 10)
            for position in positions:
                print "position: %d\n" % (position,)
                print board.BoardPositionAsString(position)
                print "action: %s\n" % (
                    picking_cans_board.ACTIONS[model.ActionForPosition(position)][1],)

def reinforcement_learning(train_model=True, model_file=None):
    if train_model:
        print reinforcement_learning_model.Train(
            rows=10,
            columns=10,
            games=1000000,
            actions_per_game=200,
            learning_rate=0.1,
            discount_rate=0.9,
            verbose=True)
    else:
        if model_file:
            model = reinforcement_learning_model.ReinforcementLearningModel(
                0.1, 1.0, filename=model_file)
        else:
            model = reinforcement_learning_model.ReinforcementLearningModel(0.1, 1.0)
        board = picking_cans_board.Board(10, 10)
        board.Randomize()
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)
