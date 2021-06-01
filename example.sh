#!/bin/bash
./rose.py `whoami` --detailed |sed -e 's/  //g' |awk -F "\"*, \"*" '{print $3}'
