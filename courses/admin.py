from django.contrib import admin

from .models import Course, Sector, Episode, CourseSection, Comment, Cart

admin.site.register(Course)
admin.site.register(Sector)
admin.site.register(Episode)
admin.site.register(CourseSection)
admin.site.register(Comment)
admin.site.register(Cart)