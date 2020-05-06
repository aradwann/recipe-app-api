from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewSet, basename="Tag")
router.register('ingredient', views.IngredientViewSet, basename="Ingredient")


app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
