from django import forms


class SearchForm(forms.Form):
    """Search form"""

    search = forms.CharField(
        label='Поиск по логам:',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
