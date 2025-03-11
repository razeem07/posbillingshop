

from django.urls import path

from pos import views

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("category",views.CategoryViewSet,basename="category"),

router.register("products",views.ProductViewSetView,basename="product")




urlpatterns=[


path("category/<int:pk>/product/",views.ProductCreateView.as_view()),


    
]+router.urls