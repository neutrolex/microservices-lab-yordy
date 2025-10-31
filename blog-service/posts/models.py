from django.db import models
from django.utils import timezone
from slugify import slugify
from categories.models import Category
from authors.models import Author


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status == 'draft':
            self.published_at = None
            
        super().save(*args, **kwargs)

    def increment_views(self):
        """Incrementar contador de vistas"""
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def excerpt(self):
        """Generar excerpt del body"""
        return self.body[:200] + '...' if len(self.body) > 200 else self.body