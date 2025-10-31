from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


@method_decorator(cache_page(60), name="retrieve")   # detalle cacheado 60s
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet para posts con búsqueda, paginación y cache
    """
    queryset = Post.objects.filter(status="published").select_related("author", "category")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'body']
    filterset_fields = ['category', 'author']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer

    def get_object(self):
        """
        Permite buscar por ID o slug
        """
        lookup_value = self.kwargs[self.lookup_field]
        
        # Intentar buscar por ID primero
        if lookup_value.isdigit():
            obj = get_object_or_404(self.get_queryset(), id=lookup_value)
        else:
            # Buscar por slug
            obj = get_object_or_404(self.get_queryset(), slug=lookup_value)
        
        # Incrementar vistas solo en retrieve
        if self.action == 'retrieve':
            obj.increment_views()
        
        return obj