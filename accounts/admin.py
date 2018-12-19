from dateutil.relativedelta import relativedelta
from django.utils import timezone

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import Profile, User, UserSession

from django.contrib.auth.models import Permission

admin.site.register(Permission)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website_url']
    list_display_links = ['user']


class UserDateJoinedFilter(admin.SimpleListFilter):
    title = '유저 가입일'
    parameter_name = 'date_joined_match'

    def lookups(self, request, model_admin):
        candidate = []
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for i in range(6):
            value = '{}-{}'.format(start_date.year, start_date.month)
            label = '{}년 {}월 가입자'.format(start_date.year, start_date.month)
            candidate.append([value, label])
            start_date -= relativedelta(months=1)
        return candidate

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        try:
            year, month = map(int, value.split('-'))
            queryset = queryset.filter(date_joined__year=year, date_joined__month=month)
        except ValueError:
            return queryset.none()

        return queryset



@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups', 'sex', UserDateJoinedFilter]
    actions = ['마케팅_이메일보내기']

    def 마케팅_이메일보내기(self, request, queryset):
        for user in queryset:
            pass
        self.message_user(request, 'Success!')

admin.site.register(UserSession)
