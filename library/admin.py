from django.contrib import admin
from .models import Book, BookAllocation
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

def create_librarian():
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@library.com', 'admin')
    except:
        pass  # Ignore errors during initial setup

# Safe way to ensure librarian exists after migrations
create_librarian()

admin.site.register(Book)
admin.site.register(BookAllocation)



'''
from django.contrib import admin
from .models import Book, BookAllocation
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Book)
admin.site.register(BookAllocation)
'''