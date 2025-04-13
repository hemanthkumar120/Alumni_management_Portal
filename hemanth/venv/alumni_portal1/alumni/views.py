from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AlumniForm,EventForm
from .models import Alumni, Event, EventRegistration,AnnouncementReadStatus,Announcement
from django.contrib.auth.models import User
from django.contrib import messages

def register_alumni(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        alumni_form = AlumniForm(request.POST, request.FILES)
        if user_form.is_valid() and alumni_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            alumni = alumni_form.save(commit=False)
            alumni.user = user
            alumni.save()
            login(request, user)
            return redirect('profile')
    else:
        user_form = UserRegisterForm()
        alumni_form = AlumniForm()
    return render(request, 'alumni/register.html', {'user_form': user_form, 'alumni_form': alumni_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
    return render(request, 'alumni/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    alumni = get_object_or_404(Alumni, user=request.user)
    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES, instance=alumni)
        if form.is_valid():
            form.save()
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'alumni/profile.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'alumni/event_list.html', {'events': events})

@login_required
def event_register(request, id):
    event = get_object_or_404(Event, id=id)
    alumni = get_object_or_404(Alumni, user=request.user)
    EventRegistration.objects.get_or_create(event=event, alumni=alumni)
    return redirect('event_list')
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, AlumniForm
from django.contrib.auth import login
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        alumni_form = AlumniForm(request.POST, request.FILES)

        if user_form.is_valid() and alumni_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            alumni = alumni_form.save(commit=False)
            alumni.user = user
            alumni.save()

            login(request, user)  # Log the user in after signup
            return redirect('profile')  # Redirect to profile page
    else:
        user_form = UserRegisterForm()
        alumni_form = AlumniForm()

    return render(request, 'alumni/signup.html', {
        'user_form': user_form,
        'alumni_form': alumni_form
    })
from django.shortcuts import render

def home(request):
    return render(request, 'alumni/home.html')
@login_required
def alumni_list(request):
    query = request.GET.get('q')
    if query:
        alumni = Alumni.objects.filter(user__first_name__icontains=query) | Alumni.objects.filter(course__icontains=query)
    else:
        alumni = Alumni.objects.all()
    return render(request, 'alumni/alumni_list.html', {'alumni_list': alumni})
def announcements(request):
    from .models import Announcement
    announcements = Announcement.objects.order_by('-date_posted')
    return render(request, 'alumni/announcements.html', {'announcements': announcements})
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    total_alumni = Alumni.objects.count()
    total_events = Event.objects.count()
    recent_regs = EventRegistration.objects.select_related('alumni', 'event').order_by('-id')[:5]
    return render(request, 'alumni/admin_dashboard.html', {
        'total_alumni': total_alumni,
        'total_events': total_events,
        'recent_regs': recent_regs,
    })
@staff_member_required
def create_announcement(request):
    from .forms import AnnouncementForm
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'alumni/create_announcement.html', {'form': form})
from .models import Announcement, AnnouncementReadStatus, Alumni
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def announcements(request):
    alumni = get_object_or_404(Alumni, user=request.user)
    announcements = Announcement.objects.all().order_by('-date_posted')

    for ann in announcements:
        # Mark unread announcements as read when viewed
        read_status, created = AnnouncementReadStatus.objects.get_or_create(alumni=alumni, announcement=ann)
        if not read_status.read:
            read_status.read = True
            read_status.save()

    return render(request, 'alumni/announcements.html', {'announcements': announcements})

def unread_announcements_count(request):
    if request.user.is_authenticated:
        alumni = Alumni.objects.filter(user=request.user).first()
        if alumni:
            count = AnnouncementReadStatus.objects.filter(alumni=alumni, read=False).count()
            return {'unread_announcement_count': count}
    return {}
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'alumni/add_event.html', {'form': form})
