from .views import *
from django.contrib.auth import views as auth_views


# Form definition
class AdminIndexView(RoleRequiredView):
    user_role = 2
    form = None
    template_path = "boec_core/admin/index.html"

    def update_post_context(self, request, *args, **kwargs):
        return super().update_post_context(request, *args, **kwargs)

    def update_get_context(self, request, *args, **kwargs):
        return super().update_get_context(request, *args, **kwargs)