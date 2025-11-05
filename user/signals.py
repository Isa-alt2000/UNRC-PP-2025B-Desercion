"""from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name == "user":  # aseguramos que solo corra para esta app
        # Definir los roles
        roles = {
            "Usuario": [],
            "Editor": ["add_post", "change_post"],
            "Moderador": ["change_post", "delete_post", "delete_comment"],
            "Administrador": ["add_post", "change_post", "delete_post", "view_post",
                              "add_comment", "change_comment", "delete_comment", "view_comment"],
        }

        # Obtenemos modelos Post y Comment
        Post = apps.get_model("user", "Post") if apps.is_installed("user") else None
        Comment = apps.get_model("user", "Comment") if apps.is_installed("user") else None

        # Crear grupos y asignar permisos
        for role, perms in roles.items():
            group, created = Group.objects.get_or_create(name=role)

            # limpiar permisos previos
            group.permissions.clear()

            # asignar permisos
            for perm_code in perms:
                if "comment" in perm_code and Comment:
                    try:
                        permission = Permission.objects.get(codename=perm_code, content_type__app_label="user", content_type__model="comment")
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        pass
                elif "post" in perm_code and Post:
                    try:
                        permission = Permission.objects.get(codename=perm_code, content_type__app_label="user", content_type__model="post")
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        pass

            group.save()
            print(f" Grupo '{role}' creado/actualizado con permisos.")
            """
