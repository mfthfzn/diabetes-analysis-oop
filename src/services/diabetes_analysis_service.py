import json
from src.analyzers.diabetes_analyzers import DiabetesAnalyzer, ClinicalAnalyzer, RiskFactorAnalyzer
from src.repositories.patient_record_repository import PatientRecordRepository

class DiabetesAnalysisService:
    """
    SERVICE LAYER: Bertindak sebagai orchestrator (koordinator).
    Menghubungkan Presentasi (CLI) dengan Lapisan Bisnis (Analyzers) dan Repositori.
    """
    
    def __init__(self, repository: PatientRecordRepository):
        self.__repository = repository
        self.__diabetes_an = None
        self.__clinical_an = None
        self.__risk_an = None
        self.__analyzers = []
        self.__is_data_initialized = False

    def initialize_data(self) -> list:
        """Memerintahkan repository untuk load data dan menyebarkannya ke seluruh analyzer."""
        self.__repository.load()
        records = self.__repository.data

        if records:
            self.__diabetes_an = DiabetesAnalyzer(records)
            self.__clinical_an = ClinicalAnalyzer(records)
            self.__risk_an = RiskFactorAnalyzer(records)
            
            self.__analyzers = [
                self.__diabetes_an, 
                self.__clinical_an, 
                self.__risk_an
            ]
            self.__is_data_initialized = True

        return records

    @property
    def is_data_initialized(self) -> bool:
        """Getter untuk memeriksa apakah data sudah berhasil di-load ke sistem."""
        return self.__is_data_initialized

    def get_overall_stats(self) -> dict:
        return {
            "total": self.__diabetes_an.get_total_patients(),
            "diabetic": self.__diabetes_an.get_diabetic_count(),
            "percentage": self.__diabetes_an.get_diabetes_percentage()
        }

    def get_diabetes_by_gender(self) -> dict:
        return self.__diabetes_an.diabetes_by_gender()

    def get_diabetes_by_age_group(self) -> dict:
        return self.__diabetes_an.diabetes_by_age_group()

    def get_analyze_hba1c(self) -> dict:
        return self.__clinical_an.analyze_hba1c()

    def get_analyze_blood_glucose(self) -> dict:
        return self.__clinical_an.analyze_blood_glucose()

    def get_analyze_bmi(self) -> dict:
        return self.__clinical_an.analyze_bmi()

    def get_analyze_hypertension_risk(self) -> dict:
        return self.__risk_an.analyze_hypertension_risk()

    def get_analyze_smoking_impact(self) -> dict:
        return self.__risk_an.analyze_smoking_impact()

    def get_all_summaries(self) -> dict:
        """Mengambil keseluruhan laporan ringkasan menggunakan Polimorfisme."""
        combined_summaries = {}
        for analyzer in self.__analyzers:
            combined_summaries.update(analyzer.generate_summary())
        return combined_summaries

    def export_report_to_json(self, output_filename: str):
        """Menangani logika penyimpanan laporan komprehensif ke JSON."""
        full_report = {
            "metadata": {
                "total_records": self.__diabetes_an.get_total_patients(),
                "overall_diabetes_rate_percentage": self.__diabetes_an.get_diabetes_percentage()
            },
            "demographics": self.__diabetes_an.generate_summary(),
            "clinical_indicators": self.__clinical_an.generate_summary(),
            "risk_factors": self.__risk_an.generate_summary()
        }

        with open(output_filename, mode="w", encoding="utf-8") as file_output:
            json.dump(full_report, file_output, indent=2)