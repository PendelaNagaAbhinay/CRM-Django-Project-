from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render


class UserLogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Use CharField for simplicity, consider hashed passwords in production

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # This links Customer to User
    # other fields for customer details


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#
#     def __str__(self):
#         return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    # Add any other fields you need

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"


from .models import Profile



def my_customers(request):
    # Fetch all users from the database
    users = User.objects.all()

    # Ensure users exist (debugging check)
    print("Users fetched: ", users)

    # Pass users to the template
    return render(request, 'my_customers.html', {'users': users})



class Product(models.Model):
    order_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Delivered', 'Delivered')])
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Relating the product to the user

    def __str__(self):
        return self.order_name


class HubProduct(models.Model):
    order_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save


from django.http import JsonResponse
from .models import Order


# View to fetch delivered orders for the logged-in user
def view_delivered_orders(request):
    if request.user.is_authenticated:
        # Filter delivered orders for the logged-in user
        delivered_orders = Order.objects.filter(user=request.user, status='Delivered')

        # Prepare the data to send back to the client
        orders_data = []
        for order in delivered_orders:
            orders_data.append({
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'created_at': order.created_at,
            })

        return JsonResponse({'orders': orders_data})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=400)

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()

    def __str__(self):
        return f'Feedback - {self.rating} stars'
