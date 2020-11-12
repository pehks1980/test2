from mainapp.models import Basket
import logging

logger = logging.getLogger(__name__)

def basket(request):
   basket = []

   if request.user.is_authenticated:
       basket = Basket.objects.filter(user=request.user)
       #logger.debug(f"access to User {request.user} basket via conetext processor")
   return {
       'basket': basket,
   }
