#!/bin/bash

# All sorts of random fun!
./rose.py `whoami` --detailed \
  |sed -e 's/  //g' \
  |awk -F "\"*, \"*" '{print $3}' \
  |sort \
  |grep -v '\['
