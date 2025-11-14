import sqlite3
import os
from datetime import datetime, timedelta

db_path = 'src/modules/data/learning.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit()

print(f"✅ Database found at: {db_path}\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check what's in the predictions table
print("="*60)
print("📊 PREDICTIONS TABLE")
print("="*60)

cursor.execute("""
    SELECT id, stock, prediction, timestamp, entry_price
    FROM predictions
    ORDER BY timestamp DESC
    LIMIT 20
""")

predictions = cursor.fetchall()

if not predictions:
    print("❌ NO PREDICTIONS FOUND IN DATABASE!")
    print("   The morning script might not be saving predictions correctly.")
else:
    print(f"✅ Found {len(predictions)} recent predictions:\n")
    for pred_id, stock, action, timestamp, entry_price in predictions:
        print(f"  ID: {pred_id}")
        print(f"  Stock: {stock}")
        print(f"  Action: {action}")
        print(f"  Time: {timestamp}")
        print(f"  Entry Price: ${entry_price}")
        print(f"  ---")

# Check what's in the outcomes table
print("\n" + "="*60)
print("📊 OUTCOMES TABLE")
print("="*60)

cursor.execute("""
    SELECT COUNT(*) as total,
           COUNT(DISTINCT prediction_id) as unique_predictions
    FROM outcomes
""")

outcome_stats = cursor.fetchone()
print(f"Total outcomes: {outcome_stats[0]}")
print(f"Unique predictions graded: {outcome_stats[1]}")

# Show which predictions have NOT been graded yet
print("\n" + "="*60)
print("🔍 UNGRADED PREDICTIONS")
print("="*60)

cursor.execute("""
    SELECT p.id, p.stock, p.prediction, p.timestamp, p.entry_price
    FROM predictions p
    LEFT JOIN outcomes o ON p.id = o.prediction_id
    WHERE o.prediction_id IS NULL
    ORDER BY p.timestamp DESC
    LIMIT 20
""")

ungraded = cursor.fetchall()

if not ungraded:
    print("✅ All predictions have been graded!")
else:
    print(f"Found {len(ungraded)} ungraded predictions:\n")
    for pred_id, stock, action, timestamp, entry_price in ungraded:
        pred_date = timestamp.split()[0] if ' ' in timestamp else timestamp
        print(f"  {stock}: {action} on {pred_date} @ ${entry_price}")

# Check the SQL query that autonomous_learner uses
print("\n" + "="*60)
print("🧪 TESTING AUTONOMOUS_LEARNER QUERY")
print("="*60)

# Test with different time deltas
test_dates = [
    ("Yesterday", 1),
    ("Today", 0),
    ("Tomorrow", -1)
]

for label, days_offset in test_dates:
    test_date = (datetime.now() - timedelta(days=days_offset)).strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE date(timestamp) <= ?
        AND id NOT IN (SELECT prediction_id FROM outcomes WHERE prediction_id IS NOT NULL)
        AND entry_price > 0
    """, (test_date,))
    
    count = cursor.fetchone()[0]
    print(f"  {label} ({test_date}): {count} predictions would be graded")

conn.close()

print("\n" + "="*60)
print("✅ Database check complete!")
print("="*60)
