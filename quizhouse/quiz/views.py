from django.shortcuts import render,redirect,get_object_or_404
from .models import Quiz,questions,userquizdata,quiztime
from .forms import basicquizdetails,CustomUserCreationForm,OptionFormSet,options,QuestionForm,userquizform
# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from datetime import datetime
import pytz

@login_required
def createquiz(request):
    if request.user.is_authenticated :
        if request.user.is_staff:
            pass
        else:
            return render(request ,'staffdashboard.html')
    else:
        return redirect('custom_login')
    if request.method == "POST":
        form=basicquizdetails(request.POST)
        if form.is_valid():
            quiz = form.cleaned_data['name']
            maxtime = form.cleaned_data['maxtime']
            numquestions = form.cleaned_data['numquestions']
            check = Quiz.objects.filter(quiz=quiz)
            if check.exists():
                print("not possible ")
            else:
                newdata=Quiz(quiz=quiz,maxtime=maxtime,numquestions=numquestions)
                newdata.save()
                return redirect('questioncreate' , quizobject=newdata.id)
    else:
        form = basicquizdetails()
    # context = {"form" : basicquizdetails}
    return render(request,'createquiz.html',{"form":form})    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
   # Check if the user is a staff member
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to the form submission view

        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'custom_login.html')
def custom_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method=="POST":
        form= CustomUserCreationForm(request.POST)
        print("h")
        if form.is_valid():
            form.save()
            print("created user")
            return redirect('custom_logout')
        else:
            messages.error(request,'correct these errors')
    else:
        form=CustomUserCreationForm()
    return render(request,'register.html',{"form":form})



def home(request):
    print(request.user.is_authenticated)
    return render (request , 'home.html' , {"timestamp": now().timestamp() , "user":request.user})
def about(request):
    pass
@login_required

def show_quiz(request):
    return render(request , 'showquizzes.html' ,{"quiz" : Quiz.objects.all() ,
                                                 "timestamp": now().timestamp() , "user":request.user})
@login_required
def questioncreate(request , quizobject):
    if request.user.is_staff:
            pass
    else:
        return render(request,'staffdashboard.html')
    if request.method=="POST":
        form= QuestionForm(request.POST)
        formset=OptionFormSet(request.POST)
        form.instance.quiz = Quiz.objects.get(id=quizobject)
        if form.is_valid()  and formset.is_valid():
            
            print(formset)
            
            question=form.save()#save the form and assign question to it
            for forms in formset:
                forms.instance.question=question
            formset.save()
            print(formset)
            questionscreated=questions.objects.filter(quiz=Quiz.objects.get(id=quizobject))
            if len(questionscreated) >= Quiz.objects.get(id=quizobject).numquestions:
                print("basassssssssssssss")
                return redirect('home')
            else:
                return  redirect('questioncreate' , quizobject=quizobject)

        else:
            print(form.errors)
            print(formset.errors)
            messages.error(request,'not valid')
    else:
        form = QuestionForm()
        formset=OptionFormSet(queryset=options.objects.none())
    return render(request , 'quiz_form.html' , {"queform": form , "formset":formset})

@login_required
def quizdetails(request, quizobject):
    if request.user.is_staff:
            pass
    else:
            return render(request ,'staffdashboard.html')
    currentquiz = get_object_or_404(Quiz, id=quizobject)
    matchingquestions = questions.objects.filter(quiz=currentquiz).prefetch_related('options_set').all()
    # Ensure "option_set" matches the related_name of the ForeignKey in your Option model
    return render(request, 'quizdetail.html', {
        "currentquiz": currentquiz,
        "questions": matchingquestions,
    })

@login_required
def takequiz(request , quizobject):
    currentquiz = get_object_or_404(Quiz, id=quizobject)
    matchingquestions = questions.objects.filter(quiz=currentquiz).prefetch_related('options_set').all()
    usersquizes=quiztime.objects.filter(user=request.user).filter(quiz=currentquiz)
    if len(usersquizes)==0:
        data = quiztime(user=request.user, quiz=currentquiz ,time=datetime.now())
        timeelapsed=0
        data.save()
    else:
        data=quiztime.objects.get(user=request.user , quiz=currentquiz)
        timezone = pytz.timezone('UTC')
        
        datatime=data.time
        timeelapsed=timezone.localize(datetime.now())-datatime
        # print(timeelapsed.total_seconds())#gives tot seconds
        if ((timeelapsed.total_seconds()/60) > currentquiz.maxtime):  
            print('time over nub')
            # return render(request,'home.html')
    userquizformset = modelformset_factory(
        userquizdata,
        form=userquizform,
        extra=len(matchingquestions)
    )
    if request.method=="POST":
        formset = userquizformset(request.POST)
        if formset.is_valid():
            # print(formset)
            for form in formset:
                print('\n', form.instance.choice)
                form.instance.user=request.user
            formset.save()
        else:
            print(formset.errors)
        pass
    else:
        formset=userquizformset(queryset=userquizdata.objects.none() )
    
    
    return render(request,'takequiz.html',{"quiz":currentquiz , "questions" : matchingquestions,
                                           "formset" : formset ,
                                           })
    