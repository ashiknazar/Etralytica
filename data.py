import random
from datetime import datetime, timedelta

# --- Define website URLs ---
urls = [
    "/index.html",
    "/about.html",
    "/contact.html",
    "/services/digital-marketing.html",
    "/services/web-development.html",
    "/services/graphic-design.html",
    "/internships/digital-marketing.html",
    "/internships/web-development.html",
    "/internships/graphic-design.html",
    "/internships/data-science.html",
    "/internships/data-analytics.html",
    "/blog.html",
    "/careers.html"
]

# --- Popularity weight (simulate more visits on some pages) ---
weights = [
    10, 5, 8, 15, 12, 8, 10, 9, 4, 11, 7, 3, 6
]

# --- IP addresses pool (simulate visitors) ---
ip_pool = [f"192.168.0.{i}" for i in range(1, 51)]  # 50 different visitors

# --- Response codes ---
response_codes = [200]*90 + [404]*7 + [500]*3  # 90% 200, 7% 404, 3% 500

# --- Start time ---
start_time = datetime(2025, 8, 28, 9, 0, 0)

# --- Function to generate log lines ---
def generate_log_line():
    ip = random.choice(ip_pool)
    timestamp = start_time + timedelta(seconds=random.randint(0, 3600*8))  # 8 hours range
    url = random.choices(urls, weights=weights)[0]
    code = random.choice(response_codes)
    size = random.randint(500, 6000) if code == 200 else random.randint(0, 500)
    
    log_line = f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET {url} HTTP/1.1" {code} {size}'
    return log_line

# --- Generate log file ---
with open("ethqan_logs.txt", "w") as f:
    for _ in range(10000):  # number of logs
        f.write(generate_log_line() + "\n")

print("Generated 10,000 log lines in 'ethqan_logs.txt'")
