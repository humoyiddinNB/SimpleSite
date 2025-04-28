from django.urls import path

from authapp.views import RegisterView, LoginView, ProfileView, LogOut, DeleteView, ChangePassword, AuthOne, AuthTwo

urlpatterns = [
    path('regis', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogOut.as_view()),
    path('profile', ProfileView.as_view()),
    path('update', ProfileView.as_view()),
    path('delete', DeleteView.as_view()),
    path('change-password', ChangePassword.as_view()),
    path('auth-one', AuthOne.as_view()),
    path('auth-two', AuthTwo.as_view())

]