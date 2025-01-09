from django.shortcuts import render, get_object_or_404, redirect
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
