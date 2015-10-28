from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView, DetailView
from models import Product, Comments
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.db.models import Count


def index(request):
    return redirect('products/')


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Your account is not active')
                return render(request, 'login.html', context_instance=RequestContext(request))
        else:
            messages.error(request, 'Wrong credentials')
            return render(request, 'login.html', context_instance=RequestContext(request))
    return render(request, 'login.html', context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('/')


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 10
    queryset = Product.objects.annotate(num_counts=Count('likes')).order_by('-num_counts')


class CreateProduct(CreateView):
    model = Product
    template_name = 'create_product.html'
    fields = '__all__'
    success_url = '/'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'


class LikeProduct(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'like_product.html'
    success_message = 'Product successfully liked'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.like(request.user)
        messages.success(self.request, self.success_message)
        return redirect('products:product_detail', obj.slug)


class AddComment(CreateView):
    model = Comments
    template_name = 'product_detail.html'
    fields = '__all__'
    success_message = 'Product successfully commented'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super(AddComment, self).form_valid(form)

    def get_success_url(self):
        return self.object.product.get_absolute_url()

