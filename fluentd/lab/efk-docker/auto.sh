#!/bin/bash
# Simple script to create and append log line by line simulately


for ((i=1;i<=1000;i++)); do  echo "Welcome $i times" >> ./fluentd/data/tail.log; sleep 1; done