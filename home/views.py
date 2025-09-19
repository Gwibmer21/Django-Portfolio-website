from django.shortcuts import render, HttpResponse
from .models import Contact

# Create your views here.


def home(request):
    #contact form database
    # if request.method == 'POST':
    #     name == request.POST['name']
    #     email == request.POST['email']
    #     subject == request.POST['subject']
    #     message == request.POST['message']
    #     contact = models.Home(name=name, email=email, subject=subject, message=message)
    #     contact.save()
    return render(request, 'home.html')


def project(request):
    return render(request, 'project.html')


def user_management_dashboard(request):
    return render(request, 'user_management_dashboard.html')


def ancap_automation(request):
    return render(request, 'ancap_automation.html')


def contact(request):
    #contact form database
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
    return render(request, 'home.html')


def reroom(request):
    return render(request, 'reroom.html')


def insurance_call_simulator(request):
    return render(request, 'insurance_call_simulator.html')


def ocr_pdf_extractor(request):
    return render(request, 'ocr_pdf_extractor.html')


# Survey Creator project view
def survey_creator(request):
    return render(request, 'survey_creator.html')
