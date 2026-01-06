# Quick Start Guide

## Your MongoDB Connection

Based on your environment, use:

```python
import os
from dotenv import load_dotenv
from medication_demographics import MedicationDemographicsAnalyzer

# Load environment variables
load_dotenv()

# Get MongoDB URI (already includes database name)
mongo_uri = os.getenv('MONGO_DATABASE_URI')
# mongodb://ai:QXnwJV4XQndF@node1.uc-prod-mongo.ihealth-eng.com:27017,node2.uc-prod-mongo.ihealth-eng.com:27017,node3.uc-prod-mongo.ihealth-eng.com:27017/UnifiedCare?authSource=admin&replicaSet=rs0.prod

# Database name
database_name = "UnifiedCare"
```

## Basic Usage

### Option 1: Quick Analysis (Recommended)

```python
from medication_demographics import MedicationDemographicsAnalyzer

# Initialize (database name is in the URI)
analyzer = MedicationDemographicsAnalyzer(mongo_uri, "UnifiedCare")

# Analyze a medication
df = analyzer.analyze_medication("lisinopril")

# View results
print(f"Found {len(df)} patients")
print(df.head())

# Save results
analyzer.save_to_csv(df, "lisinopril_demographics.csv")
analyzer.close()
```

### Option 2: Using Jupyter Notebook

1. Open the notebook:
   ```bash
   jupyter notebook medication_analysis.ipynb
   ```

2. The configuration cell should have:
   ```python
   mongo_uri = os.getenv('MONGO_DATABASE_URI')
   DATABASE_NAME = "UnifiedCare"
   MEDICATION_NAME = "lisinopril"
   ```

3. Run all cells to see visualizations and analysis

## Common Medications to Analyze

Try analyzing these common medications:
- lisinopril (blood pressure)
- metformin (diabetes)
- atorvastatin (cholesterol)
- amlodipine (blood pressure)
- levothyroxine (thyroid)
- omeprazole (acid reflux)
- losartan (blood pressure)
- gabapentin (nerve pain)
- hydrochlorothiazide (blood pressure)
- metoprolol (heart/blood pressure)

## Quick Test

Run the example script:

```bash
python example_usage.py
```

This will:
1. Connect to your MongoDB
2. Query patients taking "lisinopril"
3. Extract demographics
4. Save to CSV
5. Show list of available medications

## Output Files

The analysis creates:
- `{medication}_demographics.csv` - Full demographic data in CSV format
- `{medication}_demographics.json` - Full demographic data in JSON format

## Fields Extracted

**Basic Demographics:**
- Name, age, gender, race
- City, state, country

**Clinical:**
- Diagnoses, ICD codes
- Protocols, complexity level
- Enrollment status, programs

**Physical:**
- Height, weight, BMI (calculated)

**Provider:**
- Doctor name, clinic name
- Care team assignments

**Insurance:**
- Primary and secondary insurance

And many more fields!

## Troubleshooting

### Error: "database names cannot contain the character '.'"
- **Fix:** Make sure `DATABASE_NAME = "UnifiedCare"` (not the full URI)

### Error: No results found
- Check medication spelling
- Use `analyzer.get_medications_list()` to see available medications

### Connection timeout
- Check VPN connection
- Verify MongoDB URI is correct
- Check network connectivity

## Next Steps

After getting results:

1. **Explore in Jupyter** - Use the notebook for visualizations
2. **Filter data** - Use pandas to filter by state, age, etc.
3. **Compare medications** - Run analysis on multiple medications
4. **Export reports** - Save filtered data for presentations

## Example: Filtering Results

```python
# After running the analysis
df = analyzer.analyze_medication("lisinopril")

# Filter by state
ca_patients = df[df['state'] == 'CA']

# Filter by age range
seniors = df[df['age'] >= 65]

# Filter by enrollment status
active_patients = df[df['enrolled_status'] == 'ACTIVE']

# Combine filters
active_ca_seniors = df[
    (df['state'] == 'CA') &
    (df['age'] >= 65) &
    (df['enrolled_status'] == 'ACTIVE')
]

print(f"Found {len(active_ca_seniors)} active CA seniors")
```

## Support

If you encounter issues:
1. Check your MongoDB URI in `.env` file
2. Verify you have the required packages installed
3. Run `python test_analysis.py` to verify the setup
4. Check the [README.md](README.md) for detailed documentation
