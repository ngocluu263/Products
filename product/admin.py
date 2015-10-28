from django.contrib import admin
from models import Product, User, Like, Comments
# Register your models here.

# admin.site.register(User)
admin.site.register(Like)
admin.site.register(Product)
admin.site.register(Comments)
