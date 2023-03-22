from django.contrib import admin
from .models import House

# Register your models here.
# 데코레이터를 통해 admin class가 House model을 컨트롤한다고 알려줌
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    fields = ("name", "address", ("price_per_night","pets_allowed"))
    list_display = [
        "name",
        "price_per_night",
        "address",
        "pets_allowed"
    ]
    list_filter = ["price_per_night", "pets_allowed"]
    search_fields = ["address__startswith", "name"]