# from tempfile import template
from django.contrib.messages.views import SuccessMessageMixin
from django.core.checks import messages
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
# from django.template import context
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import RedirectView
from .forms import ProfileForm, Signupform, TweetForm, Loginform, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Tweet
from django.contrib import messages
from datetime import date, timedelta
from django.views import View
from django.db.models import Q


# Create your views here.

class Signuppage(SuccessMessageMixin, CreateView):
    model = User
    form_class = Signupform
    template_name = "signup.html"
    success_message = "Your Account Created Successfully!!!"
    success_url = '/'
    
# class Loginpage(TemplateView):
#     template_name = 'login.html'
  
#     def get_context_data(self,*args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         login_form = Loginform()
#         context = {'form': login_form} 
#         return context
    
#     def post(self, request):
#         login_form = AuthenticationForm(request= request, data = request.POST)
#         if login_form.is_valid():
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']
#             print(username)
#             user_obj = list(User.objects.filter(username = username).values('username', 'password'))
#             getted_user = user_obj[0]['username']
#             getted_password = user_obj[0]['password']
#             print(getted_password)
#             # print(user_obj[0]['username'])
#             if(user_obj):
#                 print("hello")
                
#                 if(password != user_obj.password):
#                     messages.error("Invalid password")
                    
#         return HttpResponseRedirect('/')

class Homepage(TemplateView):
    template_name = 'home.html'
    # def get(self,request):
    #     # context = super().get_context_data(**kwargs)
    #     tweet_form = TweetForm()
    #     tweet_saw = Tweet.objects.filter(post_date__gte=date.today()-timedelta(days=360)).order_by('-post_date')
    #     userobj = User.objects.all()
    #     profile,is_created = Profile.objects.get_or_create(user_id = request.user.id)
    #     context = {'form': tweet_form, 'tw':tweet_saw, 'us':userobj} 
    #     return render(request, 'home.html', context)
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        tweet_form = TweetForm()
        tweet_saw = Tweet.objects.filter(post_date__gte=date.today()-timedelta(days=360)).order_by('-post_date')
        userobj = User.objects.all()
        context = {'form': tweet_form, 'tw':tweet_saw, 'us':userobj} 
        return context
    
    def post(self,request):
        current_user = request.user
        tweet_form = TweetForm(request.POST, request.FILES)
        if tweet_form.is_valid():
            post_text = tweet_form.cleaned_data['post_text']
            post_image = tweet_form.cleaned_data['post_image']
            print(post_text)
            if post_image == None and post_text == '':
                messages.warning(request, "Your Post Not Shared!!!")
                return HttpResponseRedirect('/home/')
            share_post = Tweet(user_id = current_user.id, post_text=post_text,post_image=post_image)
            share_post.save()
            messages.success(request, "Your Post Shared Successfully!!!")
        else:
            messages.warning(request, "Your Post Not Shared!!!")
        return HttpResponseRedirect('/home/')
    
class Tweetpage(Homepage):
    template_name  = 'tweet.html'
    
class Likes(View):
    def get(self, request, id):
        tweet = Tweet.objects.get(id= id)
        is_liked = False
        for like in tweet.likes.all():
            if like == request.user:
                is_liked = True
                break
            
        if not is_liked:
            tweet.likes.add(request.user)
        if is_liked:
            tweet.likes.remove(request.user)
        total = len(list(tweet.likes.all()))
        return JsonResponse({'total':total})
        
            
            
class DelTweet(RedirectView):
    permanent = True
    url = ''
    
    def get_redirect_url(self,*args, **kwargs):
        del_id = kwargs['id']
        t = Tweet.objects.get(pk=del_id)
        tu = t.user.username
        t.delete()
        url = reverse_lazy('profile', kwargs={'username':tu})
        return url 
    
class Profilepage(View):
    def get(self, request, username):
        us = User.objects.get(username = username)
        tw = Tweet.objects.filter(user = us.id).order_by('-post_date')
        pr = Profile.objects.get_or_create(user_id = us.id) #
        follower = Profile.objects.filter(following=us.id)
        context = {'us':us, 'tw':tw, 'follower':follower}
        return render(request, 'profile.html', context)
    
class EditProfilepage(View):
    def get(self, request, username):
        us = User.objects.get(username = username)
        profile = Profile.objects.get(user_id = us.id) #
        profile_form = ProfileForm(instance=us.profile)
        context = {'us':us, 'form':profile_form}
        return render(request, 'editprofile.html', context)
    
    def post(self, request, username):
        us = User.objects.get(username = username)
        # profile = Profile.objects.get(user_id = us.id)
        profile_form = ProfileForm(request.POST,request.FILES, instance=us.profile)
        if profile_form.is_valid(): 
            dob = profile_form.cleaned_data['dob']
            bio = profile_form.cleaned_data['bio']
            location = profile_form.cleaned_data['location']
            profile_image = profile_form.cleaned_data['profile_image']
            profile = Profile.objects.get(user_id = us.id)
            profile.dob =dob
            profile.bio =bio
            profile.location=location
            profile.profile_image=profile_image
            profile.save()
            messages.success(request, 'Your Details Updated!!!')
        else:
            messages.warning(request, "Your Details Not Updated!!!")
        return render(request, 'editprofile.html', context={'us':us, 'form':profile_form})
    
class Poeplepage(TemplateView):
    template_name = 'people.html'
    
    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        user_l =  User.objects.all().order_by('-id')
        # profile = Profile.objects.all()
        context = {'users':user_l}
        return context
    
class Follows(View):
    def get(self, request, id):
        f_id = User.objects.get(id = id)
        profile,is_created = Profile.objects.get_or_create(user_id = request.user.id)
        # print(profile.following.all())
        if f_id in profile.following.all():
            profile.following.remove(f_id)
        else:
            profile.following.add(f_id)   
        total = len(list(f_id.following.all()))
        return JsonResponse({"total":total})
        
class Followers(TemplateView):
    template_name = 'followers.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        s_username = kwargs['username']
        user = User.objects.get(username = s_username)
        followers = Profile.objects.filter(following = user.id)
        # follower_user = User.objects.all()
        context = {'followers':followers, 's_username':s_username}
        return context
    
    
class Followings(TemplateView):
    template_name = 'followings.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        s_username = kwargs['username']
        user = User.objects.get(username = s_username)
        followings = Profile.objects.get(user_id = user.id)
        context = {'followings':followings, 's_username':s_username}
        return context
    
class ConfirmDel(TemplateView):
    template_name = 'confirm_delete.html'
    
class DelAccount(View):
    def get(self, request, *args, **kwargs):
        del_username = kwargs['username']
        del_user = User.objects.get(username = del_username)
        del_user.delete()
        context = {'msg':"Your Account Deleted Successfully!!!"}
        return render(request, 'delete.html', context)
    
class Searchppl(View):
    def get(self, request):
        query = request.GET['query']
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query)|Q(last_name__icontains=query))
        context = {'users':users}
        return render(request, 'search_ppl.html', context)