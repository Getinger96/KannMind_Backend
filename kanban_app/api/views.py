from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import BoardSerializer,BoardCreateSerializer
from kanban_app.models import Board

@api_view(['GET','POST'])
def first_view(request):

    if request.method == 'GET':
        board = Board.objects.all()
        serializer = BoardSerializer(board, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    

@api_view(['GET','DELETE','PUT'])
def first_single_view(request,pk):

    if request.method == 'GET':
        board = Board.objects.get(pk=pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        board = Board.objects.get(pk=pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        board = Board.objects.get(pk=pk)
        serializer = BoardSerializer(board)
        board.delete()
        return Response(serializer.data)

