from django import forms


class OpiForm(forms.Form):
    opinion = forms.IntegerField()
