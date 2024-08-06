from django.contrib import admin
from .models import Parrot, Trick
from django import forms


class ParrotAdminForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Parrot
        fields = '__all__'


class TrickInline(admin.TabularInline):
    model = Trick  # Assuming you have a Trick model related to Parrot


@admin.register(Parrot)
class ParrotAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'age')
    list_filter = ('color',)
    search_fields = ('name',)
    actions = ['make_colorful']
    form = ParrotAdminForm

    @admin.action(description="Make selected parrots colorful")
    def make_colorful(self, request, queryset):
        queryset.update(color='Rainbow')
        self.message_user(request, f"{queryset.count()} parrots were made colorful.")
