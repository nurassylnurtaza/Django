from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, ListView, DeleteView, UpdateView,DetailView
from django.urls import reverse_lazy, reverse
from .models import Post, Comment

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('post_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

class PostDetailWithCommentsView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id = self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_id']})