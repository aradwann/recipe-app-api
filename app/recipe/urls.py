from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('tags', views.TagViewSet, basename="Tag")
router.register('ingredient', views.IngredientViewSet, basename="Ingredient")
router.register('recipe', views.RecipeViewSet, basename="Recipe")

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
