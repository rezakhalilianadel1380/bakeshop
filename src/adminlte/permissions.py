from doctest import FAIL_FAST
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission,SAFE_METHODS



class Is_View_Cart(BasePermission):
    def has_permission(self,request,view):
        if request.user.has_perm('order.view_cart'):
            return True
        raise PermissionDenied({"message":"You don't have permission to access"})


class Read_Only(BasePermission):
    """only read request accept"""

    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        raise PermissionDenied({"message":"only read"})

    # def has_object_permission(self, request, view, obj):
    #        raise PermissionDenied({"message":"suck it read"})

    
class Change_Cart_Permisson(BasePermission):
    """permission change_Order"""

    def has_permission(self,request,view):
        if request.user.has_perm('order.change_cart'):
            return True
        raise PermissionDenied({"message":"only read"})

    # def has_object_permission(self, request, view, obj):
    #        raise PermissionDenied({"message":"suck it read"})

    
class Setting_Permission(BasePermission):
    """only user has change_setting can accesss"""

    def has_permission(self,request,view):
        if request.user.has_perm('acountt.change_setting'):
            return True
        return False

    # def has_object_permission(self, request, view, obj):
    #        raise PermissionDenied({"message":"suck it read"})


class User_Delete_Permission(BasePermission):
    """permission for delete user """

    def has_permission(self,request,view):
        if request.user.has_perm('auth.delete_user'):
            return True
        return False


class Bread_permission(BasePermission):
    """permission for delete bread """

    def has_permission(self,request,view):
        if request.user.has_perm('bread.delete_bread'):
            return True
        return False