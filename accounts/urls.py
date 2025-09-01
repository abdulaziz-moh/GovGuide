from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/',views.signup_veiw, name = 'signup'),
    path('login/',views.login_view, name = 'login'),
    path('logout/',views.logout_view, name = 'logout'),
    
    # change password needs 2 templates
    path('changepassword/',auth_views.PasswordChangeView.as_view(
        template_name = 'accounts/registration/changepassword_form.html',
        success_url = '/accounts/changepassword/done/',
    ), name = "changepassword"),
    path('changepassword/done/',auth_views.PasswordChangeDoneView.as_view(
        template_name = 'accounts/registration/changepassword_done.html',
    ), name = "changepassworddone"),
    
    # reset password 4html and 2txt
    path('resetpassword/',auth_views.PasswordResetView.as_view(
        template_name = 'accounts/registration/resetpassword_form.html',
        email_template_name = 'accounts/registration/resetpassword_email.txt',
        subject_template_name = 'accounts/registration/resetpassword_subject.txt',
        success_url = "/accounts/resetpassword/done/",
    ), name = "resetpassword"),
    path('resetpassword/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'accounts/registration/resetpassword_done.html',
    ), name = "resetpassworddone"),
    
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
        template_name = 'accounts/registration/resetpassword_confirm.html',
        success_url = '/accounts/reset/done/',
    ), name = "resetpasswordconfirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
        template_name = 'accounts/registration/resetpassword_complete.html',
    ), name = "resetpasswordcomplete"),
]
