class PatientRecord:
  def __init__(
    self, 
    gender: str, 
    age: float, 
    hypertension: int, 
    heart_disease: int, 
    smoking_history: str, 
    bmi: float, 
    hba1c_level: float, 
    blood_glucose_level: int, 
    diabetes: int
  ):
    self.gender = gender
    self.age = age
    self.hypertension = hypertension
    self.heart_disease = heart_disease
    self.smoking_history = smoking_history
    self.bmi = bmi
    self.hba1c_level = hba1c_level
    self.blood_glucose_level = blood_glucose_level
    self.diabetes = diabetes

  def has_diabetes(self) -> bool:
    """Mengembalikan True jika pasien terdiagnosis diabetes (angka 1)"""
    return self.diabetes == 1

  def has_hypertension(self) -> bool:
    """Mengembalikan True jika pasien memiliki hipertensi (angka 1)"""
    return self.hypertension == 1

  def has_heart_disease(self) -> bool:
    """Mengembalikan True jika pasien memiliki riwayat penyakit jantung (angka 1)"""
    return self.heart_disease == 1