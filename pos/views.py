from django.shortcuts import render,get_object_or_404

from rest_framework.viewsets import ViewSet,ModelViewSet

from pos.models import Category,Product,Order,OrderItems

from pos.serializers import CategorySerializer,ProductSerializer,OrderSerializer,OrderItemSerializer

from rest_framework.response import Response

from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView

from rest_framework.views import APIView

from rest_framework import serializers

from twilio.rest import Client


# Create your views here.

class CategoryViewSet(ViewSet):

    serializer_class = CategorySerializer

    def list(self,request,*args,**kwargs):

        qs=Category.objects.all()

        serializer_instance=self.serializer_class(qs,many=True)

        return Response(data=serializer_instance.data)

    def create(self,request,*args,**kwargs):

        serializer_instance=self.serializer_class(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)

    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=get_object_or_404(Category,id=id)

        serializer_instance=self.serializer_class(qs,many=False)

        return Response(data=serializer_instance.data)


    def update(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        category_object=get_object_or_404(Category,id=id)

        serializer_instance=self.serializer_class(data=request.data,instance=category_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def destroy(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        category_object=get_object_or_404(Category,id=id)

        category_object.delete()

        return Response(data={"message":"deleted"})


class ProductCreateView(CreateAPIView):

    serializer_class=ProductSerializer

    def perform_create(self,serializer):

        id=self.kwargs.get("pk")

        category_instance=get_object_or_404(Category,id=id)

        serializer.save(category_object=category_instance)


class ProductViewSetView(ModelViewSet):

    http_method_names=['get','put','delete']

    serializer_class=ProductSerializer

    queryset=Product.objects.all()

    def get_queryset(self):
         
         qs=Product.objects.all()

         if "category" in self.request.query_params:
             
             category_name = self.request.query_params.get("category")

             qs=qs.filter(category_object__name=category_name)


         return qs


class OrderCreateView(CreateAPIView):

    serializer_class=OrderSerializer

 

 
class OrderItemCreateView(CreateAPIView):
        
       serializer_class=OrderItemSerializer

       def create(self,request,*args,**kwargs):
           
           order_id = kwargs.get("pk")

           order_instance = get_object_or_404(Order,id=order_id)

           product_id = request.data.get("product_object")

           product_instance = get_object_or_404(Product,id=product_id)

           qty = request.data.get("qty")

           order_item_instance,created = OrderItems.objects.get_or_create(
          order_object=order_instance,product_object=product_instance)


           if created:
               
               order_item_instance.qty=qty
               order_item_instance.save()

           else:
               
               order_item_instance.qty+=qty

               order_item_instance.save()

               
           serializer_instance=OrderItemSerializer(order_item_instance)
           
           return Response(serializer_instance.data)




         




    #    def perform_create(self,serializer):
           
    #        id=self.kwargs.get("pk")

    #        order_instance=get_object_or_404(Order,id=id)

    #        product_id=self.request.data.get('product_object')

    #        product_instance=get_object_or_404(Product,id=product_id)


   
    #        serializer.save(order_object=order_instance,product_object=product_instance)


           

class OrderRetrieveView(RetrieveAPIView):

    queryset=Order.objects.all()

    serializer_class=OrderSerializer




class GenerateBillView(UpdateAPIView):

    serializer_class=OrderSerializer

    queryset = Order.objects.all()

    def perform_update(self,serializer):

        id=self.kwargs.get("pk")

        order_instance=get_object_or_404(Order,id=id)

        if order_instance.status:

            raise serializers.ValidationError("bill has been already generated")

        order_items=OrderItems.objects.filter(order_object=order_instance)

        total=sum([oi.product_object.price * oi.qty for  oi in order_items])

        Send_invoice_to_whatsapp(order_instance,total)

        return serializer.save(status=True,total=total)
    


def Send_invoice_to_whatsapp(order_instance,total):

    account_sid = 'AC5c5608b9eda1791cabb0f448d7830d85'
    auth_token = 'ccbf90984f49e39252965625a5c11355'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= f"Order Completed - ordr_id= {order_instance.id} \n  total={total}",
    to='whatsapp:+919037405251'
    )

    print(message.sid)
        

        









