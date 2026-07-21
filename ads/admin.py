from django.contrib import admin
from .models import Ad, AdImage


class AdImageInline(admin.TabularInline):
    """Фото показываем прямо внутри страницы объявления в админке."""
    model = AdImage
    extra = 1


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'status', 'author', 'views', 'created_at']
    list_filter = ['category', 'status']
    search_fields = ['title']
    inlines = [AdImageInline]
