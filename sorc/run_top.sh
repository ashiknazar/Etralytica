#!/usr/bin/env bash

INPUT=/user/ashik/input/input.txt
OUTPUT=/user/ashik/output/top_ips

hdfs dfs -rm -r -f "$OUTPUT"

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input "$INPUT" \
  -output "$OUTPUT" \
  -mapper "python3 mapper_top.py" \
  -reducer "python3 reducer_top.py" \
  -file src2/mapper_top.py \
  -file src2/reducer_top.py
