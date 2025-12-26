from django.contrib import admin

# Register your models here.
# users/admin.py
from django.contrib import admin
from .models import CustomUser, Message, JobPosting, Question, Answer, UserUpvote
from django.contrib.auth.admin import UserAdmin

# Register CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'bio', 'location', 'education']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'location', 'education', 'experience', 'skills')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'location', 'education', 'experience', 'skills')}),
    )

# Register Message model
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'text', 'timestamp']
    search_fields = ['user__username', 'group__name']
    list_filter = ['timestamp']

# Register JobPosting model
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'company', 'location', 'posted_at']
    search_fields = ['title', 'company', 'location']
    list_filter = ['posted_at']

# Register Question model
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['source', 'category', 'question_text', 'created_at']
    search_fields = ['source', 'category', 'question_text']
    list_filter = ['created_at']

# Register Answer model
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'upvotes', 'created_at']
    search_fields = ['question__question_text', 'answer_text']
    list_filter = ['created_at']

# Register UserUpvote model
class UserUpvoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'id']
    search_fields = ['user__username', 'answer__id']
    list_filter = ['user']

# Register all models in admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserUpvote, UserUpvoteAdmin)
