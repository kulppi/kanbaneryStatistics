# request_time_data.py

import requests
api_token = ""
project_id = ""

users_url = "https://iic215420141.kanbanery.com/api/v1/projects/"+project_id+"/users.json?api_token="+api_token
tasks_url = "https://iic215420141.kanbanery.com/api/v1/projects/"+project_id+"/tasks.json?api_token="+api_token
tasks_archive_url = "https://iic215420141.kanbanery.com/api/v1/projects/"+project_id+"/archive/tasks.json?api_token="+api_token
estimates_url = "https://iic215420141.kanbanery.com/api/v1/projects/"+project_id+"/estimates.json?api_token="+api_token
task_types_url = "https://iic215420141.kanbanery.com/api/v1/projects/"+project_id+"/task_types.json?api_token="+api_token


users_req = requests.get(users_url)
users_json = users_req.json()
tasks_req = requests.get(tasks_url)
tasks_json = tasks_req.json()
tasks_archive_req = requests.get(tasks_archive_url)
tasks_archive_json = tasks_archive_req.json()
estimates_req = requests.get(estimates_url)
estimates_json = estimates_req.json()
task_types_req = requests.get(task_types_url)
task_types_json = task_types_req.json()

users = {}
for x in users_json:
    users[x["id"]] = {"email": x["email"], "name": x["name"], "id": x["id"], "time": {"h": 0, "m": 0}, "estimate": {"h": 0, "m": 0}}

estimates = {}
for x in estimates_json:
    estimates[x["id"]] = {"id": x["id"], "value": x["value"]}

task_types = {}
for x in task_types_json:
    task_types[x["id"]] = {"id": x["id"], "name": x["name"], "time": {"h": 0, "m": 0}}

def get_time_for_task(task):
    title = task["title"]
    v = title.find("$")
    if (v != -1):
        v += 1
        p = title.find(":",v)
        return {"h": int(title[v:p]) , "m": int(title[p+1:p+3])}
    return {"h": 0 , "m": 0}

def get_estimate_time_for_task(task, estimates):
    estimate_id = task["estimate_id"]
    if estimate_id != None:
        estimate_value = estimates[estimate_id]["value"]
        if estimate_value < 1:
            return {"h": 0, "m": estimate_value*60}
        else:
            return {"h": estimate_value, "m": 0}
    else:
        return {"h": 0, "m": 0}

def add_times(a, b):
    c = {"h": 0 , "m": 0}
    c["m"] = a["m"] + b["m"]
    c["h"] = a["h"] + b["h"]
    if (c["m"] >= 60):
        c["m"] -= 60
        c["h"] += 1
    return c

def is_common_task(task):
    return task["title"].find("@$") != -1

def print_html (users, title):
    array_t =  ""
    for x in users:
        array_t += ("['%s', %f, %f],\n" % (users[x]["email"],
            users[x]["time"]["h"]+ users[x]["time"]["m"]/60,
            users[x]["estimate"]["h"]+ users[x]["estimate"]["m"]/60))
    print(array_t[:-2])
    
    template = """
    <html>
      <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(drawChart);
    function drawChart() {

      var data = google.visualization.arrayToDataTable([
        ['Mail', 'Time', 'Estimate Time'],
    """
    template += array_t[:-2]    
    template += """
      ]);

      var options = {
    """
    template += "title: 'Team Performance - %s'," % title  
    template += """
        hAxis: {title: 'Members', titleTextStyle: {color: 'red'}}
      };

      var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));

      chart.draw(data, options);

    }
        </script>
      </head>
      <body>
        <div id="chart_div" style="width: 900px; height: 500px;"></div>
      </body>
    </html>
    """
    # Open a file
    name = "gchart" + title + ".html"
    fo = open(name, "wb")
    fo.write( template);
    # Close opend file
    fo.close()


for x in tasks_json:
    t = get_time_for_task(x)
    e_t = get_estimate_time_for_task(x, estimates)
    task_types[x["task_type_id"]]["time"] = add_times(task_types[x["task_type_id"]]["time"], t)
    if is_common_task(x):
        for u_id in users:
            users[u_id]["time"] = add_times(users[u_id]["time"], t)
            users[u_id]["estimate"] = add_times(users[u_id]["estimate"], e_t)
    else:
        if x["owner_id"] != None:
            users[x["owner_id"]]["time"] = add_times(users[x["owner_id"]]["time"], t)
            users[x["owner_id"]]["estimate"] = add_times(users[x["owner_id"]]["estimate"], e_t)

import pickle
import os
import time

users_time_filename ="users_time.pickle"
if os.path.exists(os.getcwd()+users_time_filename):
    users_time = pickle.load(open(users_time_filename, 'r'))
else:
    users_time = {}

users_time[time.strftime("%x")] = users
pickle.dump(users_time, open(users_time_filename, 'w'))
print("Tasks unarchived :")
print("Email, Name, Time, Estimate Time")
for x in users:
    print("%s, %s, %i:%i, %i:%i" % (users[x]["email"], users[x]["name"],
        users[x]["time"]["h"], users[x]["time"]["m"],
        users[x]["estimate"]["h"], users[x]["estimate"]["m"]))

print("Task type, Time")
for x in task_types:
    print("%s, %i:%i" % (task_types[x]["name"], task_types[x]["time"]["h"],
        task_types[x]["time"]["m"]))
# print_html(users, "Tasks unarchived")


# total task, add archived
print("\n with tasks archived :")
for x in tasks_archive_json:
    t = get_time_for_task(x)
    e_t = get_estimate_time_for_task(x, estimates)
    task_types[x["task_type_id"]]["time"] = add_times(task_types[x["task_type_id"]]["time"], t)
    if is_common_task(x):
        for u_id in users:
            users[u_id]["time"] = add_times(users[u_id]["time"], t)
            users[u_id]["estimate"] = add_times(users[u_id]["estimate"], e_t)
    else:
        if x["owner_id"] != None:
            users[x["owner_id"]]["time"] = add_times(users[x["owner_id"]]["time"], t)
            users[x["owner_id"]]["estimate"] = add_times(users[x["owner_id"]]["estimate"], e_t)

print("Email, Name, Time, Estimate Time")
for x in users:
    print("%s, %s, %i:%i, %i:%i" % (users[x]["email"], users[x]["name"],
        users[x]["time"]["h"], users[x]["time"]["m"],
        users[x]["estimate"]["h"], users[x]["estimate"]["m"]))

print("Task type, Time")
for x in task_types:
    print("%s, %i:%i" % (task_types[x]["name"], task_types[x]["time"]["h"],
        task_types[x]["time"]["m"]))

print_html(users, "with tasks archived")

