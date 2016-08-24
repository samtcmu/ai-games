# AI Games

The goal of this project is to collect various AIs that can learn to play simple
games.

# Q-Learning

To train a model run the following:

```
mkdir -p output/ql-model
python -c 'import picking_cans; picking_cans.q_learning()'
```

As training continues model files will be written to the output directory.

```
% ls output/ql-model
ql-model-1000.txt       ql-model-2000.txt      ql-model-3000.txt      ql-model-4000.txt
```

Models will be saved to output/ql-model. To run a model (say
output/ql-model/ql-model-4000.txt) on a random board run the following:

```
python -c 'import picking_cans; picking_cans.q_learning(\
    train_model=False, model_file="output/ql-model/ql-model-4000.txt")' | less -r
```

# Genetic Algorithms

To train a model run the following:

```
mkdir -p output/ga-model
python -c 'import picking_cans; picking_cans.genetic_algorithm()'
```

As training continues model files will be written to the output directory.

```
% ls output/ga-model
ga-model-0-0.txt        ga-model-0-1.txt
ga-model-1-0.txt        ga-model-1-1.txt
ga-model-2-0.txt        ga-model-2-1.txt
ga-model-3-0.txt        ga-model-3-1.txt
```

Models will be saved to output/ga-model. To run a model (say
output/ga-model/ga-model-0-0.txt) on a random board run the following:

```
python -c 'import picking_cans; picking_cans.genetic_algorithm(\
    model_file="output/ga-model/ga-model-0-0.txt")' | less -r
```
