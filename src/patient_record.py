from dataclasses import dataclass

#SRP / Single Responsibility Principle 
@dataclass
class PatientRecord:
  gender: str
  age: int
  hypertension: int
  heart_disease: int
  smoking_history: str
  bmi: float
  hba1c_level: float
  blood_glucose_level: int
  diabetes: int

  def __post_init__(self):
    if isinstance(self.gender, str):
      self.gender = self.gender.strip()
    if isinstance(self.smoking_history, str):
      self.smoking_history = self.smoking_history.strip()

  def has_diabetes(self) -> bool:
    return self.diabetes == 1

  def has_hypertension(self) -> bool:
    return self.hypertension == 1

  def has_heart_disease(self) -> bool:
    return self.heart_disease == 1