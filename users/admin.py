from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
        )
    list_filter = (
        'groups', 'is_staff', 'is_active'
        )
    search_fields = ('username', 'email')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Try to register the custom User admin, but skip if User is already registered
# Do not register here to avoid conflicts with django.contrib.auth's registration.
# If you need a custom admin for the User model, handle registration in a
# dedicated AppConfig.ready() after auth app has been loaded, or adjust
# INSTALLED_APPS ordering.
