from src.repositories.patient_data_reader import CsvPatientDataReader
from src.repositories.patient_record_repository import PatientRecordRepository
from src.analyzers.diabetes_analyzers import DiabetesAnalyzer, ClinicalAnalyzer, RiskFactorAnalyzer

file_path = "./data/diabetes_dataset.csv"
reader = CsvPatientDataReader(file_path)
repo = PatientRecordRepository(reader)

repo.load()
real_data = repo.data 

# =====================================================================
# --- A. VALIDASI METHOD DI BASE / DIABETES ANALYZER ---
# =====================================================================

def test_get_total_patients():
    analyzer = DiabetesAnalyzer(real_data)
    total = analyzer.get_total_patients()
    assert isinstance(total, int), "Output harus berupa angka bulat (integer)"
    assert total > 0, "Total pasien harus lebih dari 0"

def test_get_diabetic_count():
    analyzer = DiabetesAnalyzer(real_data)
    count = analyzer.get_diabetic_count()
    assert isinstance(count, int), "Output harus berupa angka bulat (integer)"
    assert count <= analyzer.get_total_patients(), "Jumlah pasien diabetes tidak boleh melebihi total pasien"

def test_get_diabetes_percentage():
    analyzer = DiabetesAnalyzer(real_data)
    percentage = analyzer.get_diabetes_percentage()
    assert isinstance(percentage, float), "Output harus berupa angka desimal (float)"
    assert 0 <= percentage <= 100, "Persentase harus berada di rentang 0 - 100%"

def test_diabetes_by_gender():
    analyzer = DiabetesAnalyzer(real_data)
    result = analyzer.diabetes_by_gender()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "Female" in result or "Male" in result, "Kategori gender tidak valid"

def test_diabetes_by_age_group():
    analyzer = DiabetesAnalyzer(real_data)
    result = analyzer.diabetes_by_age_group()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "Anak-anak (<18)" in result, "Kategori Anak-anak hilang"
    assert "Dewasa (18-59)" in result, "Kategori Dewasa hilang"
    assert "Lansia (>=60)" in result, "Kategori Lansia hilang"

def test_diabetes_generate_summary():
    analyzer = DiabetesAnalyzer(real_data)
    summary = analyzer.generate_summary()
    assert isinstance(summary, dict), "Output harus berupa dictionary"
    assert "total_diabetes_patients" in summary
    assert "demographic_by_gender" in summary
    assert "demographic_by_age" in summary


# =====================================================================
# --- B. VALIDASI METHOD DI CLINICAL ANALYZER ---
# =====================================================================

def test_analyze_hba1c():
    analyzer = ClinicalAnalyzer(real_data)
    result = analyzer.analyze_hba1c()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "avg_diabetes" in result and "avg_normal" in result
    assert result["avg_diabetes"] > 0, "Nilai rata-rata HbA1c diabetes tidak boleh 0"
    assert result["avg_normal"] > 0, "Nilai rata-rata HbA1c normal tidak boleh 0"

def test_analyze_blood_glucose():
    analyzer = ClinicalAnalyzer(real_data)
    result = analyzer.analyze_blood_glucose()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "avg_diabetes" in result and "avg_normal" in result
    assert result["avg_diabetes"] > 0, "Nilai glukosa diabetes tidak valid"
    assert result["avg_normal"] > 0, "Nilai glukosa normal tidak valid"

def test_analyze_bmi():
    analyzer = ClinicalAnalyzer(real_data)
    result = analyzer.analyze_bmi()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "avg_diabetes" in result and "avg_normal" in result
    assert result["avg_diabetes"] > 0, "Nilai BMI diabetes tidak valid"
    assert result["avg_normal"] > 0, "Nilai BMI normal tidak valid"

def test_clinical_generate_summary():
    analyzer = ClinicalAnalyzer(real_data)
    summary = analyzer.generate_summary()
    assert isinstance(summary, dict), "Output harus berupa dictionary"
    # Memastikan semua key laporan klinis lengkap
    assert "hba1c_comparison" in summary
    assert "glucose_comparison" in summary
    assert "bmi_comparison" in summary


# =====================================================================
# --- C. VALIDASI METHOD DI RISK FACTOR ANALYZER ---
# =====================================================================

def test_analyze_hypertension_risk():
    analyzer = RiskFactorAnalyzer(real_data)
    result = analyzer.analyze_hypertension_risk()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    assert "diabetes_rate_with_hypertension" in result
    assert "diabetes_rate_without_hypertension" in result
    assert 0 <= result["diabetes_rate_with_hypertension"] <= 100
    assert 0 <= result["diabetes_rate_without_hypertension"] <= 100

def test_analyze_smoking_impact():
    analyzer = RiskFactorAnalyzer(real_data)
    result = analyzer.analyze_smoking_impact()
    assert isinstance(result, dict), "Output harus berupa dictionary"
    
    values = list(result.values())
    for i in range(len(values) - 1):
        assert values[i] >= values[i+1], "Data riwayat merokok tidak terurut secara descending!"

def test_risk_generate_summary():
    analyzer = RiskFactorAnalyzer(real_data)
    summary = analyzer.generate_summary()
    assert isinstance(summary, dict), "Output harus berupa dictionary"
    assert "hypertension_impact" in summary
    assert "smoking_impact" in summary


# =====================================================================
# --- 3. RUNNER UNTUK MENJALANKAN SEMUA METHOD VALIDASI TEST ---
# =====================================================================
if __name__ == "__main__":
    print("==========================================================")
    print(" Running Full Validation Unit Test for Every Analyzer Method ")
    print("==========================================================\n")
    
    try:
        test_get_total_patients()
        test_get_diabetic_count()
        test_get_diabetes_percentage()
        test_diabetes_by_gender()
        test_diabetes_by_age_group()
        test_diabetes_generate_summary()
        print("[OK] group_diabetes_analyzer: Semua method tervalidasi dengan baik.")
        
        test_analyze_hba1c()
        test_analyze_blood_glucose()
        test_analyze_bmi()
        test_clinical_generate_summary()
        print("[OK] group_clinical_analyzer: Semua method tervalidasi dengan baik.")
        
        test_analyze_hypertension_risk()
        test_analyze_smoking_impact()
        test_risk_generate_summary()
        print("[OK] group_risk_factor_analyzer: Semua method tervalidasi dengan baik.")
        
        print("\n🎉 SUKSES! Total 13 method di dalam seluruh Analyzers lolos validasi logika!")
        
    except AssertionError as error:
        print(f"\n❌ VALIDASI GAGAL! Terjadi kesalahan pada logika program: {error}")