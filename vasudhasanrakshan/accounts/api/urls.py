from django.urls import path

from .views import *

urlpatterns = [
	path('register/',UserCreateAPIView.as_view(),name="register"),
	path('login/',UserLoginAPIView.as_view(),name="login"),
	path('changepassword/',ChangePasswordAPIView.as_view(),name="changePassword"),
	path('password/reset/', PasswordResetView.as_view(),
    name='rest_password_reset'),
    path('rest-auth/google/', GoogleLoginView.as_view(), name='gl_login'), #facebooklogin

    path('rest-auth/facebook/', FacebookLoginView.as_view(), name='fb_login'), #facebooklogin
    path('otp-generate',OtpGenerateAPIView.as_view(),name="OtpGenerateAPIView"),
    path('otp-verify',OtpVarifyAPIView.as_view(),name="OtpVarifyAPIView"),

]
