from django import forms

class InputField(forms.Form):
    text = forms.CharField(label='Text', max_length="200")
    is_corr = forms.BooleanField(label='Is this hateful?', required=False)

class TrainConfirm(forms.Form):
    is_conf = forms.BooleanField(label="Train model now?",initial=False, required=False)
