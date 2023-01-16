from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import datetime
import googletrans
from googletrans import *


from .models import Profile

# Create your views here.

PREFERRED_LANGUAGE = ""

def index(request):

    labels_one_day = []
    labels_one_week = []
    labels_one_month = []
    data_one_day = []
    data_one_week = []
    data_one_month = []

    date = datetime.date.today()
    last_week = date - datetime.timedelta(days=6)
    last_month = date - datetime.timedelta(days=31)
    
    try:
        queryset_today = Profile.objects.filter(user=request.user, date=date)
        queryset_week= Profile.objects.filter(user=request.user, date__range=[last_week, date])
        queryset_month= Profile.objects.filter(user=request.user, date__range=[last_month, date])
        for sentence in queryset_today:
            labels_one_day.append(str(sentence.date))
            data_one_day.append(sentence.translations_done)

        for sentence in queryset_week:
            labels_one_week.append(str(sentence.date))
            data_one_week.append(sentence.translations_done)

        for sentence in queryset_month:
            labels_one_month.append(str(sentence.date))
            data_one_month.append(sentence.translations_done)

        context = {'labels_one_day': labels_one_day, 'data_one_day': data_one_day, 'labels_one_week': labels_one_week, 'data_one_week': data_one_week, 'labels_one_month': labels_one_month, 'data_one_month': data_one_month,}
        return render(request, 'index.html', context)
    except:
        return render(request, 'index.html')

def translate(request):
    if request.method == 'POST':
        date = datetime.date.today()

        translation_object_queryset = Profile.objects.filter(user=request.user, date=date)

        if translation_object_queryset.exists():
            translation_object = Profile.objects.get(user=request.user, date=date)
            sentence = request.POST.get('sentence', '')

            language_list = ["ru", "fr", "es", "ro", "en", "de", "pt", 'no', 'ja']

            translator = googletrans.Translator()
            translate = ""

            if PREFERRED_LANGUAGE in language_list:
                language_list.remove(PREFERRED_LANGUAGE)
            translated_sentences = []


            for i in language_list:
                translate = translator.translate(sentence, dest=i).text
                translated_sentences.append(translate)

            translation_object.translations_done = translation_object.translations_done + len(language_list)
            translation_object.user = request.user
            translation_object.save()
            
        
            return render(request, 'translate.html', {'translated_sentences': translated_sentences, "PREFERRED_LANGUAGE": PREFERRED_LANGUAGE})
        else:
            translation_object = Profile.objects.create(user=request.user, date=date)
            sentence = request.POST.get('sentence', '')
            
            language_list = ["ru", "fr", "es", "ro", "en", "de", "pt", 'no', 'ja']

            translator = googletrans.Translator()
            translate = ""

            if PREFERRED_LANGUAGE in language_list:
                language_list.remove(PREFERRED_LANGUAGE)
            translated_sentences = []


            

            for i in language_list:
                translate = translator.translate(sentence, dest=i).text
                translated_sentences.append(translate)

            translation_object.translations_done = translation_object.translations_done + len(language_list)
            translation_object.user = request.user
            translation_object.save()

        
            return render(request, 'translate.html', {'translated_sentences': translated_sentences, "PREFERRED_LANGUAGE": PREFERRED_LANGUAGE})
    else:
        return render(request, 'translate.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Credentials are Invalid!')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatedPassword = request.POST['repeatedPassword']
        
        if password == repeatedPassword:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already used!')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already used!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                messages.success(request, "You registered successfully")

                return redirect('login')
        else:
            messages.warning(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    messages.success(request, " You successfully logged out")

    return redirect("/")
