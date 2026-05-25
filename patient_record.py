from datetime import datetime

class PatientRecord:
  def __init__(
    self, 
    name: str, 
    age: int, 
    gender: str, 
    blood_type: str, 
    medical_condition: str, 
    date_of_admission: datetime, 
    insurance_provider: str, 
    billing_amount: float, 
    room_number: int, 
    admission_type: str, 
    discharge_date: datetime, 
    medication: str, 
    test_results: str
  ):
    self.name = name
    self.age = age
    self.gender = gender
    self.blood_type = blood_type
    self.medical_condition = medical_condition
    self.date_of_admission = date_of_admission
    self.insurance_provider = insurance_provider
    self.billing_amount = billing_amount
    self.room_number = room_number
    self.admission_type = admission_type
    self.discharge_date = discharge_date
    self.medication = medication
    self.test_results = test_results

  def get_length_of_stay(self) -> int:
    """Menghitung berapa lama pasien dirawat (dalam hari)"""
    return (self.discharge_date - self.date_of_admission).days

  def is_senior_citizen(self) -> bool:
    """Mengecek apakah pasien tergolong lansia (>= 60 tahun)"""
    return self.age >= 60

  def is_high_billing(self, threshold: float = 30000.0) -> bool:
    """Mengecek apakah biaya tagihan pasien termasuk mahal"""
    return self.billing_amount > threshold