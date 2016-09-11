import picking_cans_board

import default_agent_state
import radius_one_agent_state
import radius_two_agent_state

import genetic_algorithm_model
import manual_model
import q_learning_model
import shallow_q_learning_model

import list_util
import multiprocessing
import os

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

def GetModelClass(model_type):
    model_classes = {
        "manual": (lambda f, a: manual_model.ManualModel()),
        "genetic": (lambda f, a: genetic_algorithm_model.GeneticAlgorithmModel(
            filename=f,
            agent_state_class=a)),
        "q-learning": (lambda f, a: q_learning_model.QLearningModel(
            learning_rate=0.0,
            discount_rate=0.0,
            exploration_rate=0.0,
            filename=f,
            agent_state_class=a)),
        "shallow-q-learning": (lambda f, a: shallow_q_learning_model.ShallowQLearningModel(
            disable_training=True,
            filename=f,
            agent_state_class=a)),
    }
    try:
        return model_classes[model_type]
    except KeyError:
        raise KeyError, "invalid model_type: %s" % (model_type,)

def EvaluateModel(games=1000, board_size=(10, 10), model_file=None,
                  model_type="manual", agent_state_type="default",
                  random_wall=False, actions_per_game=200, verbose=False):
    model_class = GetModelClass(model_type)
    agent_state_class = GetAgentStateClass(agent_state_type)

    board = picking_cans_board.Board(
        board_size[0], board_size[1], agent_state_class=agent_state_class)
    model = model_class(model_file, agent_state_class)
    score = [None for _ in range(games)]
    for g in range(1, games + 1):
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        score[g - 1] = board.PickCansWithModel(
            model, actions_per_game=actions_per_game)

        if verbose:
            print "game %4d: %4d" % (g, score[g - 1])

    mean_score = list_util.Mean(score)
    stdev_score = list_util.StandardDeviation(score)

    if verbose:
        print "mean score: %4.2f" % (mean_score,)
        print "standard deviation score: %4.2f" % (stdev_score,)

    return [mean_score, stdev_score]

def RunEvaluateModel(queue, **kwargs):
    queue.put([kwargs["model_file"]] + EvaluateModel(**kwargs))

def EvaluateModels(games=1000, board_size=(10, 10), model_dir=None,
                  model_type="manual", agent_state_type="default",
                  random_wall=False, actions_per_game=200, verbose=False):
    queue = multiprocessing.Queue()
    processes = []
    stats = {}
    for f in os.listdir(model_dir):
        model_file = os.path.join(model_dir, f)
        stats[model_file] = None
        processes.append(multiprocessing.Process(
            target=RunEvaluateModel,
            args=(queue,),
            kwargs={
                "games": games,
                "board_size": board_size,
                "model_file": model_file,
                "model_type": model_type,
                "agent_state_type": agent_state_type,
                "random_wall": random_wall,
                "actions_per_game": actions_per_game,
                "verbose": verbose,
            }))
        processes[-1].start()

    for _ in range(len(stats)):
        print queue.get()
    for p in processes:
        p.join()
