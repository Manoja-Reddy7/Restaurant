from django.contrib import admin

from .models import Payment,Order,OrderedFood

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','transaction_id','payment_method', 'amount', 'status', 'created_at')

class OrderedFoodInline(admin.TabularInline):
     model = OrderedFood 
     readonly_fields = ('order','payment','user','fooditem','quantity','price','amount')
     extra = 0 # To remove extra blanks.
     
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'name','phone','email','total','payment_method','status','is_ordered','order_placed_to')
    inlines = [OrderedFoodInline]

# Register your models here.
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)


 