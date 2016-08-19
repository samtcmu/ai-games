# AI Games

The goal of this project is to collect various AIs that can learn to play simple
games.

# Reinforcement Learning

To train a model run the following:

```
mkdir -p output/rl-model
python -c 'import picking_cans; picking_cans.reinforcement_learning()'
```

Models will be saved to output/rl-model. To run a model on a random board run
the following:

```
python -c 'import picking_cans; picking_cans.reinforcement_learning(train_model=False, model_file="output/rl-model/rl-model-53000.txt")' | less -r
```

# Genetic Algorithms
