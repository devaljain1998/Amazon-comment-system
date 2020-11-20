from django import forms

ALGORITHM_CHOICES = (
    ("a",'Choose algorithm (Default :- "Naïve Bayes Text Classification")'),
    ("a", "Naïve Bayes Text Classification"),
    ("b", "Logistic Regression"),
    ("c", "SentiWordNet"),
    ("d", "Random Forest Classifier"),
    ("e", "K Neighbors Classifier")
)

class GetAllLink(forms.Form):
    get_all_links = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ['link']

class LinkForm(forms.Form):
    link = forms.URLField()

    class Meta:
        fields = ['link']

class NumberOfLink(forms.Form):
    number = forms.IntegerField()

    class Meta:
        fields = ['number']

class ChooseAlgorithm(forms.Form):
    algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES)

    class Meta:
        fields = ['algorithm']
