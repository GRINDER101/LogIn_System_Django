from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from pythondjango import settings
from django.core.mail import send_mail, EmailMessage
# from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . token import generate_token 




# Create your views here.

def home(request):

    return render(request, "authentication/index.html")


def signup(request):
        
    if request.method == "POST":
        
        #username = request.POST.get('username')
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "This username is already been in use. Can you please use a different username to register your account?")
            return redirect('home')

        #if User.objects.filter(email=email):
           # messages.error(request, "This email already exists. Can you please use a different email?")
            #return redirect('home')

        if len(username)>10:
            messages.error(request, "Length of the Username should be 10.") 
            return redirect('home') 

        if pass1 != pass2 :
            messages.error(request, "You've typed wrong password. Can you please confirm your password again?")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Your username should be alpha-numeric")  
            return redirect('home')    

        myuser = User.objects.create_user(username, email, pass1)   # type: ignore # here we created a object called "myuser" to store the datas of (username, email, password), so that we play with the object in back-end environment.

        myuser.first_name = fname   # there is another way to do the same previous work by individually store the data in a object called "myuser"
        myuser.last_name = lname

        myuser.is_active = False    # Here we inactivated myuser as we want to verify the user through a email-address confirmation link (CHECK LINE 70)

        # myuser.save()      # the save() function command will help to store the "myuser" object data in back-end.

        # messages.success(request, "You've been successfully registered!") # once the myuser object saved in back-end, we will confirm it by  sending a confirmation message to user

        # #Confirmation email will be sent to the user's email address once the user is registered in our data-base.

        # subject = "Confirmation email -(PythonDjango) App"
        # body = "Hello " + myuser.first_name + "\n It's a confirmation email from (PythonDjango) team, you have successfully registered with us.\n Thank you for considering us.\n\n Kind regards,\n Django team "
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, body, from_email, to_list, fail_silently=True)


        # EMAIL ADDRESS CONFIRMATION LINK (the user won't be able to get the access to signup to register their information in the data-base until or unless the user confirmed their identity by clicking the confirmation link sent to their email-address)

        # current_site = get_current_site(request)
        email_subject = "Confirmation Email Link -(PythonDjango) App"
        email_message = render_to_string("email_confirmation.html",{
            'name' : myuser.first_name,
            # 'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
         
        messages.success(request, " you need to first confirm your email address.")
        username = myuser.username
        return render(request, 'authentication/signin.html', {'username': username})

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == "POST":

        username = request.POST['username']
        pass1 = request.POST['pass1']
        email = request.POST.get('email')
        first_name = request.POST.get('fname')

        user = authenticate(username=username, password=pass1, email=email, fname=first_name)
        
        if user is not None:
            
            login(request, user)
            username = user.username

            # Confirmation email will be sent to the user's email address once the user is registered in our data-base.

            # subject = "SignIn email -(PythonDjango) App"
            # body = "Hello " + user.first_name + "\nIt's a SignIn email from (PythonDjango) team, you have successfully signed in.\nThank you for considering us.\n\nKind regards,\nDjango team "
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [user.email]
            # send_mail(subject, body, from_email, to_list, fail_silently=True)

            return render(request, "authentication/index.html", {'username': username})
        
        else:

            messages.error(request, "wrong input provided.")
            return redirect("home")


    return render(request, "authentication/signin.html")


def signout(request):

    logout(request)
    messages.success(request, "You've successfully logged out")
    return redirect('home')


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        messages.success(request, "You've been successfully registered!")
        login(request, myuser)
        username = myuser.username
        return render(request, "authentication/index.html", {'username': username})
    else:
        return render(request, "confirmation_failed.html")          
