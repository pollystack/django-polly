from django.contrib import admin
from .models import Parrot, Trick, Message, SmartConversation
from django import forms


# Define a custom form for Parrot model
class ParrotAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Parrot
        fields = '__all__'


# Inlines
class TrickInline(admin.TabularInline):
    model = Trick  # Assuming you have a Trick model related to Parrot


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("party", "content", "created_at", "updated_at")
    ordering = ("created_at",)


@admin.register(Parrot)
class ParrotAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'age', 'external_id', 'created_at', 'updated_at')
    list_filter = ('color', 'created_at', 'updated_at')
    search_fields = ('name', 'external_id')
    inlines = [TrickInline]
    actions = ['make_colorful']
    form = ParrotAdminForm

    @admin.action(description="Make selected parrots colorful")
    def make_colorful(self, request, queryset):
        queryset.update(color='Rainbow')
        self.message_user(request, f"{queryset.count()} parrots were made colorful.")


@admin.register(Trick)
class TrickAdmin(admin.ModelAdmin):
    list_display = ('name', 'parrot', 'difficulty', 'external_id', 'created_at', 'updated_at')
    list_filter = ('difficulty', 'created_at', 'updated_at')
    search_fields = ('name', 'parrot__name', 'external_id')


@admin.register(SmartConversation)
class SmartConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at", "updated_at")
    list_filter = ("user", "created_at", "updated_at")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    raw_id_fields = ("user",)
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "party",
        "content",
        "created_at",
        "updated_at",
    )
    list_filter = ("conversation", "party", "created_at", "updated_at")
    search_fields = ("content",)
    date_hierarchy = "created_at"
    raw_id_fields = ("conversation",)
