from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from account.forms import CustomPasswordForm,CustomSetPasswordForm,CustomPasswordChangeForm
from django.urls import reverse_lazy


app_name = 'account'

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page="account:login"), name="logout"),
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name="account/pass_reset/password_reset_form.html",
        form_class = CustomPasswordForm,
        email_template_name="account/pass_reset/password_reset_email.html",
        subject_template_name="account/pass_reset/password_reset_subject.html",
        success_url=reverse_lazy('account:password_reset_done')  # Redirect after successful password reset.
        )
        ,name="password_reset"),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="account/pass_reset/pass_reset/password_reset_done.html"

         ),name='password_reset_done'),
 
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
          template_name="account/pass_reset/password_reset_confirm.html",
          form_class=CustomSetPasswordForm,
          success_url=reverse_lazy('account:password_reset_complete') # Redirect after successful password reset_complete.
         ),
          name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('settings/',views.settings,name='settings'), 

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name="account/settings/setting.html",
        form_class=CustomPasswordChangeForm,

        success_url=reverse_lazy('account:password_change_done') # Redirect after successful password change.

        ),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(
         template_name="account/settings/password_change_done.html" 

    ),name='password_change_done'),

    path('profile/', views.profile, name='profile'),  # Add your profile view here.
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('profile_update/', views.update_profile, name='update_profile'),


    
   
    
   
]