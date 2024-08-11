from django.contrib import admin
from .models import Parrot, Trick
from django import forms


# Define a custom form for Parrot model
class ParrotAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Parrot
        fields = '__all__'


class TrickInline(admin.TabularInline):
    model = Trick  # Assuming you have a Trick model related to Parrot


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
