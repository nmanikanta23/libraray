from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, BookAllocation, User
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')
        
        # Create new user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, 'register.html')
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.username == 'admin':
                return redirect('librarian_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def librarian_dashboard(request):
    if request.user.username != 'admin':
        return redirect('user_dashboard')
    
    users = User.objects.exclude(username='admin')
    books = Book.objects.all()
    
    if request.method == 'POST':
        # Add new book
        if 'add_book' in request.POST:
            title = request.POST.get('title')
            author = request.POST.get('author')
            quantity = request.POST.get('quantity')
            Book.objects.create(title=title, author=author, quantity=quantity, available=quantity)
        
        # Allocate book to user
        elif 'allocate_book' in request.POST:
            user_id = request.POST.get('user_id')
            book_id = request.POST.get('book_id')
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
            
            if book.available > 0:
                BookAllocation.objects.create(user=user, book=book)
                book.available -= 1
                book.save()
    
    context = {
        'users': users,
        'books': books,
        'allocations': BookAllocation.objects.all()
    }
    return render(request, 'librarian_dashboard.html', context)

@login_required
def user_dashboard(request):
    if request.user.username == 'admin':
        return redirect('librarian_dashboard')
    
    allocations = BookAllocation.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'allocations': allocations})