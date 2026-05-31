import sys
from src.repositories.patient_data_reader import CsvPatientDataReader
from src.repositories.patient_record_repository import PatientRecordRepository
from src.services.diabetes_analysis_service import DiabetesAnalysisService

def main():
  print("============================================")
  print("      DIABETES PREDICTION DATA ANALYSIS     ")
  print("      Object-Oriented Implementation        ")
  print("============================================\n")

  file_path = "./data/diabetes_dataset.csv"
  
  # Setup infra data access
  reader = CsvPatientDataReader(file_path)
  repo = PatientRecordRepository(reader)
  
  # Inisialisasi Service Layer dengan menyuntikkan repository
  analysis_service = DiabetesAnalysisService(repo)
  
  # Minta service untuk menyiapkan data sistem
  records = analysis_service.initialize_data()
  
  if not records:
    print("    -> Gagal memuat data atau data kosong. Program dihentikan.")
    sys.exit()
    
  print(f"    -> Loaded {len(records):,} patient records successfully.\n")

  # Looping Menu Interaktif CLI
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
      stats = analysis_service.get_overall_stats()
      print("\n[1] Overall Statistics:")
      print(f"      Total Patients Evaluated : {stats['total']:,}")
      print(f"      Total Positive Diabetes  : {stats['diabetic']:,}")
      print(f"      Overall Diabetes Rate    : {stats['percentage']}%")

    elif choice == '2':
      demo = analysis_service.get_demographic_analysis()
      print("\n[2] Diabetes Distribution by Demographic:")
      print("      --- Diabetes by Gender ---")
      for gender, count in demo['gender'].items():
        print(f"      {gender:<15} : {count:,} patients")
        
      print("\n      --- Diabetes by Age Group ---")
      for age_grp, count in demo['age_group'].items():
        print(f"      {age_grp:<15} : {count:,} patients")

    elif choice == '3':
      clinical = analysis_service.get_clinical_analysis()
      print("\n[3] Clinical Indicators Analysis:")
      print("      --- Average HbA1c Level ---")
      print(f"      Diabetic Patients : {clinical['hba1c']['avg_diabetes']}%")
      print(f"      Normal Patients   : {clinical['hba1c']['avg_normal']}%")
      
      print("\n      --- Average Blood Glucose Level ---")
      print(f"      Diabetic Patients : {clinical['glucose']['avg_diabetes']} mg/dL")
      print(f"      Normal Patients   : {clinical['glucose']['avg_normal']} mg/dL")
      
      print("\n      --- Average BMI (Body Mass Index) ---")
      print(f"      Diabetic Patients : {clinical['bmi']['avg_diabetes']} (Obese Class I)")
      print(f"      Normal Patients   : {clinical['bmi']['avg_normal']} (Normal/Overweight)")

    elif choice == '4':
      risk = analysis_service.get_risk_analysis()
      print("\n[4] Risk Factors & Comorbidities Analysis:")
      print("      --- Hypertension Impact ---")
      print(f"      Diabetes Rate with Hypertension    : {risk['hypertension']['diabetes_rate_with_hypertension']}%")
      print(f"      Diabetes Rate without Hypertension : {risk['hypertension']['diabetes_rate_without_hypertension']}%")
      print("      (Pasien hipertensi berisiko ~4x lipat lebih tinggi terkena diabetes)")
      
      print("\n      --- Smoking History Diabetes Prevalence ---")
      for status, percentage in risk['smoking'].items():
        print(f"      {status:<15} : {percentage}% diabetes prevalence")

    elif choice == '5':
      output_filename = "diabetes_analysis_report.json"
      print("\n[5] Exporting Full Report to JSON...")
      
      # Logika ekspor yang rumit kini didelegasikan penuh ke service
      analysis_service.export_report_to_json(output_filename)
      
      print(f"      -> Berhasil! Laporan lengkap disimpan ke file: '{output_filename}'")

    elif choice == '0':
      print("\nKeluar dari sistem analisis. Terima kasih!")
      break
      
    else:
      print("\nPilihan tidak valid. Silakan coba lagi menu (0-5).")

if __name__ == "__main__":
  main()