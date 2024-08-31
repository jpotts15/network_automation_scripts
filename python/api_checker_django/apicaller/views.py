# apicaller/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ApiForm
from .api import call_api

def api_view(request):
    if request.method == 'POST':
        form = ApiForm(request.POST)
        if form.is_valid():
            api_url = form.cleaned_data['api_url']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            response = call_api(api_url, username, password)
            
            if response.ok:
                result = response.json()
            else:
                result = f"Error: {response.status_code} - {response.text}"
            
            return render(request, 'apicaller/result.html', {'result': result})
    else:
        form = ApiForm()
    
    return render(request, 'apicaller/form.html', {'form': form})
