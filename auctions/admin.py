from django.contrib import admin
from .models import User, Bid, Category, Auc_listing, Auc_comment
# Register your models here.

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Auc_listing)
admin.site.register(Auc_comment)
