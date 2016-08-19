# AI Games

The goal of this project is to collect various AIs that can learn to play simple
games.

# Reinforcement Learning

To train a model run the following:
```
mkdir -p output/rl-model
python -c 'import picking_cans; picking_cans.reinforcement_learning()'
```

As training continues model files will be written to the output directory.
```
% ls output/rl-model
rl-model-1000.txt       rl-model-2000.txt      rl-model-3000.txt      rl-model-4000.txt
```
Models will be saved to output/rl-model. To run a model (say
output/rl-model/rl-model-4000.txt) on a random board run the following:
```
python -c 'import picking_cans; picking_cans.reinforcement_learning(\
train_model=False, model_file="output/rl-model/rl-model-4000.txt")' | less -r
```

# Genetic Algorithms