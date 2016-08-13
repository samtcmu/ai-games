import genetic_algorithm_model
import picking_cans_board

def main(actions=None):
    if actions is None:
        print genetic_algorithm_model.GeneticAlgorithmModel.Train(
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
