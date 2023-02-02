#TASK 2

The main functionality of the app is that the user can view all the apps and each app has a separate point alloted to it and when the user downloads one of them, he will upload a screen shot of the open app and a task is created and the status will be marked as pending.

The admin sees the task and he verifies the screen shot and he will mark the status as rejected or approved.

When it is approved by admin, the app gets added to the apps in user profile of the user and the user points gets auto updated according to the apps.

admin facing
the admin user can only be added by a super user.
log in (it check whether the user is in sdmin group or not)
log out
get, add, edit and delete - apps
get, add, edit and delete - user profile
get, edit and delete user - tasks
"The admin sees the pending tasks and when he change the status and post it, the app will be auto added to apps in userprofile and the points will also get auto updated."

user facing
sign up (when a user signs up, he will be automatically added to the user group)
log in
log out
get - apps
get - user profile
get, post - tasks
"when a user uploads a scrn shot for particular app, he creates a task in task table with status pending, then it gets verified by the admin user"

'''
#super user credentials
username = nikil
password = nikilprasaath

#admin user credentials
username = nikil1
password = nikilprasaath

username = nikil2
password = nikilprasaath
'''


#TASK 1
#regex

import re
a='{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}'
regex=r"(?<=\:)[\d]+"
a=re.findall(regex,a)
print(a)



#TASK 3
#A 
I would recommend using a task scheduler like Celery, which is a well-established and reliable system for scheduling periodic tasks. 
Celery is capable of handling large scale production and can be easily integrated with various message brokers such as RabbitMQ and Redis for efficient task distribution. 
It also provides features for task management, monitoring, and error handling.

In terms of reliability, Celery has a solid track record and is widely used in production environments. 
However, it's crucial to monitor the task performance and ensure that the underlying message broker is properly configured for optimal performance.

In conclusion, Celery is a reliable and scalable option for scheduling periodic tasks, but proper configuration and monitoring is necessary to ensure its success at scale in production

#B 
Use Flask when you need a lightweight and flexible framework that is easy to set up and get started quickly.
You want full control over the code and implementation details.

Use django when you require a more robust and fully-featured framework for large and complex applications.
You need features such as user authentication and authorization, an ORM, and built-in admin interface out of the box.
You prefer to work with a framework that provides a lot of functionality without the need for additional libraries.