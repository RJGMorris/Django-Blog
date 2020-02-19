from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('following', 'followers')


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     filter_horizontal = ('ope',)
#
# class CustomUserAdmin(UserAdmin):
#     #filter_horizontal = ('user_permissions', 'groups', 'ope')
#     save_on_top = True
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
#     inlines = [UserProfileInline]
#
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(opetest, opetestAdmin)

admin.site.register(Profile, ProfileAdmin)
