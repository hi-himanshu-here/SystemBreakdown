from django.shortcuts import render
from django.http import JsonResponse

def crash(request):
    x = 1 / 0
    return JsonResponse({"message": "won't reach"})


