from django.contrib import admin
from .form import MedicineForm,DiseasesForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PatientsModel,MedicineModel,DiseasesModel,HistoryModel,Profile,DoctorModel

admin.site.register(PatientsModel)
admin.site.register(DoctorModel)

admin.site.register(Profile)
admin.site.register(HistoryModel)

class DiseaseAdmin(admin.ModelAdmin):
    form=DiseasesForm
admin.site.register(DiseasesModel,DiseaseAdmin)


class MedicineAdmin(admin.ModelAdmin):
    form=MedicineForm
admin.site.register(MedicineModel,MedicineAdmin)

#User.objects.filter(is_superuser=True).delete()
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Register your models here.
