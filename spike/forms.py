from django import forms


class PostForm(forms.Form):
    drug_name = forms.CharField(widget=forms.Textarea)
    start_date = forms.CharField(widget=forms.Textarea)
    end_date = forms.CharField(widget=forms.Textarea)
