from django.shortcuts import render,redirect
# Create your views here.

from django.views.generic import TemplateView   #View nne pakaram, template ellapo egane cheyanam athanne easy
from api.forms import RegistrationForm,LoginForm,QuestionForm,AnswerForm
from django.views.generic import CreateView,FormView,ListView,DetailView
from django.contrib.auth import authenticate,login,logout

from api.models import Answers, MyUser,Questions
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache



def signin_reqired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_reqired,never_cache]

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name='home.html'
    model=Questions
    form_class=QuestionForm
    success_url=reverse_lazy("index")
    context_object_name="api"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    # def post(self, request,*args,**kwargs):
    #     form=QuestionForm(request.POST)
    #     if form.is_valid():
    #         quest=form.save(commit=False)
    #         quest.user=request.user
    #         quest.save()
    #         return redirect("index")

    def get_queryset(self):

        
        return Questions.objects.all().exclude(user=self.request.user)

class SignUpView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name='register.html'
    success_url=reverse_lazy('register')


class SignInView(FormView):
    form_class=LoginForm
    template_name='login.html'
    def post(self, request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect('index')
            else:
                return render(request,self.template_name,{'form':form})


@method_decorator(decs,name="dispatch")
class QuestionDetailView(DetailView,FormView):
    model=Questions
    template_name='question_detail.html'
    pk_url_kwarg="id"
    context_object_name="question"
    form_class=AnswerForm

@method_decorator(decs,name="dispatch")
def add_answer(request,*args,**kwargs):
    form=AnswerForm(request.POST)
    if form.is_valid():
        answer=form.cleaned_data.get('answer')
        qid=kwargs.get('id')
        ques=Questions.objects.get(id=qid)
        Answers.objects.create(question=ques,
        user=request.user,
        answer=answer)
        return redirect('index')
    else:
        return redirect('index')

@method_decorator(decs,name="dispatch")
def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get('id')
    ans=Answers.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    return redirect('index')



@method_decorator(decs,name="dispatch")
def remove_view(request,*args,**kwwargs):
    ans_id=kwwargs.get('id')
    Answers.objects.get(id=ans_id).delete()
    return redirect('index')

@method_decorator(decs,name="dispatch")
class GetAnswerView(ListView):
    model=Questions
    template_name='myanswers.html'
    context_object_name="api"

    def get_queryset(self):
        return Questions.objects.filter(user=self.request.user)




def signout_View(request,*args,**kwargs):
    logout(request)
    return redirect("login")
