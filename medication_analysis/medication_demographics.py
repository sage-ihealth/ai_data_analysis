"""
Medication Demographics Analysis
Finds all patients taking a specific medication and extracts their demographic information
"""

import pymongo
import pandas as pd
from typing import List, Dict, Optional
from bson import ObjectId
import json


class MedicationDemographicsAnalyzer:
    """Analyze patient demographics for specific medications"""

    def __init__(self, mongo_uri: str, database_name: str = None):
        """
        Initialize the analyzer with MongoDB connection

        Args:
            mongo_uri: MongoDB connection string
            database_name: Name of the database to query. If None, will use the
                          database specified in the URI or get_default_database()
        """
        self.client = pymongo.MongoClient(mongo_uri)

        # If database_name is provided, use it; otherwise try to get from URI
        if database_name:
            self.db = self.client[database_name]
        else:
            # Try to get the default database from the URI
            self.db = self.client.get_default_database()

        self.medications_collection = self.db['medications']
        self.patients_collection = self.db['uc_patients']

    def get_patient_ids_by_medication(self, medication_name: str) -> List[ObjectId]:
        """
        Find distinct patient IDs taking a specific medication (limited to the first match)

        Args:
            medication_name: Name of the medication (case-insensitive)

        Returns:
            List of patient ObjectIds
        """
        # Use case-insensitive regex for medication name and limit to first matching patient
        pipeline = [
            {"$match": {"name": {"$regex": f"^{medication_name}$", "$options": "i"}}},
            {"$group": {"_id": "$memberId"}},
            {"$limit": 100},
        ]
        member_ids = [doc["_id"] for doc in self.medications_collection.aggregate(pipeline)]
        print(f"Found {len(member_ids)} patient(s) taking {medication_name} (limited to top 1)")
        return member_ids

    def extract_patient_demographics(self, patient_id: ObjectId) -> Optional[Dict]:
        """
        Extract demographic information from a patient record

        Args:
            patient_id: Patient's ObjectId

        Returns:
            Dictionary with demographic information
        """
        patient = self.patients_collection.find_one({"_id": patient_id})

        if not patient:
            return None

        profile = patient.get('profile', {})
        address = patient.get('address', [{}])[0] if patient.get('address') else {}

        demographics = {
            'patient_id': str(patient_id),
            'medical_record_id': patient.get('medicalRecordId'),
            'login_id': patient.get('loginId'),

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
            'height_cm': profile.get('height', {}).get('value') if profile.get('height', {}).get('unit') == 'cm' else None,
            'weight_kg': profile.get('weight', {}).get('value') if profile.get('weight', {}).get('unit') == 'kg' else None,

            # Insurance
            'insurance_provider': profile.get('insuranceProvider'),
            'insurance_provider_2': profile.get('insuranceProvider2'),

            # Languages
            'app_language': profile.get('appLanguage'),
            'languages': ', '.join(profile.get('languages', [])) if isinstance(profile.get('languages'), list) else str(profile.get('languages', '')),

            # Clinical info
            'patient_tech_level': profile.get('patientTechLevel'),
            'complexity': patient.get('complexity'),
            'protocol': patient.get('protocol'),
            'control_level': patient.get('controlLevel'),

            # Diagnoses and conditions
            'diagnoses': ', '.join(patient.get('diagnoses', [])) if isinstance(patient.get('diagnoses'), list) else str(patient.get('diagnoses', '')),
            'icd_codes': ', '.join(patient.get('icdCodes', [])) if isinstance(patient.get('icdCodes'), list) else str(patient.get('icdCodes', '')),
            'patient_categories': ', '.join(patient.get('patientCategories', [])) if isinstance(patient.get('patientCategories'), list) else str(patient.get('patientCategories', '')),

            # Enrollment info
            'enrolled_status': patient.get('patientListInfo', {}).get('enrolledStatus'),
            'enrollment_date': patient.get('patientListInfo', {}).get('enrollmentDate'),
            'discharged_at': patient.get('patientListInfo', {}).get('dischargedAt'),

            # Programs
            'programs': ', '.join([p.get('category', '') for p in patient.get('patientListInfo', {}).get('programs', []) if isinstance(p, dict)]) if patient.get('patientListInfo', {}).get('programs') else '',

            # Provider info
            'doctor_name': f"{profile.get('doctorUser', {}).get('firstName', '')} {profile.get('doctorUser', {}).get('lastName', '')}".strip(),
            'doctor_title': profile.get('doctorUser', {}).get('title'),
            'doctor_email': profile.get('doctorUser', {}).get('email'),

            # Clinic info
            'clinic_name': patient.get('clinic', {}).get('nickName'),
            'clinic_business_name': patient.get('clinic', {}).get('businessName'),
            'clinic_city': patient.get('clinic', {}).get('city'),
            'clinic_state': patient.get('clinic', {}).get('state'),

            # Care team
            'assigned_ca': f"{patient.get('assignedToCAUser', {}).get('firstName', '')} {patient.get('assignedToCAUser', {}).get('lastName', '')}".strip(),
            'assigned_rd': f"{patient.get('assignedToRDUser', {}).get('firstName', '')} {patient.get('assignedToRDUser', {}).get('lastName', '')}".strip(),

            # Dates
            'created_at': patient.get('createdAt'),
            'updated_at': patient.get('updatedAt'),
            'timezone': patient.get('timezone'),
        }

        return demographics

    def analyze_medication(self, medication_name: str) -> pd.DataFrame:
        """
        Get complete demographic analysis for all patients taking a medication

        Args:
            medication_name: Name of the medication to analyze

        Returns:
            DataFrame with demographic information for all patients
        """
        print(f"Analyzing demographics for patients taking: {medication_name}")

        # Get all patient IDs
        patient_ids = self.get_patient_ids_by_medication(medication_name)
         
        # Extract demographics for each patient
        demographics_list = []
        for patient_id in patient_ids:
            demo = self.extract_patient_demographics(patient_id)
            if demo:
                demographics_list.append(demo)

        # Create DataFrame
        df = pd.DataFrame(demographics_list)
        print(f"Successfully extracted demographics for {len(df)} patients")

        return df

    def get_medications_list(self, limit: int = 100) -> List[str]:
        """
        Get a list of unique medication names in the database

        Args:
            limit: Maximum number of medications to return

        Returns:
            List of medication names
        """
        medications = self.medications_collection.distinct("name")
        return sorted(medications)[:limit]

    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """Save DataFrame to CSV file"""
        df.to_csv(filename, index=False)
        print(f"Saved results to {filename}")

    def save_to_json(self, df: pd.DataFrame, filename: str):
        """Save DataFrame to JSON file"""
        df.to_json(filename, orient='records', indent=2, date_format='iso')
        print(f"Saved results to {filename}")

    def close(self):
        """Close MongoDB connection"""
        self.client.close()


def main():
    """Example usage"""
    # Configuration
    MONGO_URI = "mongodb://localhost:27017/"  # Update with your MongoDB URI
    DATABASE_NAME = "your_database"  # Update with your database name
    MEDICATION_NAME = "lisinopril"  # Medication to analyze

    # Initialize analyzer
    analyzer = MedicationDemographicsAnalyzer(MONGO_URI, DATABASE_NAME)

    try:
        # Analyze medication
        df = analyzer.analyze_medication(MEDICATION_NAME)

        # Display summary statistics
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(f"Total patients: {len(df)}")
        print(f"\nGender distribution:")
        print(df['gender'].value_counts())
        print(f"\nRace distribution:")
        print(df['race'].value_counts())
        print(f"\nState distribution:")
        print(df['state'].value_counts().head(10))
        print(f"\nEnrollment status:")
        print(df['enrolled_status'].value_counts())

        # Save results
        analyzer.save_to_csv(df, f'medication_analysis/{MEDICATION_NAME}_demographics.csv')
        analyzer.save_to_json(df, f'medication_analysis/{MEDICATION_NAME}_demographics.json')

    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
