import genetic_algorithm_model
import picking_cans_board
import reinforcement_learning_model

def genetic_algorithm(model_file=None, positions=None, models_to_diff=None):
    if (model_file is None) and (models_to_diff is None):
        print genetic_algorithm_model.Train(
            rows=10,
            columns=10,
            generations=500,
            population_size=200,
            games=200,
            actions_per_game=200,
            model_file_prefix="output/ga-model/ga-model",
            verbose=True)
    elif models_to_diff:
        board = picking_cans_board.Board(10, 10)
        models = [genetic_algorithm_model.GeneticAlgorithmModel(
            filename=f) for f in models_to_diff]
        for i in range(len(picking_cans_board.CELLS)**5):
            if models[0]._actions[i] != models[1]._actions[i]:
                print board.BoardPositionAsString(i)
                print "action[%s]: %s" % (
                    models_to_diff[0],
                    picking_cans_board.ACTIONS[models[0].ActionForPosition(i)][1],)
                print "action[%s]: %s\n" % (
                    models_to_diff[1],
                    picking_cans_board.ACTIONS[models[1].ActionForPosition(i)][1],)
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
        reinforcement_learning_model.Train(
            rows=10,
            columns=10,
            games=100000,
            actions_per_game=200,
            learning_rate=0.2,
            discount_rate=0.9,
            exploration_rate=0.001,
            model_save_frequency=1000,
            model_file_prefix="output/rl-model/rl-model",
            verbose=True)
    else:
        if model_file:
            model = reinforcement_learning_model.ReinforcementLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                filename=model_file)
        else:
            model = reinforcement_learning_model.ReinforcementLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0)
        board = picking_cans_board.Board(10, 10)
        board.Randomize()
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)
