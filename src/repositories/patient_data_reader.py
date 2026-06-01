import csv
from abc import ABC, abstractmethod
from src.models.patient_record import PatientRecord

# DIP / Dependency Inversion Principle
class PatientDataReader(ABC):
    """
    Interface (Abstract Class) untuk membaca data dari berbagai sumber data.
    Memenuhi prinsip DIP (Masing-masing komponen bergantung pada abstraksi).
    """
    @abstractmethod
    def read_patients(self) -> list:
        pass

class CsvPatientDataReader(PatientDataReader):
    def __init__(self, file_path : str):
        self.__file_path = file_path

    def read_patients(self) -> list:
        if not self.__file_path:
            print("[!] Error: file_path belum diatur. Gunakan setter '.file_path = ...' sebelum membaca data.")
            return []

        patients = []
        try:
            file = open(self.__file_path, mode='r', encoding='utf-8')
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
                patients.append(record)
            file.close()
        except FileNotFoundError:
            print(f"[!] File {self.__file_path} tidak ditemukan.")
        
        return patients