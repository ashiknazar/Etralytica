#!/bin/bash

# Remove old output if exists
hdfs dfs -rm -r /user/hadoop/output

# Run the job
hadoop jar LogStatusCount.jar LogStatusCount \
    /user/hadoop/input/input.txt \
    /user/hadoop/output
