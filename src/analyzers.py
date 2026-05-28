from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
  """
  Abstract Base Class yang menyediakan fungsionalitas dasar untuk analisis.
  Tidak bisa diinstansiasi secara langsung (harus melalui subclass).
  """
  def __init__(self, records: list):
    self.records = records

  def get_total_patients(self) -> int:
    """Mengembalikan jumlah total seluruh pasien di dalam dataset"""
    return len(self.records)

  def get_diabetic_count(self) -> int:
    """Mengembalikan jumlah total pasien yang positif diabetes"""
    count = 0
    for r in self.records:
      if r.has_diabetes():
        count += 1
    return count

  def get_diabetes_percentage(self) -> float:
    """Menghitung persentase keseluruhan pasien diabetes"""
    total = self.get_total_patients()
    if total == 0:
      return 0.0
    
    diabetic = self.get_diabetic_count()
    return round((diabetic / total) * 100, 2)

  @abstractmethod
  def generate_summary(self) -> dict:
    """
    Method abstrak: WAJIB diimplementasikan oleh semua subclass (anaknya).
    Tujuannya agar setiap analyzer memiliki format laporan (summary) yang seragam.
    """
    pass
  
class DiabetesAnalyzer(BaseAnalyzer):
  """
  Subclass khusus untuk menganalisis karakteristik pasien 
  yang terdiagnosis positif diabetes.
  """
  
  def diabetes_by_gender(self) -> dict:
    """
    Menghitung jumlah pasien yang POSITIF diabetes berdasarkan Jenis Kelamin.
    Hasilnya berupa dictionary: {'Female': jumlah, 'Male': jumlah}
    """
    gender_counts = {}
    
    for r in self.records:
      # Kita hanya menghitung pasien yang positif diabetes saja
      if r.has_diabetes():
        gen = r.gender
        gender_counts[gen] = gender_counts.get(gen, 0) + 1
        
    return gender_counts

  def diabetes_by_age_group(self) -> dict:
    """
    Menghitung jumlah pasien yang POSITIF diabetes berdasarkan Kelompok Usia.
    Kategori: Anak-anak (<18), Dewasa (18-59), Lansia (>=60).
    """
    age_groups = {
      "Anak-anak (<18)": 0, 
      "Dewasa (18-59)": 0, 
      "Lansia (>=60)": 0
    }
    
    for r in self.records:
      # Pastikan hanya memproses pasien yang memiliki diabetes
      if r.has_diabetes():
        if r.age < 18:
          age_groups["Anak-anak (<18)"] += 1
        elif 18 <= r.age < 60:
          age_groups["Dewasa (18-59)"] += 1
        else:
          age_groups["Lansia (>=60)"] += 1
          
    return age_groups

  # Wajib mengimplementasikan method dari class induk (BaseAnalyzer)
  def generate_summary(self) -> dict:
    """
    Menyusun dan mengembalikan semua hasil analisis demografi diabetes
    ke dalam satu format dictionary (laporan ringkas).
    """
    return {
      "total_diabetes_patients": self.get_diabetic_count(),
      "demographic_by_gender": self.diabetes_by_gender(),
      "demographic_by_age": self.diabetes_by_age_group()
    }
  
class ClinicalAnalyzer(BaseAnalyzer):
  """
  Subclass untuk menganalisis indikator klinis utama (HbA1c, Glukosa Darah, dan BMI).
  Membandingkan rata-rata pasien diabetes vs non-diabetes.
  """
  
  def analyze_hba1c(self) -> dict:
    """Membandingkan rata-rata HbA1c pasien diabetes vs non-diabetes"""
    diabetic_hba1c = [r.hba1c_level for r in self.records if r.has_diabetes()]
    normal_hba1c = [r.hba1c_level for r in self.records if not r.has_diabetes()]
    
    return {
      "avg_diabetes": round(sum(diabetic_hba1c) / len(diabetic_hba1c), 2) if diabetic_hba1c else 0,
      "avg_normal": round(sum(normal_hba1c) / len(normal_hba1c), 2) if normal_hba1c else 0
    }

  def analyze_blood_glucose(self) -> dict:
    """Membandingkan rata-rata Glukosa Darah pasien diabetes vs non-diabetes"""
    diabetic_glucose = [r.blood_glucose_level for r in self.records if r.has_diabetes()]
    normal_glucose = [r.blood_glucose_level for r in self.records if not r.has_diabetes()]
    
    return {
      "avg_diabetes": round(sum(diabetic_glucose) / len(diabetic_glucose), 2) if diabetic_glucose else 0,
      "avg_normal": round(sum(normal_glucose) / len(normal_glucose), 2) if normal_glucose else 0
    }

  def analyze_bmi(self) -> dict:
    """Membandingkan rata-rata BMI pasien diabetes vs non-diabetes"""
    diabetic_bmi = [r.bmi for r in self.records if r.has_diabetes()]
    normal_bmi = [r.bmi for r in self.records if not r.has_diabetes()]
    
    return {
      "avg_diabetes": round(sum(diabetic_bmi) / len(diabetic_bmi), 2) if diabetic_bmi else 0,
      "avg_normal": round(sum(normal_bmi) / len(normal_bmi), 2) if normal_bmi else 0
    }

  def generate_summary(self) -> dict:
    """Implementasi method abstrak dari BaseAnalyzer"""
    return {
      "hba1c_comparison": self.analyze_hba1c(),
      "glucose_comparison": self.analyze_blood_glucose(),
      "bmi_comparison": self.analyze_bmi()
    }


class RiskFactorAnalyzer(BaseAnalyzer):
  """
  Subclass untuk menganalisis faktor risiko dan komorbiditas 
  seperti Hipertensi dan Riwayat Merokok terhadap rasio Diabetes.
  """
  
  def analyze_hypertension_risk(self) -> dict:
    """
    Menghitung persentase risiko diabetes pada kelompok pasien hipertensi 
    dibandingkan dengan kelompok tanpa hipertensi.
    """
    ht_total = 0
    ht_diabetes = 0
    no_ht_total = 0
    no_ht_diabetes = 0
    
    for r in self.records:
      if r.has_hypertension():
        ht_total += 1
        if r.has_diabetes():
          ht_diabetes += 1
      else:
        no_ht_total += 1
        if r.has_diabetes():
          no_ht_diabetes += 1
          
    risk_with_ht = round((ht_diabetes / ht_total) * 100, 2) if ht_total else 0
    risk_without_ht = round((no_ht_diabetes / no_ht_total) * 100, 2) if no_ht_total else 0
    
    return {
      "diabetes_rate_with_hypertension": risk_with_ht,
      "diabetes_rate_without_hypertension": risk_without_ht
    }

  def analyze_smoking_impact(self) -> dict:
    """
    Menghitung tingkat prevalensi (persentase) diabetes 
    berdasarkan setiap kategori riwayat merokok.
    """
    smoke_groups = {}
    
    for r in self.records:
      status = r.smoking_history
      if status not in smoke_groups:
        smoke_groups[status] = {"total": 0, "diabetes_count": 0}
      
      smoke_groups[status]["total"] += 1
      if r.has_diabetes():
        smoke_groups[status]["diabetes_count"] += 1
        
    risks = {}
    for status, counts in smoke_groups.items():
      # Menghindari pembagian dengan nol
      if counts["total"] > 0:
        risks[status] = round((counts["diabetes_count"] / counts["total"]) * 100, 2)
      else:
        risks[status] = 0.0
        
    # Mengurutkan dari risiko tertinggi ke terendah
    return dict(sorted(risks.items(), key=lambda item: item[1], reverse=True))

  def generate_summary(self) -> dict:
    """Implementasi method abstrak dari BaseAnalyzer"""
    return {
      "hypertension_impact": self.analyze_hypertension_risk(),
      "smoking_impact": self.analyze_smoking_impact()
    }