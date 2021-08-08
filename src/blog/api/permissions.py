from rest_framework.permissions import BasePermission

class IsCommentOwner(BasePermission):
    message = 'You must be the owner of the comment!'
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

