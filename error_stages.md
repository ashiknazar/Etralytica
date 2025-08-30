# ETralitica
![](static/images/logo.png)
A simple **web traffic analysis project** for **Ethqan Technologies**, built with **Hadoop 

##  Install java

1. install java
    -  `sudo apt update`
    -  `sudo apt install openjdk-8-jdk -y`
2. Set JAVA_HOME:
    - echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc
    - echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> ~/.bashrc
    - source ~/.bashrc

##   Install Hadoop

- `wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz`
- `sudo tar -xvzf hadoop-3.3.6.tar.gz -C /usr/local/`
- `sudo mv /usr/local/hadoop-3.3.6 /usr/local/hadoop`


## Set hadoop environments
- echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.bashrc
- echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> ~/.bashrc
- echo "export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop" >> ~/.bashrc
- echo "export HDFS_NAMENODE_USER=$USER" >> ~/.bashrc
- echo "export HDFS_DATANODE_USER=$USER" >> ~/.bashrc
- echo "export HDFS_SECONDARYNAMENODE_USER=$USER" >> ~/.bashrc
- echo "export YARN_RESOURCEMANAGER_USER=$USER" >> ~/.bashrc
- echo "export YARN_NODEMANAGER_USER=$USER" >> ~/.bashrc
- source ~/.bashrc

## Configure Hadoop (Pseudo-distributed)

1. Edit `core-site.xml`
 -  nano $HADOOP_HOME/etc/hadoop/core-site.xml
 - <configuration>
   <property>
   <name>fs.defaultFS</name>
   <value>hdfs://localhost:9000</value>
   </property>
   </configuration>
2. Edit hdfs-site.xml
 -  nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml

 - <configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
    </property>
  </configuration>

3. Edit mapred-site.xml
   - nano $HADOOP_HOME/etc/hadoop/mapred-site.xml

   - <configuration>
    <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
     </property>
     </configuration>
4. Edit yarn-site.xml
   - nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
   - <configuration>
    <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
    </property>
    </configuration>

5. Format Namenode & Start Services
  - hdfs namenode -format
  - start-dfs.sh
  - start-yarn.sh


6. Upload input data to HDFS

    - hdfs dfs -mkdir -p /user/ashik/input

    - hdfs dfs -put /home/ashik/codes/Etralytica/data/input.txt /user/ashik/input/


7. creatd mapper.py,reducer.py inside src folder
    - make them executable
       - cd /home/ashik/codes/Etralytica/src
       - chmod +x mapper.py reducer.py

7. Create run.sh
    - Location: /home/ashik/codes/Etralytica/src/run.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

# Adjust these if your paths differ
HADOOP_STREAMING_JAR=$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n 1)

INPUT=/user/ashik/input/input.txt
OUTPUT=/user/ashik/output/status_counts

# Cleanup old output (ignore error if not exists)
hdfs dfs -rm -r -f "$OUTPUT" || true

# Run Hadoop Streaming
hadoop jar "$HADOOP_STREAMING_JAR" \
  -D mapreduce.job.name="ETraffic: Status Code Counts" \
  -input "$INPUT" \
  -output "$OUTPUT" \
  -mapper /home/ashik/codes/Etralytica/src/mapper.py \
  -reducer /home/ashik/codes/Etralytica/src/reducer.py \
  -file /home/ashik/codes/Etralytica/src/mapper.py \
  -file /home/ashik/codes/Etralytica/src/reducer.py

echo "Job finished. Output in HDFS: $OUTPUT"

```
8. Make it executable 
  - chmod +x /home/ashik/codes/Etralytica/src/run.sh

9. Run the job
  - bash /home/ashik/codes/Etralytica/src/run.sh

10. met with error 

11. Fix: add MapReduce env properties to mapred-site.xml + export HADOOP_MAPRED_HOME

```bash
# 1) show current HADOOP_HOME
echo "HADOOP_HOME='$HADOOP_HOME'"

# 2) back up mapred-site.xml
cp "$HADOOP_HOME/etc/hadoop/mapred-site.xml" "$HADOOP_HOME/etc/hadoop/mapred-site.xml.bak"

# 3) open the file for editing (use nano, vim or your editor)
nano "$HADOOP_HOME/etc/hadoop/mapred-site.xml"
```
- hadoop home was shown as /usr/local/hadoop so 
12. edit <configuration> by adding
  -   <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>

  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>

  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>

13. Now export HADOOP_MAPRED_HOME to your shell profile so it's available for future restarts:
```bash
 echo "export HADOOP_MAPRED_HOME=$HADOOP_HOME" >> ~/.bashrc
# also ensure HADOOP_HOME and JAVA_HOME are exported (add if missing)
grep -q "export HADOOP_HOME=" ~/.bashrc || echo "export HADOOP_HOME=$HADOOP_HOME" >> ~/.bashrc
# set JAVA_HOME if not set (replace path if different)
grep -q "export JAVA_HOME=" ~/.bashrc || echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc

source ~/.bashrc
```
14. Update hadoop-env.sh (ensure JAVA_HOME there too)
  - nano "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
  - Make sure there is a line like:
  - export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

15. Edit run.sh to use -files (not deprecated -file) and localized mapper/reducer names

```bash
  #!/usr/bin/env bash
set -euo pipefail

HADOOP_STREAMING_JAR=$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n 1)
INPUT=/user/ashik/input/input.txt
OUTPUT=/user/ashik/output/status_counts

hdfs dfs -rm -r -f "$OUTPUT" || true

hadoop jar "$HADOOP_STREAMING_JAR" \
  -D mapreduce.job.name="ETraffic: Status Code Counts" \
  -input "$INPUT" \
  -output "$OUTPUT" \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -files /home/ashik/codes/Etralytica/src/mapper.py,/home/ashik/codes/Eralytica/src/reducer.py

echo "Job finished. Output in HDFS: $OUTPUT"

```
16. Make it executable:
  - chmod +x /home/ashik/codes/Etralytica/src/run.sh
17. Restart Hadoop services (so new env vars are picked up)

  - stop-yarn.sh || true
  - stop-dfs.sh || true
  - start-dfs.sh
  - start-yarn.sh
  - jps
18. Re-run your job
  - cd /home/ashik/codes/Etralytica/src
  - bash run.sh

19. still caused error The error tells us that your Hadoop version does not support -files, it uses -file (singular, repeated per file).
  - edited run.sh

```bash
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
```
20. make both executable
  - chmod +x mapper.py reducer.py run.sh
21. Run the script:
  - bash run.sh

22. still error Error Launching job : Input path does not exist: hdfs://localhost:9000/user/hadoop/input/input.txt
  - Fix: Upload your input.txt into the correct HDFS path
```bash
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put /home/ashik/codes/Etralytica/data/input.txt /user/hadoop/input/

```
23. bash run.sh
   - success 
24. View the output

    hdfs dfs -cat /user/hadoop/output/part-00000

---


## 📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

---

## ✨ Credits
Developed by **Ethqan Technologies** as a simple demonstration of Big Data processing with Hadoop.
