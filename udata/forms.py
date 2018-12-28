from django import forms


class FetchDataForm(forms.Form):
    what = forms.CharField(max_length=256, required=False)
    where = forms.CharField(max_length=256, required=False)

    class Meta:
        fields = ('what', 'where')

    def clean(self):
        cd = self.cleaned_data
        if cd.get('what') is None:
            self.add_error('what', "You need to pass at least one query in what field.")
        return cd