Syllabus
--------

### Description

The digital age is making it easier, faster and cheaper to develop new products and services that directly address 
societal, commercial needs. Cornell Tech Studio classes give our students tools to imagine and design such products and
services. Cornell Tech technical classes give our students the depth to come up with innovative solutions to make such
products and services real.

The goal of the "Building Startup Systems" class is to give our students a concrete experience of designing, 
implementing and deploying a workable system that can be demo-ed and/or used by early users. 
The "Building Startup Systems" class is a 1-credit course, 3 hours per week for 5 weeks. The class will run 
August 23-September 20.

The class will be anchored around the design, implementation and deployment of a typical webapp. 
The topics will be presented in the context of a project that all students will have to work on. 
The class will also bring together some software engineering best practices. Students will work on the project in pairs
(note: each student will be paired twice for the duration of the class).



### Prerequisites

* Comfortable managing systems, processes, and editing files using only unix shell
* Experience with at least one well-typed or compiled language (Scala, Java, C++, etc.)
* Experience with at least one scripted language (JavaScript, Ruby, PHP, node.js, Python, etc.)
* Experience with HTML and CSS.


### Lectures
1. Git overview
   - init a repo, make a change, commit
   - show local repo
   - students clone the course repo
   - show remote repo
   - commit + push
   - send pull requests
   - Create understanding of index, local + staged
   - Show reset, reset --hard, fetch + pull
   - Clone rebase repo, work through rebase

2. Continuous Integration
   - Students clone the base project
   - Walk through build.gradle line-by-line
   - Setup clean circle.yml
   - Setup webhooks on circle.yml
   - Push a dummy commit and see failing badge in GitHub
   - Fix test, push + see passing badge in GitHub

3. AWS Brief Overview

4. HTTP Basics
   - Brief history of HTTP
   - HTTP via telnet
   - HTTP interactions in browser using Chrome Dev Tools
   - Put a breakpoint in HTTP server to debug
   - Break down different methods of sending data (Query Params etc)
   - HTTP Response Codes
   - REST Concepts 
   - General mapping of REST verbs + resources into code

5. App Architecture Walkthrough
   - Block + arrow diagram of Dropwizard technologies
   - Setup controller
   - Setup path routing
   - Create Hello World endpoint
   - Request + Response Models
   - Model validation
   - Exception Handling
   - Using Groovy console to test serialization


6. Connect to MySQL Database
   - Create some tables
   - Query, Join

7. Sessions
   - Build basic REST endpoint for receipts
   - Motivate use of sessions to partition database by-user
   - Live-code the session middleware

8. Introduce Google Vision API and use it for Optical character recognition.


9. Web Page Basics
   - HTML, DOM, CSS, Rendering Pipeline
   - jQuery


10. Intro to Docker and how to deploy on Amazon ECS Cluster
    - Docker demo
    - Docker architecture
    - Building a Dockerfile
    - Layered architecture
    - Docker push
    - Setup docker-compose with MySQL Server running
    - Amazon AWS EC2 Container Service (ECS)
    - Setup the Elastic Load Balancing (ELB)
    - Setup the ECS Cluster

