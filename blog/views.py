from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    params = {
        'posts':posts
        }
    return render(request, 'blog/post_list.html', params)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    params = {
        'post': post
        }
    return render(request, 'blog/post_detail.html', params)


def post_new(request):
    
    if request.method =='POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            
            return redirect('post_detail', pk=post.pk)
        
    else:
        form = PostForm()
        
    params = {
        'form':form
        }
    return render(request,'blog/post_edit.html', params)



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method=='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk )
    else:   
        form = PostForm(instance=post)
    
    params = {
        'form': form
        }
        
    return render(request, 'blog/post_edit.html', params)