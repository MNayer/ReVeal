#!/bin/bash

docker cp ../ReVeal $(docker ps | grep reveal | tr -s ' '  | cut -d' ' -f1):/home/user/
