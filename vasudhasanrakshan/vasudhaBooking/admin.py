from django.contrib import admin
from .models import *
# Register your models here.



from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# class UserOtherInfoInline(admin.StackedInline):
#     model = UserOtherInfo
#     can_delete = False
#     verbose_name_plural = 'UserOtherInfos'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (UserOtherInfoInline,)

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)



class RateOfProductInline(admin.TabularInline):
    model = RateOfProduct
    extra = 1
    

class RateListAdmin(admin.ModelAdmin):
    inlines = (RateOfProductInline,)


admin.site.register(RateList,RateListAdmin)




class ProductListInline(admin.TabularInline):
    model = ProductListDetail
    extra = 0
    

class SellDemandAdmin(admin.ModelAdmin):
    inlines = (ProductListInline,)

admin.site.register(SellDemand,SellDemandAdmin)



admin.site.register([HomePageImage,City])
