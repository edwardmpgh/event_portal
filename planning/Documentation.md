#Create a New Event Form

1. Get requirements for the event attendees
2. Determine if fields need to be added to the Attendee model or if a new model needs to be created
3. Create a new form in Event -> Forms.py
3.1. push to git
3.2. Log into the server and pull form git
4. Add new form to the EventForm table using the /admin site
5. Add the new form the to form_list dict located at the top of events -> views.py
6. For the event, select the new event form.

#Refresh Code from Code Commit
1. ssh heinz@heinz-notwas.heinz.cmu.edu
2. cd /webapps/heinz_signup
3. sudo su - webappuser
4. git pull origin master
5. exit

# Server Setup

Server: heinz-notwas.heinz.cmu.edu
User: Heinz

Application Linux Account: webappuser
Application Linux Group: webapps

Log files for nginx and uwsgi: /webapps/heinz_signup/log

Source location: /webapps/heinz_signup
uWsgi Conf file: /webapps/heinz_signup/conf/
uWsgi systemd conf file: /etc/systemd/system/uwsgi.service

Setup: Nginx and uWsgi

Restart: 
sudo systemctl restart nginx.service uwsgi.service  

#Panels
Management Panel: https://event.heinz.cmu.edu/manage
Admin Panel: https://event.heinz.cmu.edu/admin
 