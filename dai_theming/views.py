from django.shortcuts import render

def howto_view(request):
    return render(request, 'dai_theming/howto.html')

