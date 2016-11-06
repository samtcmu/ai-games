# This must be imported first.
import picking_cans_board

import default_agent_state
import radius_one_agent_state
import radius_two_agent_state

import deep_q_learning_model
import genetic_algorithm_model
import manual_model
import q_learning_model
import shallow_q_learning_model

def GetAgentStateClass(agent_state_type):
    agent_state_classes = {
        "default": default_agent_state.DefaultAgentState,
        "radius-one": radius_one_agent_state.RadiusOneAgentState,
        "radius-two": radius_two_agent_state.RadiusTwoAgentState,
    }
    try:
        return agent_state_classes[agent_state_type]
    except KeyError:
        raise KeyError, "invalid agent_state_type: %s" % (agent_state_type,)

def manual_algorithm(positions=None, test_model=False):
    model = manual_model.ManualModel()
    board = picking_cans_board.Board(10, 10)
    board.Randomize()
    board.RandomizeCurrentPosition()
    if positions is not None:
        for position in positions:
            state = picking_cans_board.AgentState.AgentStateForBoardPosition(
                position)
            print "position: %d\n" % (position,)
            print state
            print "action: %s\n" % (
                picking_cans_board.ACTIONS[model.ActionForState(state)][1],)
    elif test_model:
        test_trials=1000
        total_score = 0
        for i in range(1, test_trials + 1):
            board.Randomize()
            board.RandomizeCurrentPosition()
            score = board.PickCansWithModel(model, actions_per_game=200)
            total_score += score
            print "game %4d: %d" % (i, score)
        print "average score: %0.3f" % (total_score / float(test_trials),)
    else:
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)

def genetic_algorithm(model_file=None, positions=None, models_to_diff=None,
                      agent_state_type="default"):
    agent_state_class = GetAgentStateClass(agent_state_type)

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
            agent_state_class=agent_state_class,
            verbose=True)
    elif models_to_diff:
        board = picking_cans_board.Board(
                10, 10, agent_state_class=agent_state_class)
        models = [genetic_algorithm_model.GeneticAlgorithmModel(
            filename=f, agent_state_class=agent_state_class) for f in models_to_diff]
        for p in range(agent_state_class.NumberOfStates()):
            state = agent_state_class.AgentStateForBoardPosition(p)
            if models[0]._actions[p] != models[1]._actions[p]:
                print state
                print "action[%s]: %s" % (
                    models_to_diff[0],
                    picking_cans_board.ACTIONS[models[0].ActionForState(state)][1],)
                print "action[%s]: %s\n" % (
                    models_to_diff[1],
                    picking_cans_board.ACTIONS[models[1].ActionForState(state)][1],)
    else:
        if positions is None:
            model = genetic_algorithm_model.GeneticAlgorithmModel(
                filename=model_file, agent_state_class=agent_state_class)
            board = picking_cans_board.Board(
                10, 10, agent_state_class=agent_state_class)
            board.Randomize()
            board.RandomizeCurrentPosition()
            print "score: %d" % (board.PickCansWithModel(
                model, actions_per_game=200, verbose=True),)
        else:
            model = genetic_algorithm_model.GeneticAlgorithmModel(
                filename=model_file, agent_state_class=agent_state_class)
            board = picking_cans_board.Board(
                10, 10, agent_state_class=agent_state_class)
            for position in positions:
                state = agent_state_class.AgentStateForBoardPosition(
                    position)
                print "position: %d\n" % (position,)
                print state
                print "action: %s\n" % (
                    picking_cans_board.ACTIONS[model.ActionForState(state)][1],)

def q_learning(train_model=True, model_file=None, random_wall=False,
               agent_state_type="default", games=100000):
    agent_state_class = GetAgentStateClass(agent_state_type)

    if train_model:
        q_learning_model.Train(
            rows=10,
            columns=10,
            random_wall=random_wall,
            games=games,
            actions_per_game=200,
            learning_rate=0.2,
            discount_rate=0.9,
            exploration_rate=0.01,
            model_save_frequency=1000,
            model_file_prefix="output/ql-model/ql-model",
            agent_state_class=agent_state_class,
            verbose=True)
    else:
        if model_file:
            model = q_learning_model.QLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                filename=model_file,
                agent_state_class=agent_state_class)
        else:
            model = q_learning_model.QLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                agent_state_class=agent_state_class)
        board = picking_cans_board.Board(10, 10,
            agent_state_class=agent_state_class)
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)

def shallow_q_learning(train_model=True, model_file=None, random_wall=False,
                       agent_state_type="default", games=100000):
    agent_state_class = GetAgentStateClass(agent_state_type)

    if train_model:
        shallow_q_learning_model.Train(
            rows=10,
            columns=10,
            random_wall=random_wall,
            games=games,
            actions_per_game=200,
            learning_rate=0.1,
            discount_rate=0.99,
            exploration_rate=0.01,
            linear_regression_learning_rate=0.01,
            model_save_frequency=100,
            model_file_prefix="output/sql-model/sql-model",
            agent_state_class=agent_state_class,
            verbose=True)
    else:
        if model_file:
            model = shallow_q_learning_model.ShallowQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                linear_regression_learning_rate=0.0000005,
                filename=model_file,
                agent_state_class=agent_state_class)
        else:
            model = shallow_q_learning_model.ShallowQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                agent_state_class=agent_state_class)
        model.SetDisableTraining(True)
        board = picking_cans_board.Board(
            10, 10, agent_state_class=agent_state_class)
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)

def deep_q_learning(train_model=True, model_file=None, random_wall=False,
                    agent_state_type="default", games=100000):
    agent_state_class = GetAgentStateClass(agent_state_type)

    if train_model:
        deep_q_learning_model.Train(
            rows=10,
            columns=10,
            random_wall=random_wall,
            games=games,
            actions_per_game=200,
            learning_rate=0.1,
            discount_rate=0.99,
            exploration_rate=0.01,
            neural_network_learning_rate=1.0,
            model_save_frequency=100,
            model_file_prefix="output/dql-model/dql-model",
            agent_state_class=agent_state_class,
            verbose=True)
    else:
        if model_file:
            model = deep_q_learning_model.DeepQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                neural_network_learning_rate=0.0000005,
                filename=model_file,
                agent_state_class=agent_state_class)
        else:
            model = deep_q_learning_model.DeepQLearningModel(
                learning_rate=0.1,
                discount_rate=1.0,
                exploration_rate=0.0,
                agent_state_class=agent_state_class)
        model.SetDisableTraining(True)
        board = picking_cans_board.Board(
            10, 10, agent_state_class=agent_state_class)
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        print "score: %d" % (board.PickCansWithModel(
            model, actions_per_game=200, verbose=True),)
