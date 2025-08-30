#!/bin/bash
# run.sh

# Remove previous output folder if exists
hdfs dfs -rm -r /user/hadoop/output

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /user/hadoop/input/input.txt \
    -output /user/hadoop/output \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file mapper.py \
    -file reducer.py

