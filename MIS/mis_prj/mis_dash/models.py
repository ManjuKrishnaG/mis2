from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class Field_Creation(models.Model):
    field=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.field

class Title_Creation(models.Model):
    
    title_creation = models.CharField(max_length=255, blank=True)
    field_name = models.ManyToManyField(Field_Creation)
    def __str__(self):
        return f"Data for {self.title_creation}"
 
   

class FormData(models.Model):
    empid=models.CharField(max_length=20)
    firstname= models.CharField(max_length=50)
    form_number= models.IntegerField(default=0)
    title_creation = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255)
    division = models.CharField( max_length=50)
    location= models.CharField(max_length=100)
    date= models.DateField(default=timezone.now)
    edit= models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.firstname} ({self.empid}) - {self.title_creation} - {self.form_number}"
  
 
class Location(models.Model):
    Title_Creation_names = models.ManyToManyField(Title_Creation)
    location = models.CharField(max_length=255)
    Division=models.CharField(max_length=200)
    def __str__(self):
        return f"Settings for {self.location}"
       
class Show(models.Model):
    list= models.ManyToManyField(Title_Creation, through='Disable')
    locations=models.CharField( max_length=50)
    divisions=models.CharField( max_length=50)
    def __str__(self):
        return f"{self.divisions} at ({self.locations})"
    
class Disable(models.Model):
    show = models.ForeignKey('Show', on_delete=models.CASCADE)
    title_creation = models.ForeignKey('Title_Creation', on_delete=models.CASCADE)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return f"Show for {self.disable}"
    
class ApprovalNotification(models.Model):
    refid = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserMas(models.Model):
    s_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    approval_request_raised_by = models.CharField(max_length=255)
    request_status = models.CharField(max_length=255)
    action = models.CharField(max_length=255)


from django.db import models
from django.db import models
from django.db import models

class Attachment(models.Model):
    form_number = models.IntegerField(default=0)
    empid = models.CharField(max_length=30)
    Plan_forthe_Next_Month = models.CharField(max_length=255, default='0')
    remarks = models.CharField(max_length=30)
    attachment = models.FileField(upload_to='attachments/', null=True)
    uploaded_time = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Attachment {self.id} for {self.empid} - {self.uploaded_time.strftime('%Y-%m-%d')}"
 
    def get_icon_url(self):
        file_extension = self.attachment.name.split('.')[-1].lower()
 
        file_icons = {
            'jpg': 'static/icons/ima.jpg',
            'jpeg': 'static/icons/ima.jpg',
            'png': 'static/icons/ima.jpg',
            'pdf': 'static/icons/pdf.jpg',
            'xlsx': 'static/icons/xl.jpg',
            'xls': 'static/icons/xl.jpg',
            'csv': 'static/icons/xl.jpg',
            'doc': 'static/icons/word.png',
            'docx': 'static/icons/word.png',
            'txt': 'static/icons/default.jpg',
            'ppt': 'static/icons/ppt.jpeg',
            'pptx': 'static/icons/ppt.jpeg',
            'zip': 'static/icons/zip.jpg',
            'rar': 'static/icons/rar.jpg',
            'mp3': 'static/icons/audio.jpg',
            'mp4': 'static/icons/video.png',
            'avi': 'static/icons/video.png',
        }
 
        return file_icons.get(file_extension, 'static/icons/default.jpg')
 
    
class Location_Mas(models.Model):
    locationname = models.CharField(max_length=255)
    divisionname = models.CharField(max_length=255)
    
    

    def __str__(self):
        return self.locationname,self.divisionname