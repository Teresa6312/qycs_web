from django.contrib import admin
from .models import Review, Question, ReviewResponse, QuestionResponse


class ReviewResponseInline(admin.TabularInline):
	model = ReviewResponse
	verbose_name_plural = "Review Response"
	extra = 1

class QuestionResponseInline(admin.TabularInline):
	model = QuestionResponse
	verbose_name_plural = "Question Response"
	extra = 1


class ReviewAdmin(admin.ModelAdmin):
	inlines = (ReviewResponseInline,)
	list_display = ('creater', 'receiver', 'review')

class QuestionAdmin(admin.ModelAdmin):
	inlines = (QuestionResponseInline,)
	list_display = ('creater', 'receiver', 'question')

admin.site.register(Review, ReviewAdmin,)
admin.site.register(Question, QuestionAdmin,)
