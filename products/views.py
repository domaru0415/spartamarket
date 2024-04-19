from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Product, Like
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, HttpResponseRedirect

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            liked_products_ids = user.like_set.values_list('product_id', flat=True)
            context['liked_products_ids'] = liked_products_ids
        else:
            context['liked_products_ids'] = []
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        user = self.request.user
        if user.is_authenticated:
            context['is_liked'] = product.like_set.filter(user=user).exists()
        else:
            context['is_liked'] = False
        return context


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('product_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("수정 권한이 없습니다.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("삭제 권한이 없습니다.")
        return super().dispatch(request, *args, **kwargs)

def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        like.delete()
    
    redirect_url = request.META.get('HTTP_REFERER', reverse('product_detail', kwargs={'pk': pk}))
    return redirect(redirect_url)