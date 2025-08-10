from rest_framework.permissions import BasePermission

from kanban_app.models import Board,Task




class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.members.all()
    



class IsBoardMember(BasePermission):
    """
    Kombinierte Permission für Board-Zugriff (POST und Objektbezogen).
    """

    def has_permission(self, request, view):
        board_id = request.data.get('board') or request.query_params.get('board')
        if not board_id:
            return True  # Kein Board übergeben → kein Check an dieser Stelle

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False

        return request.user == board.owner or request.user in board.members.all()

    def has_object_permission(self, request, view, obj):
        board = obj.board if hasattr(obj, "board") else obj
        return request.user == board.owner or request.user in board.members.all()



class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Erlaubt nur dem Ersteller der Task oder dem Eigentümer des Boards, die Task zu löschen.
    """

    def has_object_permission(self, request, view, obj):
        # obj ist hier eine Task
        user = request.user
        return user == obj.owner or user == obj.board.owner
    

class IsBoardMemberForTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Falls obj ein Comment ist, das Board über den Task holen
        if hasattr(obj, 'task'):
            board = obj.task.board
        # Falls obj ein Task ist, direkt Board holen
        elif hasattr(obj, 'board'):
            board = obj.board
        # Sonst ablehnen
        else:
            return False

        return user.id == board.owner.id or board.members.filter(id=user.id).exists()
class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user