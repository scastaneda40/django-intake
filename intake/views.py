from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import SubmissionForm
from .models import Submission
from django.contrib.auth.decorators import login_required, user_passes_test

# Homepage
def home(request):
    if request.user.is_authenticated:
        # Redirect superusers to the admin dashboard
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        # Redirect regular users to their submission history
        return redirect('submission_history')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Use your existing registration form
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Assign role based on form input
            role = request.POST.get('role', 'student')  # Default to "student"
            if role == 'admin':
                group, created = Group.objects.get_or_create(name='Admin')
            else:
                group, created = Group.objects.get_or_create(name='Student')

            # Add the user to the group
            user.groups.add(group)
            messages.success(request, f"Account created for {role.capitalize()}!")

            # Log the user in and redirect
            login(request, user)
            return redirect('home')  # Change 'home' to your desired URL
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def submit_form(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, user=request.user)  # Pass user argument
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('submission_history')
    else:
        form = SubmissionForm(user=request.user)  # Pass user argument for prepopulation
    return render(request, 'submit_form.html', {'form': form})


@login_required
def submission_history(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, 'submission_history.html', {'submissions': submissions})

@user_passes_test(lambda u: u.is_superuser)  # Restrict access to superusers
def admin_dashboard(request):
    submissions = Submission.objects.all()  # Fetch all submissions
    return render(request, 'admin_dashboard.html', {'submissions': submissions})

@user_passes_test(lambda u: u.is_superuser)  # Restrict to admins
def change_status(request, submission_id, status):
    submission = get_object_or_404(Submission, id=submission_id)
    if status in ['Approved', 'Rejected']:
        submission.status = status
        submission.save()
    return redirect('admin_dashboard')


# Create your views here.
