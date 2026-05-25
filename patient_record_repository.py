import csv
from patient_record import PatientRecord
from datetime import datetime

class PatientRecordRepository:
  def __init__(self, file_path: str):
    self.file_path = file_path
    self._data = [] 

  def load_csv(self):
    print(f"Membaca file dataset dari: {self.file_path}")
    self._data = [] 
    
    file = open(self.file_path, mode='r', encoding='utf-8')
    reader = csv.DictReader(file)
    
    for row in reader:
      record = PatientRecord(
        name=row['Name'],
        age=int(row['Age']),
        gender=row['Gender'],
        blood_type=row['Blood Type'],
        medical_condition=row['Medical Condition'],
        date_of_admission=datetime.strptime(row['Date of Admission'], '%Y-%m-%d'),
        insurance_provider=row['Insurance Provider'],
        billing_amount=float(row['Billing Amount']),
        room_number=int(row['Room Number']),
        admission_type=row['Admission Type'],
        discharge_date=datetime.strptime(row['Discharge Date'], '%Y-%m-%d'),
        medication=row['Medication'],
        test_results=row['Test Results']
      )
      self._data.append(record)
    
    file.close()

  def get_all_patients(self) -> list:
    return self._data

  def get_patients_by_condition(self, condition: str) -> list:
    filtered_patients = []
    for patient in self._data:
      if patient.medical_condition.lower() == condition.lower():
        filtered_patients.append(patient)
    return filtered_patients

  def get_patients_by_admission_type(self, admission_type: str) -> list:
    filtered_patients = []
    for patient in self._data:
      if patient.admission_type.lower() == admission_type.lower():
        filtered_patients.append(patient)
    return filtered_patients

  def calculate_average_billing(self, provider: str) -> float:
    total_billing = 0.0
    count = 0
    
    for patient in self._data:
      if patient.insurance_provider.lower() == provider.lower():
        total_billing += patient.billing_amount
        count += 1
        
    if count == 0:
      return 0.0
      
    return round(total_billing / count, 2)