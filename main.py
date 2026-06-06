import sys
sys.dont_write_bytecode = True
import json
from src.repositories.patient_data_reader import CsvPatientDataReader
from src.repositories.patient_record_repository import PatientRecordRepository
from src.services.diabetes_analysis_service import DiabetesAnalysisService

def main():
    print("============================================")
    print("      DIABETES PREDICTION DATA ANALYSIS     ")
    print("      Object-Oriented Implementation        ")
    print("============================================\n")

    file_path = "./data/diabetes_dataset.csv"
    
    reader = CsvPatientDataReader(file_path)
    repo = PatientRecordRepository(reader)
    analysis_service = DiabetesAnalysisService(repo)
    
    print("Status Sistem: [!] Data belum dimuat ke memori. Silakan pilih Menu [1].")

    while True:
        print("\nMenu tersedia:")
        print("    [1]  Load Patient Dataset")
        print("    [2]  Analyze Diabetes cases by Gender")
        print("    [3]  Analyze Diabetes cases by Age Group")
        print("    [4]  Analyze Average HbA1c Levels")
        print("    [5]  Analyze Average Blood Glucose Levels")
        print("    [6]  Analyze Average BMI (Body Mass Index)")
        print("    [7]  Analyze Hypertension Risk Impact")
        print("    [8]  Analyze Smoking History Diabetes Prevalence")
        print("    [9]  View Comprehensive Summary (All Analyzers)")
        print("    [10] Export Full Report to JSON File")
        print("    [0]  Exit")

        choice = input("\nPilih menu (0-10): ")

        if choice == '1':
            print("\n[1] Loading Data from CSV file...")
            records = analysis_service.initialize_data()
            
            if not records:
                print("    -> Gagal memuat data atau file dataset kosong.")
            else:
                stats = analysis_service.get_overall_stats()
                print(f"    -> Sukses! Berhasil memuat {len(records):,} data pasien.")
                print(f"    -> Total Kasus Diabetes Terdeteksi: {stats['diabetic']:,} ({stats['percentage']}%)")
            continue

        if choice in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            if not analysis_service.is_data_initialized:
                print("\n❌ AKSER DITOLAK: Data belum di-load! Silakan pilih menu [1] terlebih dahulu.")
                continue

        if choice == '2':
            gender_data = analysis_service.get_diabetes_by_gender()
            print("\n[2] Diabetes Distribution by Gender:")
            for gender, count in gender_data.items():
                print(f"      {gender:<15} : {count:,} patients")

        elif choice == '3':
            age_data = analysis_service.get_diabetes_by_age_group()
            print("\n[3] Diabetes Distribution by Age Group:")
            for age_grp, count in age_data.items():
                print(f"      {age_grp:<15} : {count:,} patients")

        elif choice == '4':
            hba1c = analysis_service.get_analyze_hba1c()
            print("\n[4] Clinical Indicators - Average HbA1c Level:")
            print(f"      Diabetic Patients : {hba1c['avg_diabetes']}%")
            print(f"      Normal Patients   : {hba1c['avg_normal']}%")

        elif choice == '5':
            glucose = analysis_service.get_analyze_blood_glucose()
            print("\n[5] Clinical Indicators - Average Blood Glucose Level:")
            print(f"      Diabetic Patients : {glucose['avg_diabetes']} mg/dL")
            print(f"      Normal Patients   : {glucose['avg_normal']} mg/dL")

        elif choice == '6':
            bmi = analysis_service.get_analyze_bmi()
            print("\n[6] Clinical Indicators - Average BMI (Body Mass Index):")
            print(f"      Diabetic Patients : {bmi['avg_diabetes']} (Obese Class I)")
            print(f"      Normal Patients   : {bmi['avg_normal']} (Normal/Overweight)")

        elif choice == '7':
            ht = analysis_service.get_analyze_hypertension_risk()
            print("\n[7] Risk Factors - Hypertension Impact:")
            print(f"      Diabetes Rate with Hypertension    : {ht['diabetes_rate_with_hypertension']}%")
            print(f"      Diabetes Rate without Hypertension : {ht['diabetes_rate_without_hypertension']}%")
            print("      (Pasien dengan riwayat hipertensi memiliki rasio penularan jauh lebih tinggi)")

        elif choice == '8':
            smoking = analysis_service.get_analyze_smoking_impact()
            print("\n[8] Risk Factors - Smoking History Diabetes Prevalence:")
            for status, percentage in smoking.items():
                print(f"      {status:<15} : {percentage}% diabetes prevalence")

        elif choice == '9':
            print("\n[9] Comprehensive Summary from All Analyzers:")
            all_summaries = analysis_service.get_all_summaries()
            print(json.dumps(all_summaries, indent=4, ensure_ascii=False))

        elif choice == '10':
            output_filename = "diabetes_analysis_report.json"
            print("\n[10] Exporting Full Report to JSON...")
            analysis_service.export_report_to_json(output_filename)
            print(f"      -> Berhasil! Laporan lengkap disimpan ke file: '{output_filename}'")

        elif choice == '0':
            print("\nKeluar dari sistem analisis. Terima kasih!")
            break
            
        else:
            print("\nPilihan tidak valid. Silakan coba lagi menu (0-10).")

if __name__ == "__main__":
    main()