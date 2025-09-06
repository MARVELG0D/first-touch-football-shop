from django.shortcuts import render

def show_main(request):
    context = {
        'app' : 'First Touch Football Shop',
        'npm' : '2406421346',
        'name': 'Marvel Irawan',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)