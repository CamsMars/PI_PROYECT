import os
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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
    if request.user.is_authenticated:
        if request.method == "POST":
        # Accede a los datos enviados desde el formulario
            name = request.POST.get("name")
            last_name = request.POST.get("last-name")
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")
            favorites = request.POST.get("favorites")
            feelings = request.POST.get("feelings")
            print(name,last_name,email,username,password,favorites,feelings)

        # Obtiene el perfil del usuario actual o crea uno nuevo
        #profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Asigna los datos al perfil
        #profile.name = name
        #profile.last_name = last_name
        #profile.email = email
        #profile.username = username
        #profile.password = password  # Recuerda manejar la contraseña de forma segura
        #profile.feelings = feelings
        #profile.save()  # Guarda los cambios
        return render(request, 'profile.html')
    else:
        # Si el usuario no está autenticado, redirigir al login
        return redirect('loginaccount')