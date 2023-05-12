from django.shortcuts import render, redirect
from .models import Hate_Model
from .forms import InputField, TrainConfirm
from .scripts.predictor import prediction
from .scripts.display import displayer
from .scripts.data_train import train_it


def thanks(request):
    return render(request, 'core/thanks.html', {"output": displayer(o)})

def index(request):

    if request.method == "POST":
        form = InputField(request.POST)
        if form.is_valid():
            n = form.cleaned_data['text']
            m = form.cleaned_data['is_corr']
            global o 
            o = prediction(n)
    
            t = Hate_Model(text = n, hate = m)
            t.save()

            print(n)
            print(m)
            print("done")
            return redirect('/thanks/')
            

            
    else:
        form = InputField()
    return render(request, 'core/index.html', {"form":form})

def empty(request):
    if request.method=='POST':
        conf = TrainConfirm(request.POST)
        if conf.is_valid():

            global o 
            o = conf.cleaned_data['is_conf']
            print(o)

            if o:
                data = []
                for x in Hate_Model.objects.all():
                    buffer = [x.text, x.hate]
                    data.append(buffer)

                print(data)

                train_it(data)

                Hate_Model.objects.all().delete()
            
            return redirect('/thanks/')
            
    else:
        conf = TrainConfirm()

    return render(request, 'core/empty.html', {"form": conf})

