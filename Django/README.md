# Django

**Django**: this is a Python web framework which allows us to build a dynamic web application.

**Dynamic web**: this is a website that can respond based on how users are interacting with  it.

**Applications**: Django project consists of one or more Django applications.
- Why?
    - A big Website or a big Project has multiple different apps that are sort of seperate services that operate in it.
- Example
    - Google has
        - Google search
        - Google image
        - Google maps
        - Google scholar

**Key idea**: Web is in terms of requests and responses
- User makes a request to get a particular web page.
- Process the request.
- User gets back is a response.

**Validation**
- Client-side validation: Check on the client to make sure that clients input the valid data. The sever isn't getting any of this data.
- Server-side validation: Check on the server to make sure that inputs are valid
    - Why?
        - It's very easy to disable the client-side validation.

- Both ```client-side validation``` and ```server-side validation`` are necessary to make sure that the data is going to be accurate, clean and meet the predetermined specifications.

## HTTP

**HTTP (HyperText Transfer Protocol)**: this is the protocol for how messages are going to be sent back and forth over the internet.

### Request

```
GET / HTTP/1.1
Host: www.example.com
...
```
- ```GET``` is just a example of request method, a way you might try to get a page.
- Slash ```/``` just denotes the root of the website, usually the default page for the website.
- ```HTTP 1-1``` is the using version of HTTP.
- ```Host``` is what URL that we're trying to access the web page for. 

Request gets sent by the web browser when typing the URL and pressing Return, for example.

**Methods of request**:
- ```get```: Get a particular page.
- ```post```: Be used for submitting form data. ```Post``` method gives us the ability to send data to the route in order to  get some sort of results.

### Response

```
HTTP/1.1 200 OK
Content-Type: text/html
...
```
- ```Response``` code in this case is ```200``` which means ```OK```.
- ```Content-Type``` means the format of the data that's coming back in this reponse is ```HTML``` data.

**HTTP Status Codes**:
- 200: OK.
- 301: Moved Permanetly.
- 403: Forbidden.
- 404: Not Found.
- 500: Internal Server Error.

## Django
### Installation

```shell
pip3 install Django
```
### Create new Django project
```shell
django-admin startproject PROJECT_NAME
```
When executing this command, Django is automatically going to create some starter files.

### Run server

```shell
python manage.py runserver
```

### Importation files
- ```manage.py``` is going to be used for executing commands on this Django project (No need to touch this file in generally)

    ```shell
    python manage COMMAND
    ```

- ```settings.py``` contains important configurations settings for Django application.

- ```urls.py``` is going to be a table of contents of all of URLs on web application that you can ultimately visit. The ```urls.py``` of the project is the master urls file that might connect to the multiple different URL configurations.

- ```views.py``` is going to describe  what it is user sees when they visit a particular route.

## Django Application

```Django Application``` can be reused in various different ```Django Project```

1. Create new Django app

    ```shell
    python manage.py starapp APP_NAME
    ```

2. Add the new app to the particular Django project
Navigate to ```setttings.py``` of the the particular project and add the name of app to the ```INSTALLED_APPS``

3. Define the ```view``` of the app

    ```python
    def index(request):
        return HttpResponse("Hello, world!")
    
    # Parameterize this function to be more flexible.
    def greet(request, name):
        return HttpResponse(f'Hello, {name}')
    
    # To separate the HTML reponse from the actual Python code 
    def index(request):
        return render(request, 'hello/index.html')
    
    # To render a HTML template with variable
    def greet(request, name):
        return render(request, 'hello/greet.html', {
            'name': name
        })
    ```
    - request: a HTTP request that the user made in order to access the web server.
    - HttpResponse: a HTTP response that be sent back to the user.
    - render: to render an entire HTML template file with the specific template name.
        - Parameters:
            - request: Http request.
            - HTML template: the template that will be rendered.
            - context: the context is all of the information that would be provided to the template.
        - Why?
            - Separate the HTML reponse from the actual Python code.
            - To ensure the collaboration of different people: one person can work on Python logic and one person can work on the HTML. So, they doesn't step on each other's toe.

    To call the view defined in above, we need to map it to a URL (create the own route) configured in ```urls.py``` (need to create it in an app folder)
    - Example of non-parameterized path
        ```python
        path('giang', views.giang, name='giang')
        ```
    - Example of parameterize the path
        ```python
            path('<str:name>', views.greet, name='greet')
        ```
        Instead of prescribing exactly what URL should look like (```127.0.0.1/hello/Giang```) in case of non-parameterized path, you can give any string, any custom route (```127.0.0.1/hello/Wall``` or ```127.0.0.1/hello/Bach```) that could be passed to the variable of ```name```.
    
    Link the project URL to app URL by adding the defined routes in ```urls.py``` in the project folder
    ```python
    path('hello/', include('hello.urls'))
    # include all of the URLs from the urls in hello application.
    ```

    **Note**: You can have as many views function as you want, but you need to associate it to the specific url.

## Django session
Django session:
 - Has a ability to rememeber who you are, such that on subsequent visits, it remembers who you are and khows who you are.
- Be able to store data about your particular session. It's able to store your user ID or information about you.
- How to use:
    - ```request.session```: The dictionary of representing all the data we have on file inside the session about the user.
    - ```migrate```: By default, Django stores session data inside of a table, you can change the place saving session data. If these tables doesn't exist, we need to create it by run ```mirgrate``` command.
## HTML templates
    
These HTML templates can be parameterizale by using Django. If use HTML out of the box, you can't parameterize because HTML is a markup languages, not so much a programming languae, which means it doesn't support for variable by default.

Django have the ability to take an HTML page and treat it like a template that can be rendered. Django added its own templating language. So, we can take advantages of that to be able to render and HTML page that actually has variable, loop or condition inside of it.

Django treats HTML file as a dynamic file because of its changes using Django templating laguage with variable, loop, condition to adapt with the behaviors needed.

```html
<!--Double curly braces are part of the Django templating language allowing to plug in the value of the variable into this place-->
<h1> Hello, {{ name }}! </h1>
```

Example of condition inside of Django template
```html
{% if newyear %}
    <h1>Happy New Year </h1>
{% else %}
    <h1>Nope. It's a normal day </h1>
{% endif %}
```

**Template inheritance**: this a way of getting rid of the repetitive code blocks through many different HTML files using Django templating language.

- Why?
    - Factor out the common code to be helpful for good desgin.
    -  Reduce the repetition.
    - Only make the changes inside of the layout file instead of modifying dozens of hundreds of different places.

- Define the layout
```html
<!DOCTYPE html>
<html lang='en'>
    <head>
        <title>Tasks</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html
```


- Use the predefined layout
```html
    <!--The top of html file-->
    {% extends tasks/layout.html %}
    {% block body %}
        <h1> Template inheritance </h1>
    {% endblock %} 
```

**Use URL name**: Instead of prescribing exactly what a hardcoding URL is, I'm just say it is a url having the specified name. Django has the additional feature to figure out what URL should be.

```html
<a href="{% url 'name' %}"> Add a new Task</a>
```

- Fix the url namespace collision where two urls have the same name that makes Django confused to choose which one

```python
# Specify the app_name in each urls.py
app_name = 'tasks'
```

```html
<!--Get particular url from the particular application name which is 'tasks' in this case-->
<a href="{% url 'tasks:name' %}"> Add a new Task</a>
```
- Avoid to not hardcode URLs

```python
# Hardcode URLs
return HttpResponseRedicrect(reverse("task/index.html"))
# Better design with Django
# reverse is to figure out what the particular route is actully from.
return HttpResponseRedicrect(reverse("task:index"))
```


## CSS
Django treats CSS file as a static file because it's unchange.

Command of loading static files for this particular HTML page.
```html
<!--In a particular HTML file-->
{% load static %}

<!DOCTYPE  html>
<html lang='end'>
    <head>
        <title>Hello</title>
        <link href="{% static 'newyear/styles.css' %}">
    </head>
</html>
```
- Instead of prescribing exactly what a hardcoding URL is, I'm just saying it is a static file that is inside of a newyear folder called styles.css. Django is going to figure out what URL outght to be.




