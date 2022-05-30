#!/bin/bash

docker cp data_processing $(docker ps | grep reveal | tr -s ' '  | cut -d' ' -f1):/home/user/ReVeal/
