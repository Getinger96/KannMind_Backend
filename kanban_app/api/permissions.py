from rest_framework.permissions import BasePermission
from kanban_app.models import Board,Task




class IsBoardMemberOrOwner(BasePermission):
    """
    Erlaubt Zugriff, wenn der Benutzer entweder Eigentümer des Objekts
    oder Mitglied des zugehörigen Boards ist.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.members.all()


class IsBoardMember(BasePermission):
    """
    Kombinierte Permission für den Zugriff auf Boards.
    Prüft sowohl generelle Zugriffsrechte (POST-Anfragen mit Board-Angabe)
    als auch objektbezogene Rechte auf Board-Objekten.
    """

    def has_permission(self, request, view):
        """
        Prüft, ob der Benutzer Zugriff auf das angegebene Board hat,
        basierend auf 'board' in den Request-Daten oder Query-Parametern.
        Falls kein Board angegeben ist, wird der Zugriff nicht eingeschränkt.
        """
        board_id = request.data.get('board') or request.query_params.get('board')
        if not board_id:
            return True 

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False

        return request.user == board.owner or request.user in board.members.all()

    def has_object_permission(self, request, view, obj):
        """
        Prüft den Zugriff auf ein Board-Objekt.
        Falls das Objekt ein untergeordnetes Objekt mit 'board' ist,
        wird das Board ermittelt und die Mitgliedschaft/Eigentümerschaft geprüft.
        """
        board = obj.board if hasattr(obj, "board") else obj
        return request.user == board.owner or request.user in board.members.all()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Erlaubt Aktionen (z.B. Löschen) nur dem Ersteller der Task
    oder dem Eigentümer des zugehörigen Boards.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or user == obj.board.owner


class IsBoardMemberForTask(BasePermission):
    """
    Erlaubt Zugriff nur für Mitglieder des Boards, das mit einer Task oder einem Comment verknüpft ist.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'task'):
            board = obj.task.board
        elif hasattr(obj, 'board'):
            board = obj.board
        else:
            return False

        return user.id == board.owner.id or board.members.filter(id=user.id).exists()


class IsCommentAuthor(BasePermission):
    """
    Erlaubt Aktionen nur dem Autor des Comments.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
