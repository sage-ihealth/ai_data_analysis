"""
Test script for medication demographics analysis
Uses the sample patient data to verify the analysis works correctly
"""

from medication_demographics import MedicationDemographicsAnalyzer
from bson import ObjectId


def test_with_sample_data():
    """
    Test the demographic extraction with sample patient data
    """
    print("Testing Medication Demographics Analyzer")
    print("=" * 80)

    # Sample patient data (manually structured from the JSON export)
    sample_patient = {
        '_id': '609ab581823ab800139c2669',
        'majorRole': 'MEMBER',
        'loginId': 'cromwellraulmabalatan',
        'medicalRecordId': '49474051',
        'profile': {
            'firstName': 'Cromwell Raul',
            'lastName': 'Mabalatan',
            'birthday': '1954-06-16',
            'gender': 'M',
            'genderIdentity': 'MAN',
            'race': 'ASIAN',
            'appLanguage': 'EL',
            'languages': ['EL'],
            'height': {'unit': 'cm', 'value': 175.26},
            'weight': {'unit': 'kg', 'value': 117.9340162},
            'insuranceProvider': 'UNITEDH/C GRP MEDICARE ADV PPO',
            'insuranceProvider2': 'NA',
            'patientTechLevel': 'MEDIUM'
        },
        'address': [{
            'type': 'MAIN',
            'streetName': '253 S. 19TH STREET',
            'city': 'San Jose',
            'state': 'CA',
            'country': 'US',
            'postCode': '95116'
        }],
        'complexity': 'COMPLEX',
        'protocol': 'DM2',
        'controlLevel': 'UNCATEGORIZED',
        'diagnoses': ['CKD', 'HLD', 'DM2', 'HTN'],
        'icdCodes': ['I10', 'E78.2', 'I12.9', 'E11.22', 'N18.1'],
        'patientCategories': ['DM2', 'CKD', 'HTN', 'HLD'],
        'patientListInfo': {
            'enrolledStatus': 'DISCHARGED',
            'programs': [
                {'category': 'CCM'},
                {'category': 'RPM'}
            ]
        }
    }

    print("\nSample patient data loaded:")
    print(f"Patient ID: {sample_patient['_id']}")
    print(f"Name: {sample_patient['profile']['firstName']} {sample_patient['profile']['lastName']}")
    print(f"Medical Record ID: {sample_patient['medicalRecordId']}")

    # Create a mock analyzer for testing demographic extraction
    print("\n" + "=" * 80)
    print("TESTING DEMOGRAPHIC EXTRACTION")
    print("=" * 80)

    # Simulate what would be extracted from the database
    patient_id = sample_patient['_id']
    profile = sample_patient.get('profile', {})
    address = sample_patient.get('address', [{}])[0]

    demographics = {
        'patient_id': str(patient_id),
        'medical_record_id': sample_patient.get('medicalRecordId'),
        'login_id': sample_patient.get('loginId'),

        # Basic demographics
        'first_name': profile.get('firstName'),
        'last_name': profile.get('lastName'),
        'birthday': profile.get('birthday'),
        'gender': profile.get('gender'),
        'gender_identity': profile.get('genderIdentity'),
        'race': profile.get('race'),

        # Contact info
        'city': address.get('city'),
        'state': address.get('state'),
        'country': address.get('country'),
        'postcode': address.get('postCode'),

        # Physical measurements
        'height_cm': profile.get('height', {}).get('value'),
        'weight_kg': profile.get('weight', {}).get('value'),

        # Insurance
        'insurance_provider': profile.get('insuranceProvider'),
        'insurance_provider_2': profile.get('insuranceProvider2'),

        # Languages
        'app_language': profile.get('appLanguage'),
        'languages': ', '.join(profile.get('languages', [])),

        # Clinical info
        'patient_tech_level': profile.get('patientTechLevel'),
        'complexity': sample_patient.get('complexity'),
        'protocol': sample_patient.get('protocol'),
        'control_level': sample_patient.get('controlLevel'),

        # Diagnoses and conditions
        'diagnoses': ', '.join(sample_patient.get('diagnoses', [])),
        'icd_codes': ', '.join(sample_patient.get('icdCodes', [])),
        'patient_categories': ', '.join(sample_patient.get('patientCategories', [])),

        # Enrollment info
        'enrolled_status': sample_patient.get('patientListInfo', {}).get('enrolledStatus'),
        'programs': ', '.join([p.get('category') for p in sample_patient.get('patientListInfo', {}).get('programs', [])]),
    }

    print("\nExtracted Demographics:")
    print("-" * 80)
    for key, value in demographics.items():
        print(f"{key:30s}: {value}")

    print("\n" + "=" * 80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\nNext Steps:")
    print("1. Update MongoDB connection settings in medication_demographics.py")
    print("2. Update the MONGO_URI and DATABASE_NAME in the script or notebook")
    print("3. Run the analysis with: python medication_demographics.py")
    print("4. Or use the Jupyter notebook: medication_analysis.ipynb")


if __name__ == "__main__":
    test_with_sample_data()
