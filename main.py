import sys
import json
from src.patient_data_reader import CsvPatientDataReader
from src.patient_record_repository import PatientRecordRepository
from src.analyzers import DiabetesAnalyzer, ClinicalAnalyzer, RiskFactorAnalyzer

def main():
  print("============================================")
  print("      DIABETES PREDICTION DATA ANALYSIS     ")
  print("      Object-Oriented Implementation        ")
  print("============================================\n")

  file_path = "./data/diabetes_dataset.csv"
  
  reader = CsvPatientDataReader(file_path)
  repo = PatientRecordRepository(reader)
  
  repo.load()
  records = repo.get_all_patients()
  
  if not records:
    print("    -> Gagal memuat data atau data kosong. Program dihentikan.")
    sys.exit()
    
  print(f"    -> Loaded {len(records):,} patient records successfully.\n")

  diabetes_an = DiabetesAnalyzer(records)
  clinical_an = ClinicalAnalyzer(records)
  risk_an = RiskFactorAnalyzer(records)

  while True:
    print("\nMenu tersedia:")
    print("    [1] Overall statistics")
    print("    [2] Diabetes distribution by gender & age")
    print("    [3] Clinical indicators analysis (HbA1c, Glucose, BMI)")
    print("    [4] Risk factors & comorbidities analysis")
    print("    [5] Export full report to JSON")
    print("    [0] Exit")

    choice = input("\nPilih menu (0-5): ")

    if choice == '1':
      print("\n[1] Overall Statistics:")
      print(f"      Total Patients Evaluated : {diabetes_an.get_total_patients():,}")
      print(f"      Total Positive Diabetes  : {diabetes_an.get_diabetic_count():,}")
      print(f"      Overall Diabetes Rate    : {diabetes_an.get_diabetes_percentage()}%")

    elif choice == '2':
      print("\n[2] Diabetes Distribution by Demographic:")
      print("      --- Diabetes by Gender ---")
      for gender, count in diabetes_an.diabetes_by_gender().items():
        print(f"      {gender:<15} : {count:,} patients")
        
      print("\n      --- Diabetes by Age Group ---")
      for age_grp, count in diabetes_an.diabetes_by_age_group().items():
        print(f"      {age_grp:<15} : {count:,} patients")

    elif choice == '3':
      print("\n[3] Clinical Indicators Analysis:")
      hba1c_data = clinical_an.analyze_hba1c()
      glucose_data = clinical_an.analyze_blood_glucose()
      bmi_data = clinical_an.analyze_bmi()

      print("      --- Average HbA1c Level ---")
      print(f"      Diabetic Patients : {hba1c_data['avg_diabetes']}%")
      print(f"      Normal Patients   : {hba1c_data['avg_normal']}%")
      
      print("\n      --- Average Blood Glucose Level ---")
      print(f"      Diabetic Patients : {glucose_data['avg_diabetes']} mg/dL")
      print(f"      Normal Patients   : {glucose_data['avg_normal']} mg/dL")
      
      print("\n      --- Average BMI (Body Mass Index) ---")
      print(f"      Diabetic Patients : {bmi_data['avg_diabetes']} (Obese Class I)")
      print(f"      Normal Patients   : {bmi_data['avg_normal']} (Normal/Overweight)")

    elif choice == '4':
      print("\n[4] Risk Factors & Comorbidities Analysis:")
      ht_data = risk_an.analyze_hypertension_risk()
      smoke_data = risk_an.analyze_smoking_impact()

      print("      --- Hypertension Impact ---")
      print(f"      Diabetes Rate with Hypertension    : {ht_data['diabetes_rate_with_hypertension']}%")
      print(f"      Diabetes Rate without Hypertension : {ht_data['diabetes_rate_without_hypertension']}%")
      print("      (Pasien hipertensi berisiko ~4x lipat lebih tinggi terkena diabetes)")
      
      print("\n      --- Smoking History Diabetes Prevalence ---")
      for status, percentage in smoke_data.items():
        print(f"      {status:<15} : {percentage}% diabetes prevalence")

    elif choice == '5':
      print("\n[5] Exporting Full Report to JSON...")
      
      full_report = {
        "metadata": {
          "total_records": diabetes_an.get_total_patients(),
          "overall_diabetes_rate_percentage": diabetes_an.get_diabetes_percentage()
        },
        "demographics": diabetes_an.generate_summary(),
        "clinical_indicators": clinical_an.generate_summary(),
        "risk_factors": risk_an.generate_summary()
      }
      
      output_filename = "diabetes_analysis_report.json"
      
      file_output = open(output_filename, mode='w', encoding='utf-8')
      json.dump(full_report, file_output, indent=2)
      file_output.close()
      
      print(f"      -> Berhasil! Laporan lengkap disimpan ke file: '{output_filename}'")

    elif choice == '0':
      print("\nKeluar dari sistem analisis. Terima kasih!")
      break
      
    else:
      print("\nPilihan tidak valid. Silakan coba lagi menu (0-5).")

if __name__ == "__main__":
  main()