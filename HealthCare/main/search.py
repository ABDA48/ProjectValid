from main.models import DiseasesModel,DoctorModel,HistoryModel,MedicineModel,PatientsModel,Profile
class DiseaseSearch:
    def __init__(self,name):
        self.name=name
        self.obj=DiseasesModel.objects.filter(name=name).values()[0]
    def causes(self):
        return self.obj['causes']
    def definition(self):
        return self.obj['definition']
    def treatments(self):
        return self.obj['treatments']
    def preventions(self):
        return self.obj['preventions']
    def medicine(self):
        id=self.obj['id']
        medicine=MedicineModel.objects.get(id=id)
        return medicine.name+": "+medicine.definition
    def medicinename(self):
        id=self.obj['id']
        medicine=MedicineModel.objects.get(id=id)
        return medicine.name
    def medicineprecription(self):
        id=self.obj['id']
        medicine=MedicineModel.objects.get(id=id)
        return medicine.prescription
    def medicineeffects(self):
        id=self.obj['id']
        medicine=MedicineModel.objects.get(id=id)
        return medicine.effects



