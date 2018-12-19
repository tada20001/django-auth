from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Post

post_list = ListView.as_view(model=Post)

post_detail = DetailView.as_view(model=Post)

@login_required
@permission_required('blog.can_view_goldpage', login_url=reverse_lazy('goldmembership_guide'))
def goldpage_detail(request, pk):
    gold = get_object_or_404(Post)
    return render(request, 'blog/glodpage_detail.html', {'post': post})


def goldmembership_guide(request):
    return render(request, 'blog/goldmembership_guide.html')
