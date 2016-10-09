#!/bin/sh

OUTPUT_PREFIX=${1}

# Run the Python profiler.
python -m cProfile -s 'cumulative' -o ${OUTPUT_PREFIX}.prof profile_training.py

# Transform the output of the Python profiler to a dot file.
gprof2dot -f pstats ${OUTPUT_PREFIX}.prof -o ${OUTPUT_PREFIX}.dot

# Transform the dot file to a png image file.
dot -Tpng ${OUTPUT_PREFIX}.dot > ${OUTPUT_PREFIX}.png

echo "Produced all desired outputs:"
echo "  ${OUTPUT_PREFIX}.prof"
echo "  ${OUTPUT_PREFIX}.dot"
echo "  ${OUTPUT_PREFIX}.png"

echo "Opening the png file containing profiler results."
open ${OUTPUT_PREFIX}.png
