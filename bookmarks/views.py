from django.shortcuts import *
from bookmarks.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from bookmarks.models import *
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.db.models import Q


def Registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username = form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password2'])
            return redirect('/admin/')
        else:
            context= {
                'form': RegistrationForm(),
                'error': form.errors,
                }
            return render(request, 'Registartion.html', context)
    return render(request, 'bookmarks/Registartion.html', {'form': RegistrationForm()})

def login_view(request):
    form = LoginForm()
    if request.method =='POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
# if username and password doesn't match authenticate method will return None
        if user is not None:
            login(request, user)
            return redirect('/bookmarks/home/')
        else:
            context = {
            'message': "Please Enter Valid Credeintials",
            'form': form
            }
            return render(request,'bookmarks/login.html',context)
    return render(request, 'bookmarks/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/bookmarks/login/')

@login_required
def addbookmark(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            bookmark, created = Bookmark.objects.get_or_create(
            title = form.cleaned_data['title'],
            sharebookmark = form.cleaned_data['sharebookmark'],
            link = form.cleaned_data['link'],
            user = request.user)
            bookmark.tag.clear()
            tag_names = form.cleaned_data['tag'].split()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name = tag_name)
                bookmark.tag.add(tag)
                bookmark.save()
        return redirect ('/bookmarks/home')
    form = BookmarkForm()
    return render(request, 'bookmarks/add_bookmark.html', {'form': form})


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['title', 'link', 'tag', 'sharebookmark']
    template_name_suffix = '_update_form'
    success_url= "/bookmarks/home"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def Homepage(request):
    sharedbookmarks = voting.objects.filter(bookmark__sharebookmark = True)
    context = {
    'bookmarks': sharedbookmarks,
    'for_voting': True
    }
    return render(request, 'bookmarks/index.html', context)

@login_required
def userpage(request, username):
    bookmarks = Bookmark.objects.filter(user__username= username)
    return render(request,'bookmarks/user.html', {'bookmarks': bookmarks, 'username':username})

@login_required
def tagpage(request, tagname):
    print(request.user)
    bookmarks = Bookmark.objects.filter(tag__name = tagname)
    return render(request,'bookmarks/tag.html', {'bookmarks': bookmarks, 'tagname':tagname})

@login_required
def votepage(request, pk):
    vote = voting.objects.get(pk = pk)
    user = vote.users_voted.filter(username = request.user.username)
    if not user:
        vote.users_voted.add(request.user)
        vote.votes +=1
        vote.save()
    return redirect('/bookmarks/home')

@login_required
def search(request):
    form = BookmarkSearchForm()
    bookmarks = []
    search_results = False
    if 'query' in request.GET:
        search_results = True
        query = request.GET['query'].split()
        print(query)
        q = Q()
        for keyword in query:
            q = q | Q(title__icontains = keyword)
        form = BookmarkSearchForm({'query': query})
        bookmarks = Bookmark.objects.filter(q)
    context = {
    'bookmarks' : bookmarks,
    'form': form,
    'search_results': search_results
    }
    return render(request, 'bookmarks/search.html', context)

@login_required
def friends_page(request, username):
    user = get_object_or_404(User, username= username)
    friends = [ friend.to_friend for friend in user.to_friend.all()]
    friend_bookmarks = Bookmarks.objects.filter(user__in= friends)
    context = {
    'username' : username,
    'friends' : friends,
    'friend_bookmarks': friend_bookmarks,
    }
    return render(request, 'bookmarks/friends_page.html', context)
