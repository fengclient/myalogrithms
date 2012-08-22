#!/bin/sh
echo $1 workers
for i in {1..$1}
do
    echo "starting worker $i" 
    #python worker.py >/dev/null 2>&1 &
done
