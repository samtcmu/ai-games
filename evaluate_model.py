import picking_cans_board

import default_agent_state
import radius_one_agent_state
import radius_two_agent_state

import genetic_algorithm_model
import manual_model
import q_learning_model
import shallow_q_learning_model

import list_util

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

def main(games=1000, board_size=(10, 10), model_file=None, model_type="manual",
         agent_state_type="default", random_wall=False, actions_per_game=200,
         verbose=False):
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

    print "mean score: %4.2f" % (list_util.Mean(score),)
    print "standard deviation score: %4.2f" % (
        list_util.StandardDeviation(score),)
