from abc import ABC, abstractmethod

# OCP, LSP, ISP
class BaseAnalyzer(ABC):
  def __init__(self, records: list):
    self.records = records

  def get_total_patients(self) -> int:
    """Mengembalikan jumlah total seluruh rekaman pasien di dalam dataset."""
    return len(self.records)

  def get_diabetic_count(self) -> int:
    """Menghitung dan mengembalikan jumlah total pasien yang positif diabetes."""
    count = 0
    for r in self.records:
      if r.has_diabetes():
        count += 1
    return count

  def get_diabetes_percentage(self) -> float:
    """Menghitung persentase pasien diabetes dari total keseluruhan pasien."""
    total = self.get_total_patients()
    if total == 0:
      return 0.0
    
    diabetic = self.get_diabetic_count()
    return round((diabetic / total) * 100, 2)

  @abstractmethod
  def generate_summary(self) -> dict:
    """Method abstrak wajib untuk menghasilkan ringkasan laporan analisis."""
    pass


class DiabetesAnalyzer(BaseAnalyzer):
  def diabetes_by_gender(self) -> dict:
    """Menghitung jumlah kasus positif diabetes berdasarkan jenis kelamin pasien."""
    gender_counts = {}
    for r in self.records:
      if r.has_diabetes():
        gen = r.gender
        if gen in gender_counts:
          gender_counts[gen] += 1
        else:
          gender_counts[gen] = 1
    return gender_counts

  def diabetes_by_age_group(self) -> dict:
    """Mengelompokkan dan menghitung jumlah kasus diabetes berdasarkan kategori usia."""
    age_groups = {
      "Anak-anak (<18)": 0, 
      "Dewasa (18-59)": 0, 
      "Lansia (>=60)": 0
    }
    for r in self.records:
      if r.has_diabetes():
        if r.age < 18:
          age_groups["Anak-anak (<18)"] += 1
        elif 18 <= r.age < 60:
          age_groups["Dewasa (18-59)"] += 1
        else:
          age_groups["Lansia (>=60)"] += 1
    return age_groups

  def generate_summary(self) -> dict:
    """Menyusun laporan ringkas demografi pasien yang terkena diabetes."""
    return {
      "total_diabetes_patients": self.get_diabetic_count(),
      "demographic_by_gender": self.diabetes_by_gender(),
      "demographic_by_age": self.diabetes_by_age_group()
    }


class ClinicalAnalyzer(BaseAnalyzer):
  def analyze_hba1c(self) -> dict:
    """Membandingkan rata-rata tingkat HbA1c pasien diabetes dan non-diabetes."""
    diabetic_hba1c = []
    normal_hba1c = []
    
    for r in self.records:
      if r.has_diabetes():
        diabetic_hba1c.append(r.hba1c_level)
      else:
        normal_hba1c.append(r.hba1c_level)
        
    avg_diabetes = 0.0
    if len(diabetic_hba1c) > 0:
      avg_diabetes = round(sum(diabetic_hba1c) / len(diabetic_hba1c), 2)
      
    avg_normal = 0.0
    if len(normal_hba1c) > 0:
      avg_normal = round(sum(normal_hba1c) / len(normal_hba1c), 2)
      
    return {
      "avg_diabetes": avg_diabetes,
      "avg_normal": avg_normal
    }

  def analyze_blood_glucose(self) -> dict:
    """Membandingkan rata-rata kadar glukosa darah pasien diabetes dan non-diabetes."""
    diabetic_glucose = []
    normal_glucose = []
    
    for r in self.records:
      if r.has_diabetes():
        diabetic_glucose.append(r.blood_glucose_level)
      else:
        normal_glucose.append(r.blood_glucose_level)
        
    avg_diabetes = 0.0
    if len(diabetic_glucose) > 0:
      avg_diabetes = round(sum(diabetic_glucose) / len(diabetic_glucose), 2)
      
    avg_normal = 0.0
    if len(normal_glucose) > 0:
      avg_normal = round(sum(normal_glucose) / len(normal_glucose), 2)
      
    return {
      "avg_diabetes": avg_diabetes,
      "avg_normal": avg_normal
    }

  def analyze_bmi(self) -> dict:
    """Membandingkan rata-rata indeks massa tubuh (BMI) pasien diabetes dan non-diabetes."""
    diabetic_bmi = []
    normal_bmi = []
    
    for r in self.records:
      if r.has_diabetes():
        diabetic_bmi.append(r.bmi)
      else:
        normal_bmi.append(r.bmi)
        
    avg_diabetes = 0.0
    if len(diabetic_bmi) > 0:
      avg_diabetes = round(sum(diabetic_bmi) / len(diabetic_bmi), 2)
      
    avg_normal = 0.0
    if len(normal_bmi) > 0:
      avg_normal = round(sum(normal_bmi) / len(normal_bmi), 2)
      
    return {
      "avg_diabetes": avg_diabetes,
      "avg_normal": avg_normal
    }

  def generate_summary(self) -> dict:
    """Menyusun laporan perbandingan indikator klinis utama medis."""
    return {
      "hba1c_comparison": self.analyze_hba1c(),
      "glucose_comparison": self.analyze_blood_glucose(),
      "bmi_comparison": self.analyze_bmi()
    }


class RiskFactorAnalyzer(BaseAnalyzer):
  def analyze_hypertension_risk(self) -> dict:
    """Menghitung persentase tingkat diabetes pada kelompok pasien dengan dan tanpa hipertensi."""
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
          
    risk_with_ht = 0.0
    if ht_total > 0:
      risk_with_ht = round((ht_diabetes / ht_total) * 100, 2)
      
    risk_without_ht = 0.0
    if no_ht_total > 0:
      risk_without_ht = round((no_ht_diabetes / no_ht_total) * 100, 2)
      
    return {
      "diabetes_rate_with_hypertension": risk_with_ht,
      "diabetes_rate_without_hypertension": risk_without_ht
    }

  def analyze_smoking_impact(self) -> dict:
    """Menghitung dan mengurutkan rasio diabetes berdasarkan kategori riwayat merokok."""
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
      if counts["total"] > 0:
        risks[status] = round((counts["diabetes_count"] / counts["total"]) * 100, 2)
      else:
        risks[status] = 0.0
        
    return dict(sorted(risks.items(), key=lambda item: item[1], reverse=True))

  def generate_summary(self) -> dict:
    """Menyusun laporan ringkas dampak faktor risiko eksternal terhadap diabetes."""
    return {
      "hypertension_impact": self.analyze_hypertension_risk(),
      "smoking_impact": self.analyze_smoking_impact()
    }