from django.http import JsonResponse

def placeholder_view(request):
    return JsonResponse({"message": "Reviews endpoint is working"})
