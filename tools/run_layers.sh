#!/bin/bash
# run_layers.sh RACE  — Layers 1–5 for one race folder in reference/classic/RACE (needs the split runner workbooks)
set -e; R=$1
python3.12 tools/layer1_inventory.py reference/classic/$R
python3.12 tools/layer2_roots.py $R
python3.12 tools/layer3_web.py $R
python3.12 tools/layer4_field.py $R
python3.12 tools/layer5_reader.py $R
