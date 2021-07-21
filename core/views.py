from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, OrderItem, Order, BillingAddress
from .forms import CheckOutForm


# Create your views here.

def item_list(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, "home-page.html", context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order,
            }
            return render(self.request, "order-summary.html", context) 
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")
        
    
class ProductDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This product was update from your cart!")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This product was added to your cart!")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This product was added to your cart!")
        return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request, "This product was removed from your cart!")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This product was not to in your cart!")
            return redirect("core:product", slug=slug)            
    else:
        #add a message saying user doesnt have a order
        messages.info(request, "You do not have a active order.")
        return redirect("core:product", slug=slug)

@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, ordered = False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This product was updated from your cart!")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This product was not to in your cart!")
            return redirect("core:order-summary", slug=slug)            
    else:
        #add a message saying user doesnt have a order
        messages.info(request, "You do not have a active order.")
        return redirect("core:order-summary", slug=slug)

class CheckOutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            "form": form,
        }
        return render(self.request, "checkout-page.html")

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                apartament_address = form.cleaned_data.get("apartament_address")
                country = form.cleaned_data.get("country")
                zip = form.cleaned_data.get("zip")
                # TODO: add func for these fieds
                # same_shipping_address = form.cleaned_data.get("same_shipping_address")
                # save_info = form.cleaned_data.get("save_info")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address = street_address,
                    apartament_address = apartament_address,
                    country = country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect("core:checkout")
            messages.warning(self.request, "Failed checkout")
            return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")




            


    