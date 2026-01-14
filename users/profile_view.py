@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'users/profile.html')