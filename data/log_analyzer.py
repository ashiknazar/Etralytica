import re
from collections import Counter, defaultdict
from datetime import datetime

# --- Load logs ---
with open("input.txt", "r") as f:
    logs = f.readlines()

# --- Regex for parsing Apache-like logs ---
log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>.*?)\] "GET (?P<url>\S+) HTTP/1.1" (?P<code>\d{3}) (?P<size>\d+)'
)

# --- Storage ---
total_requests = 0
status_counts = Counter()
ip_counts = Counter()
url_counts = Counter()
internship_counts = Counter()
errors_by_url = defaultdict(Counter)
hourly_counts = Counter()

# --- Parse logs ---
for line in logs:
    match = log_pattern.match(line)
    if not match:
        continue
    
    total_requests += 1
    ip = match.group("ip")
    url = match.group("url")
    code = int(match.group("code"))
    time_str = match.group("time")
    timestamp = datetime.strptime(time_str.split()[0], "%d/%b/%Y:%H:%M:%S")
    
    # Counts
    status_counts[code] += 1
    ip_counts[ip] += 1
    url_counts[url] += 1
    
    # Internship-specific
    if url.startswith("/internships/"):
        internship_counts[url] += 1
    
    # Error breakdown
    if code != 200:
        errors_by_url[url][code] += 1
    
    # Hourly distribution
    hour = timestamp.strftime("%H:00")
    hourly_counts[hour] += 1

# --- Conversion Funnel (very simple heuristic) ---
# (counts people who visited internships/services and also contact)
visitors_internships = set()
visitors_services = set()
visitors_contact = set()

for line in logs:
    match = log_pattern.match(line)
    if not match:
        continue
    ip = match.group("ip")
    url = match.group("url")
    if url.startswith("/internships/"):
        visitors_internships.add(ip)
    if url.startswith("/services/"):
        visitors_services.add(ip)
    if url == "/contact.html":
        visitors_contact.add(ip)

conv_from_internships = len(visitors_internships & visitors_contact) / max(1, len(visitors_internships)) * 100
conv_from_services = len(visitors_services & visitors_contact) / max(1, len(visitors_services)) * 100
abandoned = 100 - conv_from_internships

# --- Reporting ---
print("# Ethqan Technologies Website Log Analysis (Sample Batch)\n")

print("## 1. Total Requests")
print(f"- **Total log entries:** {total_requests}")
print(f"- **Successful requests (200):** {status_counts[200]}")
print(f"- **Client errors (404):** {status_counts[404]}")
print(f"- **Server errors (500):** {status_counts[500]}")
print("\n---\n")

print("## 2. Top Visitors (IP Address by Number of Requests)")
print("| IP Address | Requests |")
print("|------------|----------|")
for ip, count in ip_counts.most_common(5):
    print(f"| {ip} | {count} |")
print("\n---\n")

print("## 3. Most Visited Pages")
print("| URL | Hits |")
print("|-----|------|")
for url, count in url_counts.most_common(5):
    print(f"| {url} | {count} |")
print("\n---\n")

print("## 4. Internship Page Interest")
print("| Internship Page | Visits |")
print("|-----------------|--------|")
for url, count in internship_counts.most_common():
    print(f"| {url} | {count} |")
print("\n---\n")

print("## 5. Error Analysis")
for url, codes in errors_by_url.items():
    for code, count in codes.items():
        print(f"- **{code}** on `{url}`: {count} times")
print("\n---\n")

print("## 6. Conversion Funnel Insights")
print(f"- Visitors who viewed internship pages and then `/contact.html`: ~{conv_from_internships:.1f}%")
print(f"- Visitors who viewed services and then `/contact.html`: ~{conv_from_services:.1f}%")
print(f"- Abandoned journeys (visited internships but never reached contact): ~{abandoned:.1f}%")
print("\n---\n")

print("## 7. Peak Traffic Hours")
for hour, count in sorted(hourly_counts.items()):
    print(f"- **{hour}:** {count} requests")
