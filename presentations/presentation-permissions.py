from rest_framework import permissions

class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    Permiso para permitir acceso solo a propietarios o colaboradores
    """
    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario es propietario o colaborador
        return obj.owner == request.user or request.user in obj.collaborators.all()

class IsOwner(permissions.BasePermission):
    """
    Permiso para permitir acceso solo a propietarios
    """
    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario es propietario
        return obj.owner == request.user