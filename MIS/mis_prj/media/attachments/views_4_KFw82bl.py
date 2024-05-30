from django.shortcuts import render,redirect
from .models import PeopleTrained,TrainedPeople
from .forms import PeopleTrainedForm, ManhoursForm,EmployeeDataForm

def mis_dashboard(request):
    people_trained_data = PeopleTrained.objects.all()
    context = {
        'people_trained_data': people_trained_data
    }
    return render(request,'mis_dashboard.html',context)

def employee_data(request):
    if request.method == 'POST':
        form =EmployeeDataForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the data to the database
            return redirect('mis_dashboard')  # Redirect to a success page
    else:
        form = EmployeeDataForm()
    return render(request, 'employee_data.html', {'form': form})

def mis_edit_2(request):
    return render (request,"mis_edit_2.html")
def mis_header(request):
    return render(request,"header.html")

def people_trained(request):
    if request.method == 'POST':
        form = PeopleTrainedForm(request.POST)
        if form.is_valid():
            trained_people = form.save(commit=False)
            trained_people.form_name = 'people_trained'  # Set the form_name value
            trained_people.save()
            return redirect('manhours')  # Redirect to success page after saving
    else:
        form = PeopleTrainedForm()
    
    return render(request, 'people_trained.html', {'form': form})

def manhours(request):
    if request.method == 'POST':
        form = ManhoursForm(request.POST)
        if form.is_valid():
            trained_people = form.save(commit=False)
            trained_people.form_name = 'manhours'  # Set the form_name value
            trained_people.save()
            return redirect('mis_dashboard')  # Redirect to success page after saving
    else:
        form = ManhoursForm()
    
    return render(request, 'manhours.html', {'form': form})


def number_of_training_sessions(request):
    return render(request, 'number_of_training_sessions.html')

def no_of_safety_alert_card(request):
    return render(request, 'no_of_safety_alert_card.html')

def near_miss(request):
    return render (request, 'near_miss.html')

def safety_alert_card(request):
    return render(request, 'safety_alert_card.html')

def incidents(request):
    return render(request, 'incidents.html')

def road_related_incidents(request):
    return render(request, 'road_related_incidents.html')

def no_of_safety_inspections(request):
    return render(request, 'no_of_safety_inspections.html')

def no_of_observations_for_the_month(request):
    return render(request, 'no_of_observations_for_the_month.html')

def no_of_observations_by_walkthrough(request):
    return render(request, 'no_of_observations_by_walkthrough.html')

def total_no_of_observations_ytd(request):
    return render(request, 'total_no_of_observations_ytd.html')

def total_no_of_observations_actiontaken_ytd(request):
    return render(request, 'total_no_of_observations_actiontaken_ytd.html')

def total_no_of_observations_pending_ytd(request):
    return render(request, 'total_no_of_observations_pending_ytd.html')

def work_permit_issued(request):
    return render(request, 'work_permit_issued.html')

def no_of_moc_approved_and_issued(request):
    return render(request, 'no_of_moc_approved_and_issued.html')

def no_of_eventmp_approved_and_issued(request):
    return render(request, 'no_of_eventmp_approved_and_issued.html')

def man_power_strength(request):
    return render(request, 'man_power_strength.html')