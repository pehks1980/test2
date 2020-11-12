from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.views.generic.base import View

from start_mag import settings
from mainapp.models import Product, Basket, ShopUser
from mainapp.forms import ShopUserLoginForm
from django.contrib import auth
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def main(request):
    context = {
        'title': 'Главная страница'
    }
    logger.info("Index page accessed")
    return render(request, 'index.html', context)

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = ShopUserLoginForm

    def post(self, request):
        email = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                logger.info(f"User {user} successfully logged in")
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
        logger.info(f"User {user} could'not get logged in")
        return render(request, "index.html")

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход пользователя'
        return context


class UserLogoutView(View):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выход пользователя'
        return context

    def get(self, request):
        logger.info(f"User {request.user} logged out")
        auth.logout(request)
        return render(request, "logout.html")


class ProductsView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    template_name = 'products.html'

    def get_queryset(self):
        logger.info(f"User {self.request.user} accessed product page")
        return self.model.objects.filter(is_active=True).order_by('id')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def basket_add(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        ref = reverse('products')
        return HttpResponseRedirect(ref)
    #find product in product table
    product = get_object_or_404(Product, pk=pk)
    #if product already exists in basket
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        #if this product is new in basket
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    logger.info(f"User {request.user} added 1 '{product.name}' to his basket")
    return render(request, 'added.html')

@login_required
def basket_del(request, pk):

    basket_row = get_object_or_404(Basket, pk=pk)
    logger.info(f"User {request.user} removed 1 '{basket_row.product.name}' from basket")
    basket_row.delete()

    ref = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(ref)

# - поля (по одному на строку): Клиент, Номер заказа, Адрес доставки.
# - на выходе должен быть PDF файл в каталоге, предназначенном для хранения этих файлов.
# - использовать wkhtmltopdf.
from mainapp.tasks import sleepy, async_pdf_process
@login_required
def export_pdf(request):
    user_id = ShopUser.objects.filter(email=request.user).values('id')

    async_pdf_process.delay(user_id[0]['id'])
    #async_pdf_process(user_id[0]['id'])

    context = {
        'title': 'Экспорт накладной в PDF.',
        'file_pdf': '*.pdf',
        'pdf_path': settings.PDF_PATH,
    }
    logger.info(f"User {request.user} exported manifest pdf")
    return render(request, 'export_pdf.html', context)

class BasketView(ListView):
    model = Basket
    context_object_name = 'basket'
    template_name = 'basket_list.html'

    def get_queryset(self):
        logger.info(f"User {self.request.user} checked his basket")
        return self.model.objects.filter(user=self.request.user).order_by('id')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ClientBasketView(ListView):
    model = Basket
    context_object_name = 'baskets'
    template_name = 'client_basket_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзины всех пользователей'
        return context

    def get_queryset(self):
        logger.info(f"User {self.request.user} checked clients baskets")
        qs = self.model.objects.select_related().order_by('user')
        return qs

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)