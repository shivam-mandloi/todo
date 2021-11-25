from mongoengine import connect,document,StringField,IntField,EmailField
connect(db='ToDo',
            host="localhost"
            )

class Otp(document.DynamicDocument):
    email=EmailField()
    otp=StringField()
    time=StringField()
    def to_json(self):
        return{
            "id":self.id,
            "email":self.email,
            "otp":self.otp,
            "time":self.time
        }

class Tasks(document.DynamicDocument):
    title=StringField()
    message=StringField()
    time = StringField()
    complete=IntField()
    def to_json(self):
        return {
            "id":self.id,
            "message":self.message,
            "date":self.date,
            "time":self.time,
            "complete":self.complete
        }

class User(document.DynamicDocument):
    name = StringField()
    email = EmailField()
    password = StringField()
    def to_json(self):
        return{
        "name":self.name,
        "email":self.email,
        "password":self.password
        }

collection_task = Tasks()
collection_task.title = "first todo"
collection_task.message = "This is for test."
collection_task.date = "20 nov 2021 9:08pm"
collection_task.complete = 1
collection_task.save()
task_id = collection_task.id

collection_otp = Otp()
collection_otp.email = "shivammandloi1102@gmail.com"
collection_otp.otp = "12345"
collection_otp.time = "20 nov 2021 9:08pm"
collection_otp.save()
task_id = collection_otp.id

collection_user = User()
collection_user.name = "shivam"
collection_user.email = "shivammandloi1102@gmail.com"
collection_user.password = "shivam101"
collection_user.save()
task_id = collection_user.id