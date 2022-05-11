from django.urls import path
from django.contrib.auth.decorators import login_required
from root.forms import Loginform, PasswordChangeform
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.Loginpage.as_view(), name='login'),
    path('',auth_view.LoginView.as_view(template_name='login.html', form_class=Loginform), name='login'),
    path('signup/', views.Signuppage.as_view(), name='signup'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name='change_password.html', form_class=PasswordChangeform, success_url = '/changepassworddone/'), name="change-password"),
    path('changepassworddone/', auth_view.PasswordChangeView.as_view(template_name='changepassworddone.html'), name="changepassworddone"),
    
    path('home/',login_required(views.Homepage.as_view(), login_url='login'), name='home'),
    path('tweet/', login_required(views.Tweetpage.as_view(), login_url='login'), name='tweet'),
    path('tweet/like/<int:id>/', login_required(views.Likes.as_view(), login_url='login'), name='like'),
    path('deltweet/<int:id>/', login_required(views.DelTweet.as_view(), login_url='login'), name='deltweet'),
    path('profile/<slug:username>/', login_required(views.Profilepage.as_view(), login_url='login'), name='profile'),
    path('editprofile/<slug:username>/', login_required(views.EditProfilepage.as_view(), login_url='login'), name='editprofile'),
    path('list-of-people/', login_required(views.Poeplepage.as_view(), login_url='login'), name='people'),
    path('search/', login_required(views.Searchppl.as_view(), login_url='login'), name='search'),
    path('list-of-people/follow/<int:id>/', login_required(views.Follows.as_view(), login_url='login'), name='follow'),
    path('list-of-people/followers/<slug:username>/', login_required(views.Followers.as_view(), login_url='login'), name='followers'),
    path('list-of-people/followings/<slug:username>/', login_required(views.Followings.as_view(), login_url='login'), name='followings'),
    path('confirm-del/<slug:username>/', login_required(views.ConfirmDel.as_view(), login_url='login'), name='confirm-del'),
    path('delete_account/<slug:username>/', login_required(views.DelAccount.as_view(), login_url='login'), name='del-account')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
