from django.contrib.auth.views import LogoutView
from django.urls import path
from apps.usuario.views import *

app_name = 'usuario'

urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('listarUsuario/', listarUsuariosView.as_view(), name='listarUsuario'),
    path('crearUsuario/', crearUsuarioView.as_view(), name='crearUsuario'),
    path('modificarUsuario/<int:pk>', updateUsuarioView.as_view(), name='modificarUsuario'),
    path('eliminarUsuario/<int:pk>/', eliminarUsuario.as_view(), name='eliminarUsuario'),
    path('profile/', updateUsuarioProfileView.as_view(), name='profile'),
    path('reset/password/', resetearPasswordView.as_view(), name='resetear_password'),
    path('change/password/<str:token>/', changePasswordView.as_view(), name='change_password')
]