from django.urls import path
from user import login, profiles, view_admin

app_name = 'users'

urlpatterns = [
    path("register/", login.register_view, name="register"),
    path("login/", login.CustomLoginView.as_view(), name="login"),
    path("logout/", login.CustomLogoutView.as_view(), name="logout"),
    path('miperfil/', profiles.profile_view, name='perfil'),
    path('perfil/<slug:profile_slug>/', profiles.user_profile, name='public_profile'),
    path('admin/dashboard/usuarios/', view_admin.user_dashboard, name='user_dashboard'),
    ]
