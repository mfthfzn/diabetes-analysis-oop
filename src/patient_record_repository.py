import csv
from src.patient_record import PatientRecord

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
        gender=row['gender'],
        age=float(row['age']),
        hypertension=int(row['hypertension']),
        heart_disease=int(row['heart_disease']),
        smoking_history=row['smoking_history'],
        bmi=float(row['bmi']),
        hba1c_level=float(row['HbA1c_level']),
        blood_glucose_level=int(row['blood_glucose_level']),
        diabetes=int(row['diabetes'])
      )
      self._data.append(record)
    
    file.close()

  def get_all_patients(self) -> list:
    """Mengembalikan seluruh data pasien"""
    return self._data

  def get_diabetic_patients(self) -> list:
    """Memfilter dan mengembalikan daftar pasien yang positif diabetes"""
    filtered_patients = []
    for patient in self._data:
      if patient.has_diabetes():
        filtered_patients.append(patient)
    return filtered_patients

  def get_patients_by_gender(self, gender: str) -> list:
    """Memfilter data pasien berdasarkan jenis kelamin ('Male' atau 'Female')"""
    filtered_patients = []
    for patient in self._data:
      if patient.gender.lower() == gender.lower():
        filtered_patients.append(patient)
    return filtered_patients

  def get_patients_with_heart_disease(self) -> list:
    """Memfilter dan mengembalikan daftar pasien dengan penyakit jantung"""
    filtered_patients = []
    for patient in self._data:
      if patient.has_heart_disease():
        filtered_patients.append(patient)
    return filtered_patients