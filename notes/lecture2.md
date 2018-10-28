# Lecture 2

- A server is just a computer:
    - Each server has a **host**
    - Open **ports** (1024-65535)
    - centralize information 
    

- How do we talk to servers?
    - Server-Client Model
        - ex: http://google.com
        - Request is sent over Hyper Text Protocol = port 80
        - Examples:
        - https = port 443
        - ssh = port 22
        - ftp = port 20/21 (filezilla)
        - the 'google.com' part is the *domain name*
        - google inc owns google.com
        - google also owns mail.g / calendar.g / maps.g -> DNS sets the rules
        

    - Requests are methods + data
        - methods are a standard: HTTP (protocol) established set of rules
        
    - Methods indicate purpose:
        - GET = information retrieval
        - POST = information transmission 
        \* most commonly used verbs

    - Data is data, sort of
        - A request contains metadata : data about the request
            * sources
            * destination 
            * type
            = headers

    - More Standards:
        - Data is nonuniform
        - JSON / XML

    - GET Requests:
        -"?key1=value1&key2=value2"

    - POST Requests:
        - User name and password would be included in the body of the request
        - Post requests are not obvious to people 
        - Contained in some sort of encryption
        - Does not have enough security in its own

    - What do servers say back?
        - Response codes
            * 200 OK
            * 404 Not Found
            * 500 Internal Server Error

- Servers 
        
    - How do you write one?
        - Frameworks
            - abstracts away semantics of networks
            - Only need to write logic from input data to output
            - Necessary for most backend development

        - Flask = our framework of choice
            - python 
            - Easy to learn, simple syntax
            - scales poorly on its own
                - not good at handling many requests
        

- Flask Code:

```{python}
# initialize the app
app = Flask(__name__)
# run the app
app.run()
```

Routes handle requests

```{python}
@app.route('/search', methods=['GET']_
def search():
...
```

- The return values:
    - dictionary = JSON
    - `send_from_dictionary(...) = file`


- What else is there?
    - django / spark / express


