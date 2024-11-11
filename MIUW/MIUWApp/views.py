import os
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")

        if user_input:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)

            if response and hasattr(response, 'text'):
                return JsonResponse({"generated_text": response.text})
            else:
                return JsonResponse({"error": "No se pudo generar contenido."}, status=500)
        else:
            return JsonResponse({"error": "El input del usuario está vacío."}, status=400)

    return render(request, 'chat.html')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'chattest.html')


def perfil(request):
    return render(request, 'profile.html')
