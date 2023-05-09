from django.shortcuts import render
from django.http import HttpResponse

#from .models import testtb
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings


from . models import *

from tensorflow.keras import backend as K

from suicide_det import test_suicide

from emotion_det import test_emotion

import chatbot as chbt

from datetime import datetime

import pycurl
from urllib.parse import urlencode

def sends_mail(mail,msg):

	crl = pycurl.Curl()
	crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
	data = {'email': mail,'msg':msg}
	pf = urlencode(data)

	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	crl.setopt(crl.POSTFIELDS, pf)
	crl.perform()
	crl.close()



def first(request):
    return render(request,'index.html')
    
    
    

def index(request):
    return render(request,'index.html')

def reg(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=register(name=name,phone=phone,email=email,password=password)
        reg.save()
    return render(request,'login.html')



def login(request):
    return render(request,'login.html')

def logint(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif register.objects.filter(email=email,password=password).exists():
        userdetails=register.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
        
        return render(request,'index.html')
        
    else:
        return render(request, 'login.html', {'success':'Invalid email id or Password'})
        
        
        
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)
        
def diary(request):
    if request.method=="POST":
        sel = register.objects.filter(id=request.session['uid'])
        notes=request.POST.get('notes')
        K.clear_session()
        suicide_res=test_suicide.predict(str(notes))
        K.clear_session()
        emotion_res=test_emotion.predict(str(notes))
        K.clear_session()
        print("result:",suicide_res,emotion_res)
        suggestions={'fear':"I'm sorry to hear that you're feeling fear. Fear is a natural and normal response to perceived threats or danger, but it can also be overwhelming and challenging to manage. It's important to acknowledge and validate your feelings of fear, and to remind yourself that you are not alone in experiencing them. Some things that may help you cope with your fear include practicing relaxation techniques, such as deep breathing or meditation, seeking support from a trusted friend or mental health professional, engaging in activities that bring you a sense of calm or comfort, and taking small steps to face your fears in a safe and supportive environment. Remember, it's okay to take things one step at a time, and to seek help if you need it.",
                     'joy':"I'm happy to hear that you're feeling joyful! To prolong and deepen your joy, consider practicing gratitude, connecting with others, taking care of your physical health, and engaging in activities that bring you joy. Cherishing these moments of joy and finding ways to extend and deepen them can help improve your overall well-being and happiness.",
                     'sadness':"I'm sorry to hear that you're feeling sad. It's important to acknowledge and validate our emotions, including sadness. It's okay to take some time to process and work through these feelings. Some things that might help you cope with your sadness include talking to someone you trust, such as a friend or mental health professional, practicing self-care, engaging in activities that you enjoy, and finding healthy ways to express your emotions, such as through journaling or art. Remember, it's important to take care of yourself and seek support when you need it.",
                     'anger':"I'm sorry to hear that you're feeling angry It's understandable to experience this emotion from time to time, but it's important to find healthy ways to cope with it. if you find that your anger is becoming overwhelming and difficult to manage on your own, it may be helpful to speak with a mental health professional who can provide you with additional support and guidance.Remember, it's important to take care of your mental health and find healthy ways to cope with difficult emotions like anger.",
                     'love':"It's wonderful to hear that you're feeling love! Love can be a powerful and positive emotion that can bring a sense of connection and meaning to our lives. To nurture and deepen your feelings of love, it may be helpful to express your feelings to the person or people you love, whether it's through words, actions, or small gestures. It can also be helpful to practice self-love and self-compassion, as these feelings can help us develop a healthier and more positive relationship with ourselves. Remember to cherish and appreciate the love you feel and to find ways to express and extend it to those around you."}
        sugg=suggestions[emotion_res]
        if suicide_res=="suicide":
            body="name:",sel[0].name,"phone",sel[0].phone
            sends_mail("jishnujanardhanan937@gmail.com",body)

        return render(request,'diary.html',{'emotion':emotion_res,'suicide':suicide_res,'suggestion':sugg})

    return render(request,'diary.html')
    

def chatbot(request):
    return render(request,'chatbot.html')

def chat(request):
    message=request.GET.get("msg")
    response=str(chbt.talk(message,"chatbot"))
    print("message:",message,"  Response:",response)
    return HttpResponse(response, content_type='text/plain')

def viewusers(request):
    sel=register.objects.all()
    return render(request,'viewusers.html',{'res':sel})

def doctorchat(request,id):
    request.session['chat_id']=id
    return render(request,'doctorchat.html')

def chatss(request):
    if request.method=="POST":
        sel=chats.objects.filter(user_id=request.session['chat_id'])
        print(sel)
        msg=request.POST.get('msg')
        dt=datetime.now()
        sel1=chats(user_id=request.session['chat_id'],d_chat=msg,datetme=dt.timestamp())
        sel1.save()
        return render(request,'doctorchat.html',{'res':sel})
    
def userchat(request):
    if request.method=="POST":
        sel=chats.objects.filter(user_id=request.session['uid'])
        print(sel)
        msg=request.POST.get('msg')
        dt=datetime.now()
        sel1=chats(user_id=request.session['uid'],u_chat=msg,datetme=dt.timestamp())
        sel1.save()
        return render(request,'userchat.html',{'res':sel})
    return render(request,'userchat.html')
