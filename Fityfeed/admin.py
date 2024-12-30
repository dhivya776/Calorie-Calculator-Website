from django.contrib import admin
from .models import User, Customer
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
class CustomUserAdmin(UserAdmin):
    pass

# Register your models here.
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Customer.objects.create(user=user, name=user.username, email=user.username+'@example.com')
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    
admin.site.register(User, CustomUserAdmin)


from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')


