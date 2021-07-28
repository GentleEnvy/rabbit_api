from django.contrib import admin

from api.models import *

admin.site.register(TypeGroup)

admin.site.register(MotherCage)
admin.site.register(FatteningCage)

admin.site.register(Bunny)
admin.site.register(DeadRabbit)
admin.site.register(FatteningRabbit)
admin.site.register(MotherRabbit)
admin.site.register(FatherRabbit)
