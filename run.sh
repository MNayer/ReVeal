#!/bin/bash

# Parse source function files
pushd data/examples
/home/user/ReVeal/code-slicer/joern/joern-parse -outformat csv raw_code/
popd


pushd data_processing/
python extract_slices.py
popd
