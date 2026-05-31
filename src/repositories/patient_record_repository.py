from src.repositories.patient_data_reader import PatientDataReader

# DIP / Dependency Inversion Principle
class PatientRecordRepository:
  """
  Repository hanya fokus mengelola penyimpanan data di memori.
  Menerima sumber data apapun selama mengimplementasikan PatientDataReader.
  """
  def __init__(self, data_reader: PatientDataReader):
    self._data_reader = data_reader
    self._data = []

  def load(self):
    self._data = self._data_reader.read_patients()

  def get_all_patients(self) -> list:
    return self._data

  def get_diabetic_patients(self) -> list:
    diabetic_patients = []
    for p in self._data:
      if p.has_diabetes():
        diabetic_patients.append(p)
    return diabetic_patients