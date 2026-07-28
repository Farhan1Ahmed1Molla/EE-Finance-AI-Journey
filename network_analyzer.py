import sqlite3
connection = sqlite3.connect("logs.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY,
    ip TEXT,
    level TEXT,
    timestamp TEXT)""")
connection.commit()

Error_counts = {}
Alert_Threshold = 3

def parse_log_line(line):
    words = line.split()
    timestamp = words[0] + " " + words[1]

    level = words[2]
    ip = words[3]

    return timestamp, level, ip

try:
    with open("network_log.txt", "r") as file:
        for line in file:
            if not line.strip():
                continue
            timestamp, level, ip = parse_log_line(line)

            cursor.execute(
                """INSERT INTO logs (timestamp, level, ip) VALUES (?, ?, ?)""",
                (timestamp, level, ip))

            if level != "ERROR":
                continue

            Error_counts[ip] = Error_counts.get(ip, 0) + 1

    connection.commit()
except FileNotFoundError:
    print("Warning: The log file 'network_log.txt' was not found.")
    print("Please ensure the file exists and is accessible. Log parsing and error counting have been skipped.")


for ip, count in Error_counts.items():
    print("=" * 30)
    print(f"IP: {ip}")
    print(f"Error Count: {count}")
    print("=" * 30)

for ip, count in Error_counts.items():

    if count >= Alert_Threshold:
        print("=" * 30)
        print("⚠️ SECURITY ALERT")
        print(f"IP: {ip}")
        print(f"Failed Attempts: {count}")
        print("=" * 30)

cursor.execute("SELECT * FROM logs")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
