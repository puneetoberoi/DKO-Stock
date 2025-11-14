import sqlite3

conn = sqlite3.connect('src/modules/data/learning.db')
cursor = conn.cursor()

# Get the NEWEST predictions (highest IDs)
cursor.execute("""
    SELECT id, stock, entry_price, timestamp
    FROM predictions
    ORDER BY id DESC
    LIMIT 20
""")

print("NEWEST 20 PREDICTIONS:")
for row in cursor.fetchall():
    print(f"ID {row[0]}: {row[1]} - ${row[2]} - {row[3]}")

conn.close()
```

---

## **About the Missing LLM Analysis:**

The log shows:
```
🔍[AAPL] Received 0 LLM predictions.
