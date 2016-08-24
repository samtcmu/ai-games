import genetic_algorithm_model
import picking_cans_board
import q_learning_model
import shallow_q_learning_model

def genetic_algorithm(model_file=None, positions=None, models_to_diff=None):
    if (model_file is None) and (models_to_diff is None):
        genetic_algorithm_model.Train(
            rows=10,
            columns=10,
            generations=500,
            population_size=200,
            games=200,
            actions_per_game=200,
            mutation_rate=0.005,
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

def q_learning(train_model=True, model_file=None, random_wall=False):
    if train_model:
        q_learning_model.Train(
            rows=10,
            columns=10,
            random_wall=random_wall,
            games=100000,
            actions_per_game=200,
            learning_rate=0.2,
            discount_rate=0.9,
            exploration_rate=0.002,
            model_save_frequency=1000,
            model_file_prefix="output/ql-model/ql-model",
            verbose=True)
    else:
        if model_file:
            model = q_learning_model.QLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                filename=model_file)
        else:
            model = q_learning_model.QLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0)
        board = picking_cans_board.Board(10, 10)
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)

def shallow_q_learning(train_model=True, model_file=None, random_wall=False):
    if train_model:
        shallow_q_learning_model.Train(
            rows=10,
            columns=10,
            random_wall=random_wall,
            games=100000,
            actions_per_game=200,
            learning_rate=0.5,
            discount_rate=0.9,
            exploration_rate=0.1,
            linear_regression_learning_rate=0.1,
            model_save_frequency=1000,
            model_file_prefix="output/sql-model/sql-model",
            verbose=True)
    else:
        if model_file:
            model = shallow_q_learning_model.ShallowQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                linear_regression_learning_rate=0.0000005,
                filename=model_file)
        else:
            model = shallow_q_learning_model.ShallowQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0)
        board = picking_cans_board.Board(10, 10)
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)
