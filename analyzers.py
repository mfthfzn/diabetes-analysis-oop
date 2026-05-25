class BaseAnalyzer:
  """Superclass yang menyediakan fungsionalitas dasar analisis"""
  def __init__(self, records: list):
    self.records = records

  def get_total_patients(self) -> int:
    return len(self.records)


class OperationalAnalyzer(BaseAnalyzer):
  """Subclass khusus untuk analisis manajemen operasional rumah sakit"""
  
  def avg_stay_by_condition(self) -> dict:
    condition_data = {}
    for r in self.records:
      cond = r.medical_condition
      stay = r.get_length_of_stay()
      if cond not in condition_data:
        condition_data[cond] = {'total_days': 0, 'count': 0}
      condition_data[cond]['total_days'] += stay
      condition_data[cond]['count'] += 1
      
    averages = {}
    for cond, data in condition_data.items():
      averages[cond] = round(data['total_days'] / data['count'], 2)
    return dict(sorted(averages.items(), key=lambda item: item[1], reverse=True))

  def admission_type_distribution(self) -> dict:
    distribution = {}
    for r in self.records:
      adm_type = r.admission_type
      distribution[adm_type] = distribution.get(adm_type, 0) + 1
    return distribution


class FinancialAnalyzer(BaseAnalyzer):
  """Subclass khusus untuk analisis ekonomi kesehatan dan asuransi"""
  
  def avg_billing_by_insurance(self) -> dict:
    insurance_data = {}
    for r in self.records:
      provider = r.insurance_provider
      billing = r.billing_amount
      if provider not in insurance_data:
        insurance_data[provider] = {'total_billing': 0, 'count': 0}
      insurance_data[provider]['total_billing'] += billing
      insurance_data[provider]['count'] += 1
      
    averages = {}
    for provider, data in insurance_data.items():
      averages[provider] = round(data['total_billing'] / data['count'], 2)
    return dict(sorted(averages.items(), key=lambda item: item[1], reverse=True))
  
class DemographicAnalyzer(BaseAnalyzer):
  """Subclass khusus untuk menganalisis karakteristik demografi pasien"""
  
  def age_group_distribution(self) -> dict:
    """Mengelompokkan pasien berdasarkan kategori usia"""
    groups = {"Anak-anak (<18)": 0, "Dewasa (18-59)": 0, "Lansia (>=60)": 0}
    
    for r in self.records:
      if r.age < 18:
        groups["Anak-anak (<18)"] += 1
      elif 18 <= r.age < 60:
        groups["Dewasa (18-59)"] += 1
      else:
        groups["Lansia (>=60)"] += 1
        
    return groups

  def medical_condition_by_gender(self) -> dict:
    """Memetakan tren jenis penyakit berdasarkan jenis kelamin pasien"""
    matrix = {}
    
    for r in self.records:
      gender = r.gender
      cond = r.medical_condition
      
      if gender not in matrix:
        matrix[gender] = {}
      
      matrix[gender][cond] = matrix[gender].get(cond, 0) + 1
      
    return matrix