from django.shortcuts import render
from .catch import *

# Create your views here.
def index(request):
    if request.method == "POST":
        value = request.POST['value']

    else:
        value = "未輸入取樣數值"
    return render(request,'internet/index.html',locals())




