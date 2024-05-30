
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from datetime import date
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Max, F
def header (request):
    refid = request.session.get('refid')
    user_data = get_user_data(refid)
    refid = request.session.get('refid')

    return ('header.html', {'refid':refid})

def graph(request, month):
    # Fetch data for the selected month from the database
    data = fetch_data_for_month(month)
    titles = Title_Creation.objects.filter(disable=False)  # Assuming you need titles for the dropdown
    context = {
        'month': month,
        'data': data,
        'titles': titles,
    }
    return render(request, 'graph.html', context)

def fetch_data_for_month(month):
    # Convert month name to month number
    month_number = convert_month_to_number(month)
    return FormData.objects.filter(date__month=month_number)

def convert_month_to_number(month):
    month_mapping = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }
    return month_mapping.get(month.lower())

def get_titles():
    # Fetch distinct titles
    return FormData.objects.values_list('title_creation', flat=True).distinct()

def validate_refid(refid):
    with connection.cursor() as cursor:
        # Execute a raw SQL query to check if the refid exists in your MySQL table
        cursor.execute("SELECT COUNT(*) FROM user_mas WHERE refid = %s", [refid])
        # Fetch the result of the query
        row = cursor.fetchone()
        # The result will be a tuple with the count of rows matching the refid
        count = row[0]
        # If count is exactly 1, return True
        return count == 1

def get_user_data(refid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT firstname, lastname, empid, location_name, division_name, defaultuser FROM user_mas WHERE refid = %s", [refid])
        row = cursor.fetchone()
        if row:
            firstname, lastname, empid, location_name, division_name, defaultuser = row
            return {'firstname': firstname, 'lastname': lastname, 'empid': empid, 'location_name':location_name, 'defaultuser':defaultuser, 'division_name':division_name}
        else:
            return None

def delete_data(request):
    
    if request.method == 'POST':
        
        # Delete the data from the database
        # For example, if you want to delete the entry for the current date:
        today = date.today()
        title_creation = request.POST.get('title_creation')
        print(title_creation)
        # FormData.objects.filter(date=today).delete()
        return JsonResponse({'message': 'Data deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def change_edit_field(request):
    if request.method == 'POST':
        # Assuming you are passing 'edit' as a parameter in the POST request
        edit_value = request.POST.get('edit', None)
        # Assuming you have a way to identify the FormData object for which you want to change the 'edit' field
        # Here, I'm assuming you have an emp_id and title_creation to identify the object
        refid = request.session.get('refid')
        user_data = get_user_data(refid)
        emp_id = user_data.get('empid')
        
        # Update the FormData object
        try:
            form_data = FormData.objects.filter(empid=emp_id  )
            for data in form_data:
                data.edit = False
                data.save()
            return JsonResponse({'success': True})
        except FormData.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'FormData object does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
def mis_dashboard(request,refid):
    print(refid)
    user_data = get_user_data(refid)
      
    emp_id = None
    loc = None
    div = None

    if user_data:
        emp_id = user_data.get('empid')
        loc = user_data.get('location_name')
        div = user_data.get('division_name')
        request.session['refid'] = refid


    # Access session data
    
    Locations=Show.objects.filter(locations=loc, divisions= div)
    list_values = []

    for location in Locations:
        titles = location.list.all()  # Retrieve all related Title_Creation objects
        for title in titles:
            list_values.append(title.title_creation)  # Access the specific field of Title_Creation
        
# Removing duplicates if needed
    list_values = list(set(list_values))
    print(list_values)
    location = Location.objects.all()
    tc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
    print(tc)
    # Reverse the order of tc queryset
    tc = reversed(tc)
    today = date.today()
    people_trained_data = FormData.objects.filter(empid = emp_id, date__month=today.month)
    title_field_data = {}
    for title in list_values:
        field_data = FormData.objects.filter(empid=emp_id, date__month=today.month, title_creation=title)
        title_field_data[title] = field_data.values_list('field_name', 'field_value')
    
    if validate_refid(refid):
        user_data = get_user_data(refid)
        for title, fields in title_field_data.items():
            print(f"Title: {title}")
            for field_name, field_value in fields:
                print(f"Field: {field_name}, Value: {field_value}")
        context = {
            'user_data': user_data,
            'refid': refid,
            'emp_id':emp_id,
            'loc':loc,
            'div':div,
            'tc':tc,
            'title_field_data': title_field_data,
            'refid':refid,
            'people_trained_data':people_trained_data
            
        }
        return render(request, 'mis_dashboard.html', context)
    else:
        return HttpResponse("Invalid refid")
    
def calender(request):
    titles = Title_Creation.objects.filter(disable=False)
    refid = request.session.get('refid')

    # form_data = FormData.objects.all()
    context={
        'titles': titles,
        'refid':refid,

        # 'form_data': form_data,
 
    }
    return render(request, 'calender.html', context)

def get_month_data(request, month):
    # Assuming your model has a field named 'date' which is a DateField or DateTimeField
    existing_entry = FormData.objects.filter(date__month=month)
    data_list = list(existing_entry.values('title_creation', 'field_name', 'field_value', 'division', 'location', 'date'))
    print()
    return JsonResponse(data_list, safe=False)

def adminscrn(request):
    location_names = []
    division_names = []
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT locationname, divisionname FROM location_mas")
            rows = cursor.fetchall()

            # Process location names to be distinct
            seen_locations = set()
            for row in rows:
                location_name = row[0]
                if location_name not in seen_locations:
                    location_names.append(location_name)
                    seen_locations.add(location_name)

            # Process division names to be distinct
            seen_divisions = set()
            for row in rows:
                division_name = row[1]
                if division_name not in seen_divisions:
                    division_names.append(division_name)
                    seen_divisions.add(division_name)

            print("Details of records:")
            for row in rows:
                print("Location Name:", row[0])
                print("Division Name:", row[1])

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'adminscrn.html', {'location_names': location_names, 'division_names': division_names})

from django.db.models.functions import TruncMonth

def manage(request):
    refid = request.session.get('refid')
    user_data = get_user_data(refid)
    defaultuser = user_data.get('defaultuser')
    unique_objects=[]
    if  defaultuser == 1:
        unique_objects=[]


            # Get distinct combinations of empid and form_number
        distinct_combinations = FormData.objects.values('empid', 'form_number').distinct()
        print(distinct_combinations, "2222222222222222222222")
        # Loop through the distinct combinations
        for combination in distinct_combinations:
            empid = combination['empid']
            form_number = combination['form_number']

        # Get all objects for the current combination
            object_for_combination = FormData.objects.filter(empid=empid, form_number=form_number).last()

        # Extend the list with objects for the current combination
            if object_for_combination:
                    # Append the object to the list
                    unique_objects.append(object_for_combination)

        context = {
                'employees':unique_objects,
                'defaultuser':defaultuser,
                'refid':refid
            #     'employees_current_month': latest_employees_current_month,
            #     'employees_prev_month': latest_employees_prev_month,
            #     'employees_future_month': latest_employees_future_month
            }
        return render(request, 'manage.html', context)

    else:
        unique_objects=[]
        refid = request.session.get('refid')
        user_data = get_user_data(refid)
        emp_id = user_data.get('empid')
        distinct_combinations = FormData.objects.filter(empid=emp_id).values('form_number').distinct()
        print(distinct_combinations)
        # Loop through the distinct combinations
        for combination in distinct_combinations:
            form_number = combination['form_number']

        # Get all objects for the current combination
            object_for_combination = FormData.objects.filter(empid=emp_id, form_number=form_number).last()

        # Extend the list with objects for the current combination
            if object_for_combination:
                    # Append the object to the list
                    unique_objects.append(object_for_combination)

        context = {
                'employees':unique_objects,
                'refid':refid

            #     'employees_current_month': latest_employees_current_month,
            #     'employees_prev_month': latest_employees_prev_month,
            #     'employees_future_month': latest_employees_future_month
            }
        return render(request, 'manage.html', context)




def people_trained(request):
    refid = request.session.get('refid')
    user_data = get_user_data(refid)
    emp_id = None
    loc = None
    div = None
    # Get all unique objects based on distinct combinations of empid and form_number
    

    if user_data:
        emp_id = user_data.get('empid')
        loc = user_data.get('location_name')
        div = user_data.get('division_name')

    print(div)
    Locations=Show.objects.filter(locations=loc, divisions= div)
    list_values = []
    for location in Locations:
        titles = Title_Creation.objects.filter(disable__show=location, disable__disable=False)
        for title in titles:
            list_values.append(title.title_creation)
# Removing duplicates if needed
    today = date.today()

    list_values = list(set(list_values))
    print(list_values)
    location = Location.objects.all()
    tc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
    dc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
    values = FormData.objects.filter(empid=emp_id, date__month=today.month)
    print(values,'mmmmmmmmmmmmmmmmmmm')
    # Reverse the order of tc queryset
    tc = reversed(tc)
    return render(request, 'people_trained.html', {'refid':refid,'location': location, 'tc': tc,'dc':dc, 'empid':emp_id,'div':div, 'loc':loc,'Locations':Locations, 'values':values})

from django.shortcuts import render
from django.http import HttpResponse
from django.db.utils import IntegrityError
from .models import FormData
from datetime import date

def save_form_data(request):
    try:
        refid = request.session.get('refid')
        user_data = get_user_data(refid)
        emp_id = None
        location = None
        division = None
        form_number= None
        firstname = None
        if user_data:
            emp_id = user_data.get('empid')
            division= user_data.get('division_name')
            location= user_data.get('location_name')
            firstname= user_data.get('firstname')

        today = date.today()
        existing_entry = FormData.objects.filter(date__month=today.month, empid=emp_id).first()
        month_start = today.replace(day=1)

        if request.method == 'POST':
            form_number= request.POST.get('formid')
            if not form_number and FormData.objects.filter(location = location).last() : 
                            form = FormData.objects.filter(location = location).last()
                            form_number = int(form.form_number) + 1
            if not FormData.objects.filter(location = location).last():
                form_number=1
            # Iterate over the keys in request.POST to handle each field individually
            for field_name, field_value in request.POST.items():
                if field_name == 'csrfmiddlewaretoken' or field_name == 'title_creation':
                    continue  # Skip csrfmiddlewaretoken and title_creation fields

                if '_' in field_name:
                    title_creation, field_name = field_name.split('_', 1)
                else:
                    print(f"Skipping invalid field_name: {field_name}")
                    continue

                print("Title Creation:", title_creation)
                print("Field Name:", field_name)
                print("Field Value:", field_value)

                # Check if field_value is not null before saving
                if field_value is not None:
                    # Check if an instance already exists for this empid, title_creation, and field_name
                    form_data, created = FormData.objects.get_or_create(
                        empid=emp_id,
                        title_creation=title_creation,
                        field_name=field_name,
                        division=division,
                        location=location,
                        firstname=firstname,
                        form_number=form_number
                    )

                    # Update or create the form data
                    if not created and existing_entry:
                        # If the instance already exists, update its field_value
                        form_data.field_value = field_value
                        month_start = today.replace(day=1)
                        editable = True if 1 <= today.day <= 5 else False
                        if editable:
                            form_data.save()
                        print("Form Data Updated:", form_data)
                    else:
                        # If the instance does not exist, create it with the given field_value
                        form_data.field_value = field_value
                        
                        form_data.form_number = form_number
                        month_start = today.replace(day=1)
                        editable = True if 1 <= today.day <= 5 else False
                        if editable:
                            form_data.save()
                        print("Form Data Created:", form_data)
                else:
                    print("Field Value is null. Skipping...")

            # You can add any additional logic here
    except IntegrityError as e:
        # Handle the IntegrityError due to duplication
        print("Integrity Error:", e)
        # Add your handling logic here, such as logging the error or informing the user

    return render(request, 'people_trained.html')

def save_data(request):
    if request.method == 'POST':
        title_name = request.POST.get('titleCreation')
        field_name = request.POST.get('fieldCreation')
        division = request.POST.get('division')
        location_name = request.POST.get('location')

        # Create or get Title_Creation instance
        title_creation, created = Title_Creation.objects.get_or_create(title_creation=title_name)

        # Create Field_Creation instance
        field_creation = Field_Creation.objects.create(field=field_name)

        # Add Field_Creation instance to Title_Creation
        title_creation.fields.add(field_creation)

        # Create Location instance
        location = Location.objects.create(location=location_name, Division=division)

        # Add Title_Creation instance to Location
        location.Title_Creation_names.add(title_creation)

        return JsonResponse({'message': 'Data saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
from django.http import JsonResponse
from .models import Title_Creation, Field_Creation

def get_data(request):
    if request.method == 'GET':
        titles = Title_Creation.objects.all()
        fields = Field_Creation.objects.all()
        # divisions = Location.objects.values_list('Division', flat=True).distinct()
        # locations = Location.objects.values_list('location', flat=True).distinct()
        data = {
            'titles': list(titles.values('id', 'title_creation')),  # Adjusted to use 'title_creation' instead of 'title'
            'fields': list(fields.values('id', 'field')),
            # 'divisions': [{'value': division, 'label': division} for division in divisions],
            # 'locations': [{'value': location, 'label': location} for location in locations],
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def disable_data(request):
    if request.method == 'GET':
        titles = Disable.objects.filter(disable=True)
        list1=list(titles.values("title_creation"))
        list2=[]
        for title in list1:
            list2.append(title["title_creation"])
        print(list2)
        # for title in titles:
        disable=Title_Creation.objects.filter(id__in=list2)
        # list1.append(disable)
        print(list1)

        data = {
            'titles': list(disable.values('id', 'title_creation')),
           
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



def enable_data(request):
    print(1)
    try:
        print(1)
        data = json.loads(request.body)
        print(data)
        location = data["locations"]

        division = data["division"]
        title_id = data["fieldId"]
        print(location,division,title_id)

            # Get the Show and Title_Creation objects
        show_object = Show.objects.get(divisions=division,locations=location)
        print(2)
        title_object =Title_Creation.objects.get(id=title_id)
        print(title_object)

        # Get or create the Disable object
        disable_object= Disable.objects.get(show=show_object, title_creation=title_object)

        # Toggle the disable field
        disable_object.disable = not disable_object.disable
        disable_object.save()
        # Confirm the change by re-fetching the object
        disable_object.refresh_from_db()
        # Fetch all enabled titles for the given location and division
        enabled_titles = Title_Creation.objects.filter(
            disable__show__locations=location,
            disable__show__divisions=division,
            disable__disable=False
        ).distinct()

        titles_data = [{'id': title.id, 'title_creation': title.title_creation} for title in enabled_titles]
        return JsonResponse({'status': 'success', 'titles': titles_data, 'disable_status': disable_object.disable})
    except Show.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Show object not found'})
    except Title_Creation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Title_Creation object not found'})
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    
    
import logging

logger = logging.getLogger(__name__)
def update_approval_request(request):
    if request.method == 'POST':
        refid = request.POST.get('refid')
        month = request.POST.get('month')  # Get the selected month
        remarks = request.POST.get('remarks')
        if refid:
            with connection.cursor() as cursor:
                try:
                    # Fetch details from user_mas table where approval status is 1
                    cursor.execute("SELECT * FROM user_mas WHERE approval_st = 1")
                    rows = cursor.fetchall()

                    # Print details to console for each record
                    print("Details of records with approval status 1:")
                    for row in rows:
                        print("Ref ID:", row[0])  # Assuming the first column is refid
                        print("Other details if any:", row[1:])  # Assuming the rest are details

                    # Update approval status for the specific refid
                    sql = "UPDATE user_mas SET approval_st = %s WHERE refid = %s"
                    new_value = True
                    cursor.execute(sql, [new_value, refid])

                    subject = 'Approval Request Updated'
                    message = 'The approval request with refid {} has been updated successfully.'.format(refid)
                    message += f'Selected Month: {month}\n'
                    message += f'Remarks: {remarks}'
                    from_email = 'vandhana.jayakumar1106@gmail.com'  # Update with your email
                    to_email = ['vandhana.jayakumar1106@gmail.com']  # Update with recipient's email
                    send_mail(subject, message, from_email, to_email)

                    ApprovalNotification.objects.create(refid=refid, month=month, remarks=remarks)

                    return JsonResponse({'success': True, 'message': 'Approval request updated successfully'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid refid'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})


def delete_field_values(request):
    if request.method == 'POST':
        print(request.POST)

        title_creation = request.POST.get('title_creation')
        
        if not title_creation:
            return JsonResponse({'error': 'Title creation parameter is missing or empty'}, status=400)

        try:
            # Assuming you have a model named FormData with fields empid and title_creation
            # Delete all field values associated with the given title_creation
            FormData.objects.filter(title_creation=title_creation).delete()
            return JsonResponse({'message': 'Field values deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while deleting field values', 'detail': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import render
from django.utils import timezone
# from .models import Attachment


def editfield(request, empid, form_number):


    
    a = FormData.objects.filter(empid=empid, form_number=form_number).first()
    values = FormData.objects.filter(empid=empid, form_number=form_number).first()
    print(values,'eeeeeeeeeeeeeeeeeeeeeeeee')
    if a:
        loc = None
        div = None

        if a:
            emp_id = a.empid
            loc = a.location
            div = a.division

        print(div)
        Locations=Show.objects.filter(locations=loc, divisions= div)
        list_values = []

        for location in Locations:
            titles = location.list.all()  # Retrieve all related Title_Creation objects
            for title in titles:
                list_values.append(title.title_creation)  # Access the specific field of Title_Creation
            
    # Removing duplicates if needed
        list_values = list(set(list_values))
        print(list_values)
        location = Location.objects.all()
        tc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
        dc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
        values = FormData.objects.filter(empid=emp_id, form_number= form_number)
        print(emp_id)
        print(values)
        # Reverse the order of tc queryset
        tc = reversed(tc)
    else:
        return 'invalid id'
    return render(request, 'showfield.html', {'location': location, 'tc': tc,'dc':dc, 'empid':emp_id,'div':div, 'loc':loc,'Locations':Locations, 'values':values})


def showfield(request, empid, form_number):

    a = FormData.objects.filter(empid=empid, form_number=form_number).first()
    values = FormData.objects.filter(empid=empid, form_number=form_number).first()
    print(values,'eeeeeeeeeeeeeeeeeeeeeeeee')

    if a:
        loc = None
        div = None

        if a:
            emp_id = a.empid
            loc = a.location
            div = a.division

        print(div)
        Locations=Show.objects.filter(locations=loc, divisions= div)
        list_values = []

        for location in Locations:
            titles = location.list.all()  # Retrieve all related Title_Creation objects
            for title in titles:
                list_values.append(title.title_creation)  # Access the specific field of Title_Creation
            
    # Removing duplicates if needed
        list_values = list(set(list_values))
        print(list_values)
        location = Location.objects.all()
        tc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
        dc = Title_Creation.objects.filter(title_creation__in=list_values).order_by('-id')  # Reverse order by 'id' or any other suitable field
        values = FormData.objects.filter(empid=emp_id, form_number= form_number)
        print(emp_id)
        print(values)
        # Reverse the order of tc queryset
        tc = reversed(tc)
    else:
        return 'invalid id'
    return render(request, 'editfield.html', {'location': location, 'tc': tc,'dc':dc, 'empid':emp_id,'div':div, 'loc':loc,'Locations':Locations, 'values':values})

from django.shortcuts import render
from django.utils import timezone
from .models import Attachment

def upload_files(request):
    refid = request.session.get('refid')
    user_data = get_user_data(refid)
    emp_id = user_data.get('empid')
    success_message = None
    location= user_data.get('location')
    form_number= request.POST['formid']


    if request.method == 'POST':
        plan_for_next_month = request.POST.get('plan_for_next_month', '')  # Get the value from the text field
        today = timezone.now()
        
        # Iterate over each file and its associated remark
        for file in request.FILES.getlist('attachment'):
            if not form_number and FormData.objects.filter(location = location).last() : 
                            form = FormData.objects.filter(location = location).last()
                            form_number = form.form_number + 1
            if not FormData.objects.filter(location = location).last():
                form_number=1
            remark = request.POST.get(f'remarks_{file.name}', '')  # Assuming input name is 'remarks_{file.name}'
            Attachment.objects.create(
                empid=emp_id,
                Plan_forthe_Next_Month=plan_for_next_month,
                remarks=remark,
                attachment=file,
                uploaded_time=today,
                form_number= form_number
            )
        saved_data = Attachment.objects.filter(empid=emp_id, form_number = form_number)

        success_message = "Files uploaded successfully"

    return render(request, 'people_trained.html', {'success_message': success_message, 'saved_data': saved_data})

from django.http import JsonResponse

def delete_attachment(request, attachment_id):
    if request.method == 'POST':
        attachment = get_object_or_404(Attachment, id=attachment_id)
        attachment.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def save_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empid = data.get('empid')
            title_creation_name = data.get('title_creation')
            field_name = data.get('field_name')
            field_value = data.get('field_value')
            division = data.get('division')
            location = data.get('location')

            # Ensure that required fields are provided
            if not (empid and title_creation_name and field_name and division and location):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
            title, _ = Title_Creation.objects.get_or_create(title_creation=title_creation_name)
            print(field_value)
            for fieldSub in field_name:
                field, _ = Field_Creation.objects.get_or_create(field=fieldSub)
                if field not in title.field_name.all():
                    title.field_name.add(field)
                    title.save()

            

            new_form_data, created = FormData.objects.get_or_create(
                empid=empid,
                title_creation=title_creation_name,
                field_name=field_name,
                field_value=field_value,
                division=division,
                location=location,
                date=timezone.now()
            )

            show, show_created = Show.objects.get_or_create(divisions=division, locations=location)
            if title not in show.list.all():
                show.list.add(title)
                show.save()

            show_data = {
                'id': show.id,
                'divisions': show.divisions,
                'locations': show.locations,
                'titles': list(show.list.values('id', 'title_creation'))
            }

            return JsonResponse({'status': 'success', 'message': 'Field created successfully', 'show': show_data})

        except Exception as e:
            # Log the exception
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {e}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def dis(request):
    title_creation_instance = get_object_or_404(Title_Creation, pk=1)  # Adjust the pk value as needed
    context = {
        'disable': title_creation_instance.disable,
        'division_names': ['Division 1', 'Division 2', 'Division 3'],  # Example divisions
        'location_names': ['Location 1', 'Location 2', 'Location 3'],  # Example locations
    }
    return render(request, 'adminscrn.html', context)
def get_locations(request):
    selected_division = request.GET.get('division')  # Assuming the division is passed as a GET parameter

    # Query locations based on the selected division
    if selected_division:
        locations = Location_Mas.objects.filter(divisionname=selected_division).values_list('locationname', flat=True)
        return JsonResponse({'locations': list(locations)})

    # Handle if no division is selected
    return JsonResponse({'error': 'No division selected'}, status=400)

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Attachment
 
@csrf_exempt
def render_people_trained(request):
    if request.method == 'POST':
        refid = request.session.get('refid')
        user_data = get_user_data(refid)
        emp_id = user_data.get('empid')
        location = user_data.get('location')
        form_number = request.POST.get('formid')
       
        plan_for_next_month = request.POST.get('plan_for_next_month', '')  
        today = timezone.now()
       
        for file in request.FILES.getlist('attachment'):
            file_name = file.name
            remark = request.POST.get(f'remarks_{file_name}', '')  # Extract remark for each file
            Attachment.objects.create(
                empid=emp_id,
                Plan_forthe_Next_Month=plan_for_next_month,
                remarks=remark,  # Save the remark along with the attachment
                attachment=file,
                uploaded_time=today,
                form_number=form_number
            )
       
        cache.delete('uploaded_files')
       
        saved_data = Attachment.objects.filter(empid=emp_id, form_number=form_number)  
       
        success_message = "Files uploaded successfully"
 
        return render(request, 'people_trained.html', {'success_message': success_message, 'saved_data': saved_data})
   
    elif request.method == 'GET':
        refid = request.session.get('refid')
        user_data = get_user_data(refid)
        emp_id = user_data.get('empid')
       
        saved_data = Attachment.objects.filter(empid=emp_id)
       
        files_data = [{
            'id': file.id,
            'fileName': file.attachment.name,
            'remarks': file.remarks,
            'iconUrl': file.get_icon_url()
        } for file in saved_data]
       
        return JsonResponse(files_data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Attachment
 
@csrf_exempt
def delete_attachment(request, attachment_id):
    if request.method == 'POST':
        attachment = get_object_or_404(Attachment, id=attachment_id)
        attachment.delete()  # Delete the attachment from the database
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
 