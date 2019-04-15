#!/bin/bash
# Simple script to create and append log line by line simulately
# trap ctrl-c and ctrl_c()

#trap ctrl_c INT
#
#function ctrl_c() {
#    rm -f ./vsmart-logs/fake_catalina.log
#    exit 0
#}

while IFS= read -r line;do
    sleep 1
    echo "$line" >> ./fluentd/data/example.log
done < ./sample-logs/example.log

while IFS= read -r line;do
    sleep 1
    echo "$line" >> ./fluentd/data/rails.log
done < ./sample-logs/rails.log

while IFS= read -r line;do
    sleep 1
    echo "$line" >> ./fluentd/data/java.log
done < ./sample-logs/java.log




