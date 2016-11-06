# AI Games

The goal of this project is to collect various AIs that can learn to play simple
games.

# Deep Q-Learning

To train a model run the following:

```
mkdir -p output/sql-model
python -c 'import picking_cans; picking_cans.deep_q_learning()'
```

As training continues model files will be written to the output directory.

```
% ls output/dql-model
dql-model-100.txt       dql-model-200.txt      dql-model-300.txt      dql-model-400.txt
```

Models will be saved to output/dql-model. To run a model (say
output/ql-model/dql-model-400.txt) on a random board run the following:

```
python -c 'import picking_cans; picking_cans.deep_q_learning(\
    train_model=False, model_file="output/dql-model/dql-model-400.txt")' | less -r
```

# Shallow Q-Learning

To train a model run the following:

```
mkdir -p output/sql-model
python -c 'import picking_cans; picking_cans.shallow_q_learning()'
```

As training continues model files will be written to the output directory.

```
% ls output/sql-model
sql-model-100.txt       sql-model-200.txt      sql-model-300.txt      sql-model-400.txt
```

Models will be saved to output/sql-model. To run a model (say
output/ql-model/sql-model-400.txt) on a random board run the following:

```
python -c 'import picking_cans; picking_cans.shallow_q_learning(\
    train_model=False, model_file="output/sql-model/sql-model-400.txt")' | less -r
```

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
