# SRP / Single Responsibility Principle 
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
        self.__gender = gender
        self.__age = age
        self.__hypertension = hypertension
        self.__heart_disease = heart_disease
        self.__smoking_history = smoking_history
        self.__bmi = bmi
        self.__hba1c_level = hba1c_level
        self.__blood_glucose_level = blood_glucose_level
        self.__diabetes = diabetes

    @property
    def gender(self) -> str:
        return self.__gender

    @property
    def age(self) -> int:
        return self.__age

    @property
    def hypertension(self) -> int:
        return self.__hypertension

    @property
    def heart_disease(self) -> int:
        return self.__heart_disease

    @property
    def smoking_history(self) -> str:
        return self.__smoking_history

    @property
    def bmi(self) -> float:
        return self.__bmi

    @property
    def hba1c_level(self) -> float:
        return self.__hba1c_level

    @property
    def blood_glucose_level(self) -> int:
        return self.__blood_glucose_level

    @property
    def diabetes(self) -> int:
        return self.__diabetes