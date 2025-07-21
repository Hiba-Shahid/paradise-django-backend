from django.db import models
from apis.models.competition import Competition

# Create your models here.
class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

class StaticPage(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Page(models.Model):
    SLUG_CHOICES = [
        ('how-to-play', 'How to Play'),
        ('privacy-policy', 'Privacy Policy'),
        ('terms-and-conditions', 'Terms and Conditions'),
        ('faq', 'FAQ'),  
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, choices=SLUG_CHOICES)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, blank=True)  
    is_active = models.BooleanField(default=True)

class SiteDesignSetting(models.Model):
    LAYOUT_CHOICES = [
        ('wide', 'Wide Layout'),
        ('narrow', 'Narrow Layout')
    ]
    FONT_CHOICES = [
        ('jhenghei', 'Microsoft Jhenghei UI'),
        ('roboto', 'Roboto'),
        ('open_sans', 'Open Sans'),
    ]
    layout_type = models.CharField(max_length=10, choices=LAYOUT_CHOICES, default='narrow')
    font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='jhenghei')
    primary_color = models.CharField(max_length=7, default='#000000') 
    secondary_color = models.CharField(max_length=7, default='#3C3C3C') 
    accent_color = models.CharField(max_length=7, default='#00FFEA') 
    highlight_color = models.CharField(max_length=7, default='#F8A800')  
    updated_at = models.DateTimeField(auto_now=True)

class Language(models.Model):
    code = models.CharField(max_length=5)  
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)


class HeroBanner(models.Model):
    image = models.ImageField(upload_to='hero_banners/')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

class PopupMessage(models.Model):
    TRIGGER_CHOICES = [
        ('registration', 'After Registration'),
        ('login', 'After Login'),
    ]
    trigger = models.CharField(max_length=20, choices=TRIGGER_CHOICES)
    message = models.TextField()
    is_active = models.BooleanField(default=True)

