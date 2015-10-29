from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, FormView
from models import Product
from django.contrib import messages
from django.db.models import Count
from forms import CommentsForm


def index(request):
    return redirect('products/')


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


class ProductDetail(DetailView, FormView):
    model = Product
    template_name = 'product_detail.html'
    form_class = CommentsForm
    success_message = 'Product successfully commented'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            print(form)
            return self.form_valid(form)
        else:
            print(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super(ProductDetail, self).form_valid(form)

    def get_success_url(self):
        obj = self.get_object()
        return obj.get_absolute_url()


class LikeProduct(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'like_product.html'
    success_message = 'Product successfully liked'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.like(request.user)
        obj.save()
        messages.success(self.request, self.success_message)
        return redirect('products:product_detail', obj.slug)


