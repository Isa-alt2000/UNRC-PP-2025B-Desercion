from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='media/profiles/',
        null=True,
        blank=True,
        default='default_avatar.png'  # Imagen defaultt
    )
    alias = models.CharField(max_length=50, blank=True, null=True)
    profile_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def display_name(self):
        return self.alias or self.username

    def save(self, *args, **kwargs):
        if not self.profile_slug:
            # Crear slug desde alias o username
            base_text = self.alias if self.alias else self.username
            self.profile_slug = slugify(base_text)

            # Prevenir duplicados
            original_slug = self.profile_slug
            counter = 1
            while User.objects.filter(profile_slug=self.profile_slug).exclude(pk=self.pk).exists():
                self.profile_slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'profile_slug': self.profile_slug})

    def __str__(self):
        return self.username


# Señal para crear un perfil por defecto
@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Señal para operaciones posteriores a la creación del usuario"""
    if created:
        # Puedes agregar lógica adicional aquí si necesitas
        pass
