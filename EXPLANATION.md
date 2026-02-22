# Concept Explanations

Here are the explanations for the terms you requested:

## 1. CRUD
**CRUD** stands for **C**reate, **R**ead, **U**pdate, **D**elete.  
These are the four basic operations that persistent storage (data storage) systems typically support. In the context of an API (like our ToDo app), they correspond to HTTP methods:
- **Create** -> `POST` (Create a new ToDo item)
- **Read** -> `GET` (Get a list of ToDos or a single ToDo)
- **Update** -> `PUT` or `PATCH` (Edit an existing ToDo)
- **Delete** -> `DELETE` (Remove a ToDo)

## 2. Endpoint
An **Endpoint** is a specific URL (Uniform Resource Locator) pattern that an API exposes to clients (users or other apps) to perform actions.  
It is like a "digital door" to a specific function of your application.
- Example: `GET https://myapp.com/api/todos` is an endpoint to get the list of todos.
- Example: `GET https://myapp.com/api/todos/5` is an endpoint to get the todo with ID 5.

## 3. Uvicorn
**Uvicorn** is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation for Python.
- **FastAPI** is the framework you use to write your code (logic, routing, validation).
- **Uvicorn** is the server that actually *runs* your code, listens for incoming requests from the internet, and sends back the responses your FastAPI code generates.
- Without Uvicorn (or a similar ASGI server like Hypercorn), your FastAPI application is just a bunch of code files; Uvicorn makes it a running web server.
