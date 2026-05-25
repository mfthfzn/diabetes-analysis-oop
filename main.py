import os
import sys
from patient_record_repository import PatientRecordRepository
from analyzers import BaseAnalyzer, DemographicAnalyzer, FinancialAnalyzer, OperationalAnalyzer

def main():
  # Tampilan Header Sistem
  print("============================================")
  print("      HEALTHCARE DATA ANALYSIS SYSTEM       ")
  print("      Object-Oriented Implementation        ")
  print("============================================\n")

  # Menentukan lokasi file (pastikan file CSV ada di lokasi ini)
  file_path = "healthcare_dataset.csv"
  
  # Jika diletakkan di dalam folder 'data', Anda bisa memakai: 
  # file_path = os.path.join("data", "healthcare_dataset.csv")
  
  # 1. Inisialisasi Repository dan Muat Data
  repo = PatientRecordRepository(file_path)
  
  try:
    repo.load_csv()
  except FileNotFoundError:
    print(f"[!] Error: File '{file_path}' tidak ditemukan.")
    print("    Pastikan nama file dan lokasinya sudah benar.")
    sys.exit()

  # 2. Ambil data pasien dari repository
  records = repo.get_all_patients()
  
  if not records:
    print("    -> Gagal memuat data atau data kosong. Program dihentikan.")
    sys.exit()
    
  print(f"    -> Loaded {len(records):,} patients successfully.\n")

  # 3. Inisialisasi semua objek Analyzer menggunakan data dari repository
  base_analyzer = BaseAnalyzer(records)
  ops_analyzer = OperationalAnalyzer(records)
  fin_analyzer = FinancialAnalyzer(records)
  demo_analyzer = DemographicAnalyzer(records)

  # 4. Looping Menu Interaktif
  while True:
    print("\nMenu tersedia:")
    print("    [1] Overall patient statistics")
    print("    [2] Operational analysis (Stay & Admission)")
    print("    [3] Financial analysis (Billing by Insurance)")
    print("    [4] Demographic analysis (Age & Gender)")
    print("    [5] Run full analysis report")
    print("    [0] Exit")

    choice = input("\nPilih menu (0-5): ")

    if choice == '1':
      print("\n[1] Overall Patient Statistics:")
      print(f"      Total Patients in System : {base_analyzer.get_total_patients():,}")

    elif choice == '2':
      print("\n[2] Operational Analysis:")
      print("      --- Avg Stay by Condition ---")
      for cond, days in ops_analyzer.avg_stay_by_condition().items():
        print(f"      {cond:<15} : {days} days")
        
      print("\n      --- Admission Type Distribution ---")
      for adm, count in ops_analyzer.admission_type_distribution().items():
        print(f"      {adm:<15} : {count:,} patients")

    elif choice == '3':
      print("\n[3] Financial Analysis:")
      print("      --- Avg Billing by Insurance ---")
      for prov, bill in fin_analyzer.avg_billing_by_insurance().items():
        print(f"      {prov:<15} : ${bill:,.2f}")

    elif choice == '4':
      print("\n[4] Demographic Analysis:")
      print("      --- Age Group Distribution ---")
      for age_grp, count in demo_analyzer.age_group_distribution().items():
        print(f"      {age_grp:<15} : {count:,} patients")
        
      print("\n      --- Medical Condition by Gender ---")
      for gen, conds in demo_analyzer.medical_condition_by_gender().items():
        print(f"      [{gen.upper()}]")
        for c, count in conds.items():
          print(f"        - {c:<12} : {count:,} cases")

    elif choice == '5':
      print("\n============================================")
      print("             FULL ANALYSIS REPORT           ")
      print("============================================")
      
      print(f"\n[1] Total Patients: {base_analyzer.get_total_patients():,}")
      
      print("\n[2] Top 3 Longest Stays by Condition:")
      stays = list(ops_analyzer.avg_stay_by_condition().items())[:3]
      for cond, days in stays:
        print(f"      {cond:<15} : {days} days")
        
      print("\n[3] Top 3 Highest Billing Insurance:")
      bills = list(fin_analyzer.avg_billing_by_insurance().items())[:3]
      for prov, bill in bills:
        print(f"      {prov:<15} : ${bill:,.2f}")
        
      print("\n[4] Patient Demographics:")
      for age_grp, count in demo_analyzer.age_group_distribution().items():
        print(f"      {age_grp:<15} : {count:,} patients")
        
      print("\n============================================")
      print("  Analysis complete. All methods executed.  ")
      print("============================================")

    elif choice == '0':
      print("\nKeluar dari sistem. Terima kasih!")
      break
      
    else:
      print("\nPilihan tidak valid. Silakan coba lagi.")

# Titik eksekusi program utama
if __name__ == "__main__":
  main()