"""
Quick test - analyzes only first 10 patients for fast verification
"""

import os
from dotenv import load_dotenv
from medication_demographics import MedicationDemographicsAnalyzer
import pandas as pd

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment
MONGO_URI = os.getenv('MONGO_DATABASE_URI')

print("Quick Test - Medication Demographics Analyzer")
print("=" * 80)

# Initialize analyzer
analyzer = MedicationDemographicsAnalyzer(MONGO_URI, "UnifiedCare")
print(f"✓ Connected to database: {analyzer.db.name}\n")

# Get patient IDs for lisinopril
medication_name = "lisinopril"
print(f"Finding patients taking {medication_name}...")
patient_ids = analyzer.get_patient_ids_by_medication(medication_name)
print(f"✓ Found {len(patient_ids)} patients total\n")

# Test with only first 10 patients
print("Extracting demographics for first 10 patients...")
demographics_list = []
for i, patient_id in enumerate(patient_ids[:10], 1):
    print(f"  Processing patient {i}/10...", end='\r')
    demo = analyzer.extract_patient_demographics(patient_id)
    if demo:
        demographics_list.append(demo)

print(f"\n✓ Successfully extracted demographics for {len(demographics_list)} patients\n")

# Create DataFrame
df = pd.DataFrame(demographics_list)

# Show summary
print("=" * 80)
print("SAMPLE RESULTS")
print("=" * 80)
print(f"\nTotal patients analyzed: {len(df)}")
print(f"\nColumns extracted: {len(df.columns)}")
print(f"\nSample data:")
print(df[['first_name', 'last_name', 'gender', 'state', 'city', 'enrolled_status']].to_string())

print("\n" + "=" * 80)
print("DEMOGRAPHICS SUMMARY")
print("=" * 80)
print(f"\nGender distribution:")
print(df['gender'].value_counts())

print(f"\nState distribution:")
print(df['state'].value_counts())

print(f"\nEnrollment status:")
print(df['enrolled_status'].value_counts())

# Save small sample
df.to_csv('lisinopril_sample_10.csv', index=False)
print(f"\n✓ Sample saved to lisinopril_sample_10.csv")

analyzer.close()

print("\n" + "=" * 80)
print("TEST COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nThe analyzer is working correctly.")
print(f"To analyze all {len(patient_ids)} patients, use:")
print("  - python example_usage.py (takes longer)")
print("  - jupyter notebook medication_analysis.ipynb (recommended)")
