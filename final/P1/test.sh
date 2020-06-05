#!/bin/bash

for i in $(seq 1 $1);
do
    ./gen.py > test$i
done

for i in $(seq 1 $1);
do
    ./client.py 127.0.0.1 1234$i test$i
done

for i in $(seq 1 $1);
do
    if [ -f rcv_test$i ];
    then
        diff test$i rcv_test$i
        if [[ $? == 0 ]];
        then
            echo Test $i success
        else
            echo Test $i failed
        fi
        rm test$i
        rm rcv_test$i
    else
        echo rcv_test$i not found!
    fi
done
