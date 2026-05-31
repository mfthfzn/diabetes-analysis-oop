import json
from src.analyzers.diabetes_analyzers import DiabetesAnalyzer, ClinicalAnalyzer, RiskFactorAnalyzer
from src.repositories.patient_record_repository import PatientRecordRepository

class DiabetesAnalysisService:
  """
  SERVICE LAYER: Bertindak sebagai orchestrator (koordinator).
  Menghubungkan Presentasi (CLI) dengan Lapisan Bisnis
  (Analyzers) dan Repositori.
  """
  
  def __init__(self, repository: PatientRecordRepository):
    self._repository = repository
    self._diabetes_an = None
    self._clinical_an = None
    self._risk_an = None

  def initialize_data(self) -> list:
    """
    Memerintahkan repository untuk load data
    dan menyebarkannya ke seluruh analyzer.
    """
    self._repository.load()
    records = self._repository.get_all_patients()

    if records:
      self._diabetes_an = DiabetesAnalyzer(records)
      self._clinical_an = ClinicalAnalyzer(records)
      self._risk_an = RiskFactorAnalyzer(records)

    return records

  def get_overall_stats(self) -> dict:
    return {
      "total": self._diabetes_an.get_total_patients(),
      "diabetic": self._diabetes_an.get_diabetic_count(),
      "percentage": self._diabetes_an.get_diabetes_percentage()
    }

  def get_demographic_analysis(self) -> dict:
    return {
      "gender": self._diabetes_an.diabetes_by_gender(),
      "age_group": self._diabetes_an.diabetes_by_age_group()
    }

  def get_clinical_analysis(self) -> dict:
    return {
      "hba1c": self._clinical_an.analyze_hba1c(),
      "glucose": self._clinical_an.analyze_blood_glucose(),
      "bmi": self._clinical_an.analyze_bmi()
    }

  def get_risk_analysis(self) -> dict:
    return {
      "hypertension": self._risk_an.analyze_hypertension_risk(),
      "smoking": self._risk_an.analyze_smoking_impact()
    }

  def export_report_to_json(self, output_filename: str):
    """
    Menangani logika pembuatan dan
    penyimpanan laporan JSON.
    """
    full_report = {
      "metadata": {
        "total_records": self._diabetes_an.get_total_patients(),
        "overall_diabetes_rate_percentage":
          self._diabetes_an.get_diabetes_percentage()
      },
      "demographics": self._diabetes_an.generate_summary(),
      "clinical_indicators": self._clinical_an.generate_summary(),
      "risk_factors": self._risk_an.generate_summary()
    }

    with open(
      output_filename,
      mode="w",
      encoding="utf-8"
    ) as file_output:
      json.dump(full_report, file_output, indent=2)
