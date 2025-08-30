# ETralytica
![](static/images/logo.png)

A simple **web traffic analysis project** for **Ethqan Technologies**, built with **Hadoop Streaming** and **Python** (mapper & reducer).  

This project demonstrates how to run a basic **MapReduce job** on a single-node Hadoop cluster, processing ~10,000 website log records to extract insights.

---

## 📂 Repository Structure
```text
ETralitica/
│
├── data/
│   ├── log_analyzer.py        # Direct file analysis (non-Hadoop)
│   └── input.txt              # Sample input dataset   
│
├── data_gen/
│   └── data_generator.py      # Fake log data generator
│
├── docs/
│   └── project_overview.md    # Expected analysis output
│
├── src/
│   ├── mapper.py              # Mapper script
│   ├── reducer.py             # Reducer script
│   └── run.sh                 # Job runner script
│
├── static/
│   └── images/
│
├── .gitignore
├── README.md
└── LICENSE
```
___
## 🚀 Setup Guide

### Step 1 — Install Java
```bash
    sudo apt update
    sudo apt install openjdk-8-jdk -y
```
Set environment variables:
```bash
    echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc
    echo "export PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc
    source ~/.bashrc
```

## Step 2 — Install Hadoop

Download and extract Hadoop:
```bash

    wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
    sudo tar -xvzf hadoop-3.3.6.tar.gz -C /usr/local/
    sudo mv /usr/local/hadoop-3.3.6 /usr/local/hadoop
```
Set Hadoop environment variables:
```bash
    echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.bashrc
    echo "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin" >> ~/.bashrc
    echo "export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop" >> ~/.bashrc
    source ~/.bashrc
```
___
## Step 3 — Configure Hadoop (Pseudo-Distributed Mode)

Edit configuration files inside `$HADOOP_HOME/etc/hadoop/`:

### core-site.xml
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

### hdfs-site.xml
```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
```

### mapred-site.xml
```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
```

### yarn-site.xml
```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
</configuration>
```
___
## Step 4 — Start Hadoop Services


```bash

    hdfs namenode -format
    start-dfs.sh
    start-yarn.sh
    jps   # verify processes
```
## Step 5 — Upload Input Data to HDFS


```bash

    hdfs dfs -mkdir -p /user/hadoop/input
    hdfs dfs -put data/input.txt /user/hadoop/input/

```

## Step 6 — Mapper & Reducer
Make both executable:

```bash

    cd src
    chmod +x mapper.py reducer.py


```
## Step 7 — Run Hadoop Streaming Job
`run.sh`:

```bash
#!/bin/bash
set -euo pipefail

hdfs dfs -rm -r /user/hadoop/output || true

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /user/hadoop/input/input.txt \
  -output /user/hadoop/output \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file mapper.py \
  -file reducer.py

echo "✅ Job finished. Results available in HDFS: /user/hadoop/output"

```
Make it executable

```bash
chmod +x run.sh
```
Run the job:
```
./run.sh
```
___
## Step 8 — View Output
```bash
hdfs dfs -cat /user/hadoop/output/part-00000
```
## Expected Insights

From sample data (~10,000 logs), analysis includes:

- Total Requests (200, 404, 500)

- Top Visitors (IPs)

- Most Visited Pages

- Internship Page Interest

- Error Analysis

- Peak Traffic Hours

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ✨ Credits

Developed by **Ethqan Technologies** as a simple demonstration of Big Data processing with Hadoop.
