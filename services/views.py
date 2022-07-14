from . forms import *
from . models import *
from . mixins import *
from django.http import Http404
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.
#Class Based Views
class WorkCreateView(UserPermissionMixin,SuccessMessageMixin,generic.CreateView):
    form_class = WorkCreateForm
    template_name = "services/CreateWork.html"
    success_url = reverse_lazy("home")
    success_message = "Work was successfully Assigned"
    def form_valid(self,form):
        form.instance.created_by = self.request.user
        super(WorkCreateView, self).form_valid(form)
        return redirect("home")
class ManageWorksView(LoginRequiredMixin,UserPermissionMixin,generic.ListView):
    model = Work
    fields = ['title','description','deadline','assigned_to']
    template_name = "services/ViewAllWorks.html"
    def queryset(self):
        return Work.objects.all().order_by('-date_of_creation')
    
class WorkDetailView(LoginRequiredMixin,generic.DetailView):
    model = Work
    fields = ['title','description','date_of_creation','deadline','created_by','assigned_to']
    template_name = "services/ViewWork.html"
    def get_object(self):
        work = super(WorkDetailView,self).get_object()
        if self.request.user in work.assigned_to.all() or self.request.user == work.created_by or self.request.user.is_superuser:
            return work
        raise Http404
class WorkUpdateView(LoginRequiredMixin,UserPermissionMixin,generic.UpdateView):
    model = Work
    slug_field = "Work.slug"
    fields = ['title','description','date_of_creation','deadline','created_by','assigned_to']
    template_name = "services/UpdateWork.html"
#Function Based Views
def home(request):
    progress = Progress.objects.filter(user = request.user,progress = "ASSIGNED").order_by('-assigned_work__date_of_creation')
    return render(request,"services/home.html",{"Progress":progress})
def landingpage(request):
    if request.user.is_authenticated:
        return redirect("portal")
    return render(request,"services/landing_page.html")
@login_required
def update_progress_by_member(request,pk):
    progress = get_object_or_404(Progress,pk=pk)
    if request.user in progress.assigned_work.assigned_to.all():
        progress_form = ProgressUpdateForm(request.FILES or None, request.POST or None,instance = progress)
        if progress_form.is_valid():
            progress_form.instance.progress = "APPROVAL PENDING"
            progress_form.save()
            messages.success(request,"Successfully Submitted for Approval")
            return redirect("portal")
        return render(request,'services/progress_update.html',{"progress":progress,"form":progress_form})
    else:
        messages.error(request,"Error Processing your Request")
        return redirect('portal')
    
        