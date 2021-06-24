from django.shortcuts import render
from gmailapp.models import MyUser,Registration,Gmail
from gmailapp.forms import GmailForm
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



def index(request):
    return render(request,'index.html',)
def view(request):
    return render(request, 'email.html')
def register_page(request):
    return render(request,'register_page.html')
def save_register(request):

    if request.method == "POST":
        #import pdb
        #pdb.set_trace()
        user = MyUser.objects.create_user(email=request.POST['email'], password=request.POST['password'])
        Registration.objects.create(myuser=user)
        return render(request, 'index.html')
    else:
        return render(request, 'index.html', {'error': 'you are not eigible for this job'})
def validation_login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'email.html')


    else:
        return render(request, 'index.html', {'error': 'Invalid username or password'})

def compose(request):
    user=request.user
    print(user.id)
    form=GmailForm
    return render(request,'compose.html',{'form':form,'user':user})

def save_mail(request):
    """TO send the mails from user"""
    if request.method == "POST":
        if request.POST["send"] != "cancel":
            subject = request.POST.get('subject')
            body = request.POST.get('message')
            reciever = request.POST.get('email')
            send_mail(subject, body, settings.EMAIL_HOST_USER,
                      [reciever], fail_silently=False)
            Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body, is_draft=True)
            return render(request,"email.html")
        else:
            subject = request.POST.get('subject')
            body = request.POST.get('message')
            reciever = request.POST.get('email')
            send_mail(subject, body, settings.EMAIL_HOST_USER,
                      [reciever], fail_silently=False)
            Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body,is_draft=True)
            return render(request, "email.html")
    else:
        return render(request, "compose.html")
    # if request.method == 'POST':
    #     subject = request.POST.get('subject')
    #     body = request.POST.get('message')
    #     reciever = request.POST.get('email')
    #     send_mail(subject, body, settings.EMAIL_HOST_USER,
    #               # [reciever], fail_silently=False)
    #     Mail.objects.create(sender=request.user,
    #                         subject=subject,
    #                         reciever=MyUser.objects.get(email=reciever),
    #                         body=body
    #                         )
    #     return render(request, 'webmail/mail_sent.html', {'email': reciever})
    #
    # return render(request, 'webmail/index.html')


@login_required(login_url='/gmailapp/')
def inbox(request):
    """ mail inbox """
    mail = Gmail.objects.filter(reciever=request.user).filter(is_spam=False)
    return render(request, 'inbox.html', {'mail': mail})

@login_required(login_url='/gmailapp/')
def sent_mail(request):
    user = request.user
    mail = user.email
    print(mail)
    print(type(mail))
    sent = Gmail.objects.filter(sender=user).filter(is_spam=False)
    print([each for each in sent])
    import pdb
    # pdb.set_trace()
    """ sent mails"""
    # sent = Gmail.objects.filter(sender='mail')
    # pdb.set_trace()

    return render(request, 'sent_mail.html', {'mail': sent})

@login_required(login_url='/gmailapp/')
def make_spam(request, id):
    """ making spam mails"""
    Gmail.objects.filter(id=id).update(is_spam=True)

    return render(request, 'inbox.html')

@login_required(login_url='/gmailapp/')
def spam(request):
    """ spam mails """
    user = request.user
    data = Gmail.objects.filter(is_spam=True).filter(reciever=user)
    return render(request, 'spam.html', {'mail': data})


def logout_page(request):
    """ logout page"""
    logout(request)
    return HttpResponseRedirect('/gmailapp/')


@login_required(login_url='/gmailapp/')
def make_unspam(request, id):
    """ making spam mails"""
    Gmail.objects.filter(id=id).update(is_spam=False)
    return render(request, 'inbox.html')


def make_draft(request, id):
    """ making drafts """
    Gmail.objects.filter(id=id).update(is_draft=True)
    return render(request, 'email.html', {'msg': 'message saved as draft'})


def draft(request):
    data = Gmail.objects.filter(is_draft=True)
    print(data)
    return render(request, 'draft.html', {'data': data})


def make_trash(request, id):
    Gmail.objects.filter(id=id).update(is_trash=True)
    return render(request, 'email.html')


def trash(request):
    user = request.user
    data = Gmail.objects.filter(is_trash=True).filter(reciever=user).filter(sender=user)
    return render(request, 'trash.html', {'data': data})


def make_untrash(request, id):
    Gmail.objects.filter(id=id).update(is_trash=False)
    return render(request, 'email.html')


def delete(request, id):
    Gmail.objects.filter(id=id).delete()
    return render(request, 'email.html')


def save_draftmail(request):
    """ saving mils"""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('message')
        # file = request.POST.get('file')
        reciever = request.POST.get('email')
        # send_mail(subject, body, settings.EMAIL_HOST_USER,
        #           [reciever], fail_silently=False)
        import pdb
        # pdb.set_trace()
        Gmail.objects.create(sender=request.user,
                             subject=subject,
                             reciever=MyUser.objects.get(email=reciever),
                             body=body, is_draft=True)
        return render(request, 'email.html', {'email': reciever})

    return render(request, 'index.html')






# Create your views here.
