from django.contrib import admin
from .models import Customer, Order

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

    def delete_model(self, request, obj):
        # Custom logic before deleting a customer
        # For example, check if the customer has orders
        if obj.orders.exists():
            # Prevent deletion if there are associated orders
            self.message_user(request, "Cannot delete customer with existing orders.", level='error')
            return
        super().delete_model(request, obj)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)


from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Register Profile model in admin (if you have one)
admin.site.register(Profile)