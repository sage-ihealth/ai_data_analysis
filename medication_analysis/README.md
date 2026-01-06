# Medication Demographics Analysis

This project provides tools to analyze patient demographics based on medication usage by querying MongoDB collections.

## Overview

The analysis workflow:

1. Query the `medications` collection to find all distinct `memberId` values for a specific medication (e.g., "lisinopril")
2. Query the `uc_patients` collection to retrieve demographic information for those patients
3. Extract and analyze comprehensive demographic data including:
   - Basic demographics (age, gender, race)
   - Geographic distribution
   - Clinical information (diagnoses, conditions, protocols)
   - Physical measurements (height, weight, BMI)
   - Insurance and language preferences
   - Provider and clinic information
   - Enrollment and program status

## Files

- **[medication_demographics.py](medication_demographics.py)** - Core Python class for querying and extracting patient demographics
- **[medication_analysis.ipynb](medication_analysis.ipynb)** - Jupyter notebook for interactive analysis with visualizations
- **[test_analysis.py](test_analysis.py)** - Test script to verify the analysis works correctly
- **[apatient.json](apatient.json)** - Sample patient data for reference

## Requirements

Install the required Python packages:

```bash
pip install pymongo pandas numpy matplotlib seaborn jupyter
```

Or use the requirements file from the parent directory:

```bash
pip install -r ../requirements.txt
```

## Usage

### Option 1: Python Script

1. Update the MongoDB connection settings in [medication_demographics.py](medication_demographics.py:334):

```python
MONGO_URI = "mongodb://your-host:27017/"
DATABASE_NAME = "your_database_name"
MEDICATION_NAME = "lisinopril"
```

2. Run the analysis:

```bash
python medication_demographics.py
```

3. Results will be saved as:
   - `{medication}_demographics.csv`
   - `{medication}_demographics.json`

### Option 2: Jupyter Notebook (Recommended)

1. Start Jupyter:

```bash
jupyter notebook medication_analysis.ipynb
```

2. Update the configuration cell with your MongoDB connection details

3. Run all cells to perform the analysis with interactive visualizations

### Option 3: Use as a Python Module

```python
from medication_demographics import MedicationDemographicsAnalyzer

# Initialize analyzer
analyzer = MedicationDemographicsAnalyzer(
    mongo_uri="mongodb://localhost:27017/",
    database_name="your_database"
)

# Analyze a specific medication
df = analyzer.analyze_medication("lisinopril")

# Save results
analyzer.save_to_csv(df, "lisinopril_demographics.csv")
analyzer.save_to_json(df, "lisinopril_demographics.json")

# Close connection
analyzer.close()
```

## Extracted Demographics

The analysis extracts the following demographic fields:

### Basic Information
- Patient ID
- Medical Record ID
- Login ID
- First Name, Last Name
- Birthday, Age
- Gender, Gender Identity
- Race

### Contact Information
- City, State, Country
- Postcode

### Physical Measurements
- Height (cm)
- Weight (kg)
- BMI (calculated)

### Insurance
- Primary Insurance Provider
- Secondary Insurance Provider

### Language
- App Language
- Spoken Languages

### Clinical Information
- Patient Tech Level
- Complexity Level
- Protocol
- Control Level
- Diagnoses (comma-separated)
- ICD Codes (comma-separated)
- Patient Categories

### Enrollment
- Enrollment Status (ACTIVE, DISCHARGED, etc.)
- Enrollment Date
- Discharged Date
- Programs (CCM, RPM, etc.)

### Provider Information
- Doctor Name
- Doctor Title
- Doctor Email

### Clinic Information
- Clinic Name
- Clinic Business Name
- Clinic City
- Clinic State

### Care Team
- Assigned Care Advisor (CA)
- Assigned Registered Dietitian (RD)

### Timestamps
- Created At
- Updated At
- Timezone

## Analysis Features

The Jupyter notebook provides:

1. **Summary Statistics**
   - Total patient count
   - Age distribution
   - Gender and race breakdowns
   - Geographic distribution

2. **Visualizations**
   - State distribution bar chart
   - Enrollment status pie chart
   - BMI distribution histogram
   - Top diagnoses bar chart

3. **Clinical Analysis**
   - Most common diagnoses
   - Most common ICD codes
   - Complexity and protocol distribution
   - Program enrollment analysis

4. **Cross-tabulations**
   - Gender vs. enrollment status
   - Average age by race
   - Average BMI by complexity level

5. **Export Options**
   - CSV for spreadsheet analysis
   - JSON for programmatic use

## Example Queries

### Find patients taking a specific medication

```python
# Case-insensitive search
patient_ids = analyzer.get_patient_ids_by_medication("lisinopril")
```

### Get list of all medications

```python
medications = analyzer.get_medications_list(limit=100)
```

### Extract demographics for a specific patient

```python
from bson import ObjectId
demographics = analyzer.extract_patient_demographics(
    ObjectId("609ab581823ab800139c2669")
)
```

## Sample Output

```
Found 150 patients taking lisinopril

SUMMARY STATISTICS
================================================================================
Total patients: 150

Gender distribution:
M    85
F    65

Race distribution:
WHITE    60
ASIAN    45
HISPANIC 30
BLACK    15

State distribution:
CA    50
NY    25
TX    20
...

Enrollment status:
ACTIVE       100
DISCHARGED    45
PENDING        5
```

## MongoDB Collections

### medications collection
- **memberId**: ObjectId reference to patient
- **name**: Medication name (string)

### uc_patients collection
- **_id**: Patient ObjectId
- **profile**: Nested document with demographic information
- **address**: Array of address objects
- **patientListInfo**: Enrollment and program information
- **diagnoses**: Array of diagnosis codes
- **healthConditions**: Array of condition objects with ICD codes

## Testing

Run the test script to verify the setup:

```bash
python test_analysis.py
```

This will simulate the demographic extraction using the sample patient data in [apatient.json](apatient.json).

## Notes

- Medication name matching is case-insensitive
- All dates are converted to pandas datetime for easy analysis
- Missing values are handled gracefully
- BMI is automatically calculated when height and weight are available
- Results can be filtered and analyzed further using pandas DataFrames

## Troubleshooting

### Connection Issues
- Verify MongoDB URI is correct
- Check network connectivity to MongoDB server
- Ensure database name is correct

### No Results
- Verify medication name spelling
- Check that the medication exists in the medications collection
- Try the `get_medications_list()` method to see available medications

### Missing Fields
- Some patients may not have all demographic fields populated
- The analysis handles missing data gracefully with None/NaN values

## Next Steps

After running the analysis, you can:

1. Filter patients by specific criteria (age range, state, enrollment status)
2. Compare demographics across different medications
3. Analyze trends over time using enrollment and discharge dates
4. Cross-reference with other collections for deeper insights
5. Export results for presentation or reporting

## License

Internal use only.
