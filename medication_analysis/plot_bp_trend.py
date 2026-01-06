"""
Plot Blood Pressure Trend for a Specific Patient
Fetches BP measurements and visualizes changes over time
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
MONGO_URI = os.getenv('MONGO_DATABASE_URI')
DATABASE_NAME = "UnifiedCare"
PATIENT_ID = "65ce4e0e422eafa30ba57c15"  # The patient to analyze

print("Blood Pressure Trend Analysis")
print("=" * 80)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
measurements_collection = db['measurements']

print(f"✓ Connected to database: {db.name}")
print(f"✓ Analyzing patient: {PATIENT_ID}\n")

# Query blood pressure measurements for this patient
query = {
    "memberId": ObjectId(PATIENT_ID),
    "type": "BP"
}

# Fetch measurements
cursor = measurements_collection.find(query).sort("updatedAt", 1)
measurements = list(cursor)

print(f"Found {len(measurements)} blood pressure measurements\n")

if len(measurements) == 0:
    print("No measurements found for this patient.")
    client.close()
    exit()

# Extract data into lists
data = []
for m in measurements:
    record = {
        'date': m.get('updatedAt'),
        'systolic': m.get('systolic_blood_pressure', {}).get('value'),
        'diastolic': m.get('diastolic_blood_pressure', {}).get('value'),
        'heart_rate': m.get('heart_rate', {}).get('value')
    }
    data.append(record)

# Create DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Display summary statistics
print("=" * 80)
print("BLOOD PRESSURE STATISTICS")
print("=" * 80)
print(f"\nDate Range: {df['date'].min()} to {df['date'].max()}")
print(f"Duration: {(df['date'].max() - df['date'].min()).days} days")
print(f"Total Measurements: {len(df)}")

print("\nSystolic BP (mmHg):")
print(f"  Mean: {df['systolic'].mean():.1f}")
print(f"  Min:  {df['systolic'].min()}")
print(f"  Max:  {df['systolic'].max()}")
print(f"  Std:  {df['systolic'].std():.1f}")

print("\nDiastolic BP (mmHg):")
print(f"  Mean: {df['diastolic'].mean():.1f}")
print(f"  Min:  {df['diastolic'].min()}")
print(f"  Max:  {df['diastolic'].max()}")
print(f"  Std:  {df['diastolic'].std():.1f}")

if df['heart_rate'].notna().any():
    print("\nHeart Rate (bpm):")
    print(f"  Mean: {df['heart_rate'].mean():.1f}")
    print(f"  Min:  {df['heart_rate'].min()}")
    print(f"  Max:  {df['heart_rate'].max()}")

# Show first and last few measurements
print("\n" + "=" * 80)
print("FIRST 5 MEASUREMENTS")
print("=" * 80)
print(df[['date', 'systolic', 'diastolic', 'heart_rate']].head().to_string(index=False))

print("\n" + "=" * 80)
print("LAST 5 MEASUREMENTS")
print("=" * 80)
print(df[['date', 'systolic', 'diastolic', 'heart_rate']].tail().to_string(index=False))

# Save to CSV
csv_filename = f'bp_trend_{PATIENT_ID}.csv'
df.to_csv(csv_filename, index=False)
print(f"\n✓ Data saved to {csv_filename}")

# Create visualization
print("\nCreating blood pressure trend plot...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Plot 1: Blood Pressure (both systolic and diastolic)
ax1.plot(df['date'], df['systolic'], marker='o', linestyle='-', linewidth=2,
         markersize=4, label='Systolic', color='#e74c3c', alpha=0.8)
ax1.plot(df['date'], df['diastolic'], marker='s', linestyle='-', linewidth=2,
         markersize=4, label='Diastolic', color='#3498db', alpha=0.8)

# Add reference lines for normal BP
ax1.axhline(y=120, color='orange', linestyle='--', alpha=0.5, label='Systolic Target (120)')
ax1.axhline(y=80, color='lightblue', linestyle='--', alpha=0.5, label='Diastolic Target (80)')
ax1.axhline(y=140, color='red', linestyle=':', alpha=0.5, label='High BP Threshold (140)')
ax1.axhline(y=90, color='darkblue', linestyle=':', alpha=0.5, label='High BP Threshold (90)')

ax1.set_ylabel('Blood Pressure (mmHg)', fontsize=12, fontweight='bold')
ax1.set_title(f'Blood Pressure Trend - Patient {PATIENT_ID}',
              fontsize=14, fontweight='bold', pad=20)
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(bottom=0)

# Plot 2: Heart Rate
if df['heart_rate'].notna().any():
    ax2.plot(df['date'], df['heart_rate'], marker='o', linestyle='-',
             linewidth=2, markersize=4, color='#2ecc71', alpha=0.8)
    ax2.axhline(y=60, color='gray', linestyle='--', alpha=0.5, label='Normal Range')
    ax2.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Heart Rate (bpm)', fontsize=12, fontweight='bold')
    ax2.set_title('Heart Rate Trend', fontsize=12, fontweight='bold', pad=10)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(bottom=0)

# Format x-axis
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()

# Save plot
plot_filename = f'bp_trend_{PATIENT_ID}.png'
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
print(f"✓ Plot saved to {plot_filename}")

plt.show()

# Close connection
client.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nOutput files:")
print(f"  - {csv_filename} (data)")
print(f"  - {plot_filename} (visualization)")
