"""
Example usage of the Medication Demographics Analyzer
Shows different ways to connect and analyze medications
"""

import os
from dotenv import load_dotenv
from medication_demographics import MedicationDemographicsAnalyzer

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment
MONGO_URI = os.getenv('MONGO_DATABASE_URI')

# Option 1: Let the analyzer get the database from the URI
print("Option 1: Using database from URI")
print("=" * 80)
analyzer = MedicationDemographicsAnalyzer(MONGO_URI)
print(f"Connected to database: {analyzer.db.name}")

# Analyze a medication
medication_name = "lisinopril"
df = analyzer.analyze_medication(medication_name)

# Show summary
print(f"\nFound {len(df)} patients taking {medication_name}")
if len(df) > 0:
    print("\nSample demographics:")
    print(df[['first_name', 'last_name', 'age', 'gender', 'state', 'enrolled_status']].head())

# Save results
if len(df) > 0:
    analyzer.save_to_csv(df, f'{medication_name}_demographics.csv')
    print(f"\nResults saved to {medication_name}_demographics.csv")

analyzer.close()

print("\n" + "=" * 80)
print("Option 2: Explicitly specify database name")
print("=" * 80)

# Option 2: Explicitly specify the database name
analyzer2 = MedicationDemographicsAnalyzer(MONGO_URI, "UnifiedCare")
print(f"Connected to database: {analyzer2.db.name}")

# Get list of available medications
print("\nGetting list of medications...")
medications = analyzer2.get_medications_list(limit=20)
print(f"\nSample medications in database (first 20):")
for i, med in enumerate(medications[:20], 1):
    print(f"{i:2d}. {med}")

analyzer2.close()

print("\nAnalysis complete!")
