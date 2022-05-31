#!/bin/bash

# Exit on fail
set -e

# Parse source function files
pushd data/example
/home/user/ReVeal/code-slicer/joern/joern-parse -outformat csv raw_code/
popd


pushd data_processing/
python extract_slices.py
popd

pushd data_processing/
python create_ggnn_data.py --project crash --csv /home/user/ReVeal/data/example/parsed/raw_code/ --src /home/user/ReVeal/data/example/raw_code/ --output /home/user/ReVeal/data/example/full_experiment_real_data/crash/crash.json
popd
