from src.repositories.patient_data_reader import PatientDataReader

# DIP / Dependency Inversion Principle
class PatientRecordRepository:
    """
    Repository hanya fokus mengelola penyimpanan data di memori.
    Menerima sumber data apapun selama mengimplementasikan PatientDataReader.
    """
    def __init__(self, data_reader: PatientDataReader):
        self.__data_reader = data_reader
        self.__data: list = []
        self.__diabetic_patients = []

    def load(self):
        self.__data = self.__data_reader.read_patients()

    @property
    def data(self) -> list:
        """Getter untuk mengambil seluruh data list pasien"""
        return self.__data
    
    @property
    def diabetic_patients(self) -> list:
        """Getter untuk mengambil data list pasien diabetes"""
        for p in self.__data:
            if p.diabetes == 1:
                self.__diabetic_patients.append(p)
        return self.__diabetic_patients
