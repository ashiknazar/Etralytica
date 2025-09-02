#!/bin/bash

# Clean old classes
rm -rf classes
mkdir classes

# Compile
javac -classpath `hadoop classpath` -d classes src/LogStatusCount.java

# Create JAR
jar -cvf LogStatusCount.jar -C classes/ .
