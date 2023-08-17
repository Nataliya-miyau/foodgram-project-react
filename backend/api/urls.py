from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (DownloadShoppingCartView, IngredientViewSet,
                       RecipeShoppingCartViewSet, RecipeViewSet, TagViewSet,
                       UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register('recipes', RecipeViewSet, 'recipes')
router.register('recipes', RecipeShoppingCartViewSet, 'recipes')
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart',
    ),
    path('', UserViewSet.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
