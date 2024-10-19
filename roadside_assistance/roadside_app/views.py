from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm, ServiceProviderForm
from .models import ServiceProvider


  
#login
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser  # Assuming you have a CustomUser model

from django.contrib.auth import get_user_model

User = get_user_model()

def is_user_active(username):
    try:
        user = User.objects.get(username=username)
        return user.is_active  # Return True if active, False if not
    except User.DoesNotExist:
        return False  # User does not exist

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active:  # Check if the user is active
                    messages.error(request, "Your account has been deactivated. Please contact admin.")
                    return render(request, 'login.html', {'form': form})  # Return the form with the message
                else:
                    # Log the user in and create session
                    auth_login(request, user)
                    request.session['user_id'] = user.id  # Store the user ID in session

                    # Redirect based on the user role
                    if user.is_superuser:
                        return redirect('admin_dashboard')
                    elif user.role == 'user':
                        return redirect('user_dashboard')
                    elif user.role == 'service_provider':
                        return redirect('service_provider_dashboard')
                    else:
                        return redirect('home')  # Default redirection
            else:
                # Authentication failed, show appropriate message
                try:
                    user = CustomUser.objects.get(username=username)
                    if not user.is_active:
                        messages.error(request, "Your account has been deactivated. Please contact support.")
                    else:
                        messages.error(request, 'Invalid username or password.')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

def logout_view(request):
    # Log the user out and clear session
    auth_logout(request)
    request.session.flush()  # Clear all session data
    
    # Redirect to the login page or home page
    return HttpResponseRedirect('/')

#Registration
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, ServiceProviderForm
from .models import CustomUser, ServiceProvider

from django.shortcuts import render, redirect
from .models import ServiceProvider, ServiceType  # assuming these are your models
from .forms import ServiceProviderForm

def reg_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save user before any further actions
            
            if user.role == 'service_provider':
                return redirect('reg2', user_id=user.id)  # Redirect to the service provider registration form
            else:
                messages.success(request, 'Registration successful!')
                return redirect('login')  # Redirect to the login page after registration
        else:
            messages.error(request, 'Registration failed. Please check the details and try again.')
    else:
        form = RegistrationForm()
    
    return render(request, 'reg.html', {'form': form})

from django.http import HttpResponseRedirect
from django.urls import reverse

def reg2_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Get the user or 404
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, request.FILES)
        if form.is_valid():
            service_provider = form.save(commit=False)
            service_provider.user = user  # Link to the service provider's user account
            service_provider.save()
            messages.success(request, 'Service provider registration successful!')
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceProviderForm()
    
    return render(request, 'reg2.html', {'form': form}) 




def home_view(request):
    return render(request, 'home.html')

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    logout(request)  # This deletes the session
    messages.success(request, "You have successfully logged out.")
    return redirect('home')  # Redirect to login page after logout



#password reset

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

class CustomPasswordResetView(auth_views.PasswordResetView):
    """
    Handles the display and processing of the password reset form.
    """
    template_name = 'password/password_reset.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    Informs the user that an email has been sent for password reset.
    """
    template_name = 'password/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Handles the setting of a new password.
    """
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    Informs the user that the password has been successfully reset.
    """
    template_name = 'password/password_reset_complete.html'

########################################################################################################


# User View

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserUpdateForm

from django.contrib.auth.decorators import login_required
from .forms import CustomUserUpdateForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserUpdateForm
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')  # Redirect to login if not authenticated
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# View Profile
@login_required
def user_dashboard(request):
    user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user information
            messages.success(request, 'Your changes have been saved.')
            # return redirect('user_dashboard') # Redirect to display the success message
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserUpdateForm(instance=user)  # Load the current user data into the form

    context = {
        'form': form,
    }
    return render(request, 'user/user_dashboard.html', context)


def update_profile(request):
    return render(request, 'user/update_profile.html')

    
#update_profile
@login_required
def user_update_profile(request):
    user = request.user  # Get the current logged-in user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user information
            messages.success(request, 'Your changes have been saved.')
            return redirect('user_dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserUpdateForm(instance=user)  # Load the current user data into the form

    return render(request, 'user/user_dashboard.html', {'form': form})

@login_required
def view_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'view_profile.html', context)

from django.shortcuts import render
from .models import ServiceType, ServiceProvider

# Request_Assistance

from django.shortcuts import render
from .models import ServiceType, ServiceProvider

def request_assistance(request):
    # Fetch all service types
    service_types = ServiceType.objects.all()

    # Fetch all service providers
    service_providers = ServiceProvider.objects.select_related('user', 'service_type').all()

    context = {
        'service_types': service_types,
        'service_providers': service_providers,
    }
    return render(request, 'user/request_assistance.html', context)


from django.shortcuts import render
from .models import ServiceType

def request_assistance(request):
    service_types = ServiceType.objects.all()
    return render(request, 'user/request_assistance.html', {'service_types': service_types})

#showing service_providers_list
from django.shortcuts import render, get_object_or_404
from .models import ServiceType, ServiceProvider

def service_providers_list(request, service_type_id):
    service_type = get_object_or_404(ServiceType, servicetype_id=service_type_id)
    service_providers = ServiceProvider.objects.filter(service_type=service_type)
    return render(request, 'user/service_providers_list.html', {
        'service_type': service_type,
        'service_providers': service_providers
    })

########################################################################################################

#Admin

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserUpdateForm
from .forms import CustomUserUpdateForm as ProfileUpdateForm


@login_required
def view_users(request):
    users = CustomUser.objects.all() 
    return render(request, 'admin/view_users.html', {'users': users})


 # View Profile of admin
def view_profile(request):
    user = request.user
    if user.superuser:  # Custom superuser check
        return render(request, 'admin_dashboard.html', {'user': user})
    else:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

# Update Profile of admin

from django.shortcuts import render, redirect
from .forms import AdminProfileUpdateForm
from .models import CustomUser  # Your custom user model


@login_required
def admin_dashboard(request):
    user = request.user  # Get the current logged-in user (admin)

    context = {
        'user': user,  # Pass the user object to display additional admin info if needed
        'form': AdminProfileUpdateForm(instance=user) 
    }

    return render(request, 'admin/admin_dashboard.html', context)  # Render the dashboard template



from .forms import AdminProfileUpdateForm
@login_required
def admin_profile_update(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        form = AdminProfileUpdateForm(request.POST, instance=user)  # Bind the form to the user instance
        if form.is_valid():
            form.save()  # Save the changes
            messages.success(request, 'Your profile has been updated.')
            return redirect('admin_profile_update')  # Redirect to the dashboard or desired page
    else:
        form = AdminProfileUpdateForm(instance=user)
          # Create a form instance with the user data

    return render(request, 'admin/admin_dashboard.html', {'form': form})

#view users by admin
@login_required
def view_users(request):
    users = CustomUser.objects.all()  # Fetch all users
    return render(request, 'admin/view_users.html', {'users': users})

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import CustomUser

def toggle_active_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        
        status = request.POST.get('status')
        current_table = request.POST.get('current_table')  # Get the current table (users or service providers)
        
        if status == 'deactivate':
            user.is_active = False
        elif status == 'activate':
            user.is_active = True
        user.save()

        # Redirect back to the same page with the correct table
        if current_table == 'users':
            return HttpResponseRedirect('/admin_dashboard?show=users')
        elif current_table == 'service_providers':
            return HttpResponseRedirect('/admin_dashboard? show=service_providers')
    
    return redirect('view_users')  # Fallback if something goes wrong

def service_provider_list(request):
    # Fetch all service providers along with their related service type
    users = CustomUser.objects.prefetch_related('serviceprovider_set__service_type').all()
    print(users)  # Check if users are being fetched

    return render(request, 'service_provider/serviceprovider_dashboard.html', {
        'users': users,
    })

#add service type
from django.shortcuts import render, redirect
from .models import ServiceType
from .forms import ServiceTypeForm
from django.contrib import messages

def manage_service_types(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service type added successfully.')
            return redirect('manage_service_types')
    else:
        form = ServiceTypeForm()
    
    service_types = ServiceType.objects.all()
    return render(request, 'admin/manage_service_types.html', {'form': form, 'service_types': service_types})

from django.shortcuts import render, redirect, get_object_or_404
from .models import ServiceType
from .forms import ServiceTypeForm

def edit_service_type(request, servicetype_id):
    service_type = get_object_or_404(ServiceType, servicetype_id=servicetype_id)
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, request.FILES, instance=service_type)
        if form.is_valid():
            form.save()
    return redirect('manage_service_types')

def delete_service_type(request, servicetype_id):
    service_type = get_object_or_404(ServiceType, servicetype_id=servicetype_id)
    if request.method == 'POST':
        service_type.delete()
        return redirect('manage_service_types')
    return redirect('manage_service_types')





########################################################################################################



# #Service Provider

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from .forms import ServiceProviderUpdateForm
from .models import CustomUser

@login_required
def service_provider_dashboard(request):
    return render(request, 'service_provider/serviceprovider_dashboard.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from .models import ServiceProvider

@login_required
def service_provider_dashboard(request):
    # Get the current logged-in user
    user = request.user  
    
    # Fetch the service provider information if available
    try:
        service_provider = ServiceProvider.objects.select_related('service_type').get(user=user)
    except ServiceProvider.DoesNotExist:
        service_provider = None

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the user profile updates
            
            # Re-fetch the service provider to ensure updated information is shown
            try:
                service_provider = ServiceProvider.objects.select_related('service_type').get(user=user)
            except ServiceProvider.DoesNotExist:
                service_provider = None
    else:
        form = CustomUserUpdateForm(instance=user)
    
    # Pass both the form and service provider information to the template
    return render(request, 'service_provider/serviceprovider_dashboard.html', {
        'form': form,
        'service_provider': service_provider,
    })

#update_profile

@login_required
def update_profile(request):
    user = request.user  # Get the current logged-in user

    # Fetch the service provider information if available
    try:
        service_provider = ServiceProvider.objects.select_related('service_type').get(user=user)
    except ServiceProvider.DoesNotExist:
        service_provider = None

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        
        if form.is_valid():
            print("Form is valid. Saving...")  # Debugging output
            form.save()  # Save the updated user information
            messages.success(request, 'Your changes have been saved.')
            return redirect('service_provider_dashboard')  # Redirect to the dashboard
        else:
            print("Form errors:", form.errors)  # Log errors for debugging
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserUpdateForm(instance=user)  # Load the current user data into the form

    # Pass the form and the service provider information to the template
    return render(request, 'service_provider/serviceprovider_dashboard.html', {
        'form': form,
        'service_provider': service_provider,  # Ensure this is passed
    })
