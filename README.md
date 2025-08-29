# ETraffic-Analytics 🚀
![](static/images/logo.png)
A simple **web traffic analysis project** for **Ethqan Technologies**, built with **Hadoop Streaming** and **Python** (mapper & reducer).  

This project demonstrates how to run a basic **MapReduce job** on a single-node Hadoop cluster, processing ~10,000 records to analyze website traffic.

---

## 📂 Repository Structure

ETraffic-Analytics/
│
├── data/
│   ├── input.txt              # Sample input dataset
│   └── expected_output.txt    # Reference output (optional)
│
├── src/
│   ├── mapper.py              # Mapper script
│   ├── reducer.py             # Reducer script
│   └── run.sh                 # Helper script to run Hadoop job
│
├── docs/
│   └── project_overview.md    # Project explanation
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

---

## ⚙️ Prerequisites

- Java 8+
- Hadoop (single-node / pseudo-distributed mode)
- Python 3

Verify Hadoop is installed:

    hadoop version

---

## 🚀 Running the Project

1. Start Hadoop services

    start-dfs.sh
    start-yarn.sh

2. Upload input data to HDFS

    hdfs dfs -mkdir -p /user/hadoop/input
    hdfs dfs -put data/input.txt /user/hadoop/input/

3. Run the MapReduce job

    bash src/run.sh

   This uses Hadoop Streaming to run the Python `mapper.py` and `reducer.py`.

4. View the output

    hdfs dfs -cat /user/hadoop/output/part-00000

---

## 🧩 Example

Input (data/input.txt):

    192.168.1.1 GET /index.html
    192.168.1.2 GET /contact.html
    192.168.1.1 GET /about.html

Output (aggregated visits per IP):

    192.168.1.1    2
    192.168.1.2    1

---

## 📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

---

## ✨ Credits
Developed by **Ethqan Technologies** as a simple demonstration of Big Data processing with Hadoop.
