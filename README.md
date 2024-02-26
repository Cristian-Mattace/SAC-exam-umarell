# UNIMORE SAC EXAM FEBRUARY 2024

We want to create an application for the management of a new service called Umarell as a Service. 
In the service you can register yards that want to be observed and umarell looking for yards to watch. 

The application has two interfaces:
1. APIs for construction site and umarell management 
2. Web interface for construction site search 

The application must be stretched for deployment on GCP platform using the following services:
- App Engine
- Firestore
- PubSub

## REST API backend
The application must expose the following features via appropriate restful Web APIs:

- ``POST`` and ``GET`` requests to the URI _/api/v1/umarell/{idumarell}_ you can add or retrieve data related to an umarell
- ``POST`` and ``GET`` requests to the URI _/api/v1/cantiere/{idcantiere}_ it is possible to add or retrieve data relating to a construction site
- ``POST`` requests to the URI _/api/v1/clean_ you can delete the consumption stored in the firestore database

The API usage interface must strictly match the available OpenAPI specification file along with this specification.

## Web Application
Create a web page that allows you to query the database of sites and umarell. 
The page must include a form with two controls:
- An entryfield to insert a CAP to search
- A series of checkboxes that allow you to select whether the search should made for umarells, construction site or both.

Once a request has been sent, a list of umarells and construction site is returned to the page (depending on what has been selected) indicating address or first name and surname.

## Interconnection of Services (PubSub)
Implement a system that implements a notification mechanism that allows the umarell to be updated on new construction sites. 
A umarell can be registered to a topic and receive notifications about new construction sites being entered. 
From the command line you can specify one cap that will be used to filter useful messages.

