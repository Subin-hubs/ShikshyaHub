import os

# This tells the computer to create the structure for ShikshyaHub
folders = ['app/routes', 'app/templates/auth', 'app/templates/student', 
           'app/templates/teacher', 'app/templates/admin', 'app/templates/public', 
           'app/templates/includes', 'app/static/css', 'app/static/js', 
           'app/static/uploads/assignments', 'app/utils']

files = ['.env', 'config.py', 'run.py', 'requirements.txt', 'app/__init__.py', 
         'app/models.py', 'app/forms.py', 'app/routes/auth.py', 'app/routes/main.py']

for f in folders: os.makedirs(f, exist_ok=True)
for f in files: open(f, 'a').close()

print("Project structure created!")