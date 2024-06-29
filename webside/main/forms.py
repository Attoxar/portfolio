from django import forms

INTELLIGENCE_OPTIONS = [
    ("port_scan", "Port Scanning"),
    ("web_scan", "Web Vulnerability Scanning"),
    ("dns_lookup", "DNS Lookup"),
    ("traceroute", "Traceroute"),
    ("os_detection", "OS Detection"),
]


class ContactForm(forms.Form):
    username = forms.CharField(label="Your name", max_length=100)
    email = forms.EmailField(label="Your email")
    message = forms.CharField(widget=forms.Textarea, label="Your message")


class TargetForm(forms.Form):
    target = forms.CharField(label="Target", max_length=100)
    # intelligence_option = forms.ChoiceField(
    # choices=INTELLIGENCE_OPTIONS, label="Intelligence Gathering"
    # )
