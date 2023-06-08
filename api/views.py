from rest_framework import status
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from .models import Expense
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# user signup


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    else:
        raise ValidationError(serializer.errors)


# user login
@api_view(['POST'])
def login(request):
    from rest_framework.decorators import api_view


@api_view(['GET'])
def index(request):
    return Response("Hello World")

# fetch all expenses


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
@parser_classes([JSONParser])
def getExpenses(request):
    try:
        user = request.user
        expenses = user.expense_set.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def getExpense(request, pk):
    try:
        expense = get_object_or_404(Expense, id=pk)
        serializer = ExpenseSerializer(expense, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=404)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def createExpense(request):
    data = request.data
    user = request.user

    try:
        expense = Expense.objects.create(
            title=data['title'],
            amount=data['amount'],
            user=user  # Set the user as the owner of the expense
        )
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    serializer = ExpenseSerializer(expense, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updateExpense(request, pk):
    data = request.data
    user = request.user

    try:
        expense = Expense.objects.get(id=pk, user=user)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found or you don't have permission to update."}, status=404)

    serializer = ExpenseSerializer(instance=expense, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def deleteExpense(request, pk):
    try:
        expense = get_object_or_404(Expense, id=pk)
        expense.delete()
        return Response("Expense was deleted")
    except Exception as e:
        return Response({"error": str(e)}, status=404)
