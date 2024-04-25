# 495 Website

To run it locally:
1. Follow the instructions in .env.example to create your .env file.
2. From this directory, run "./all.sh"
3. If you get an error about permission denied for "localhost:5000", that means
I forgot to uncomment a line in a Dockerfile about using my local docker registry.
Go through the Dockerfiles (it's probably the one in /website), and comment the "FROM localhost:5000/< image name >" and uncomment the "FROM < image name >" line above it.

# Project Documentation

## How to install software
### If someone wanted to deploy your application on their own environment, what should they do?
1. Follow the instructions in .env.example to create your .env file.
2. From this directory, run "./all.sh"
3. If you get an error about permission denied for "localhost:5000", that means
I forgot to uncomment a line in a Dockerfile about using my local docker registry.
Go through the Dockerfiles (it's probably the one in /website), and comment the line
"FROM localhost:5000/< image name >" and uncomment the line "FROM < image name >" above it.

### What software is needed?  (docker really shines here)
1. Docker + Compose Plugin
2. That's it! Docker takes care of installs for you

### What are sources of
### What external resources are used (put any free/paid tier information here)
- Twilio (free tier, for simple sending of SMS)
- Open calendar (open source embedded calendar)
- Gmail SMTP (Free, but you must set up a gmail account and an app password to use SMTP)
- The Movie Database (TMDB) API is used. You will have to register the app, but it is free to use for a school project like this

### Other installation questions
1. What is Airbyte and how does that work?
- Airbyte is an ELT application. You simply clone their repo and run the initialization script. More details are included in /database, but included in this repo is a custom connector that pulls movie and TV show data from their API. You can import /database/tmdb.yaml into an Airbyte instance, provide your API key, hook it up to a destination (like a postgres database, for example), and watch it go. It'll pull and normalize the data for you, and provide metadata.

## How to use each feature (should link to sprint features in the project)
### List of features and how to use them (Should link to sprint features in the project)
TODO (need to finish)
1. Create an account
2. Browse top shows
3. Add and remove shows from watchlist/favorites

###  Document results of each function and how they link to other functions
TODO
Ex: "placed orders that have not been fulfilled can be viewed on the in process screen"..."there are three types of user accounts"

### How are external resources incorporated?
- Twilio is used to verify a user's phone number and send SMS reminders for air dates
- Gmail is used for sending users verification emails. You will need a gmail account and an associated app password to use Gmail's SMTP server
- TMDB provides the movie and TV show data, as well as the poster and backdrop images for them. The data is pulled through Airbyte with the TMDB API. The images, however, are not. I'm not a huge fan of using Postgres for storing jpg files, and Airbyte doesn't have an easy way to iterate over rows in a database and making API calls based on the values. Images are pulled into a docker volume by a celery task. The code for this process is found in get_images() in /website/our_app/tasks.py. This repo currently serves static data (pulled from TMDB via Airbyte). This data is stored in the /database/init-2.sql file and mounted into the Postgres container at startup. In a production deployment, you'd want to expose a port of the database container and register it as a destination for your Airbyte instance.

## How to modify/extend software
### Assuming someone has followed the instruction for installing the application, how can they make changes?
- Website pages are dynamically linked to the back-end database, but can be modified with simple HTML/CSS under ```/website/templates/```. Therefore, any UI changes or additions can be directly edited in those HTML files.
- To create any changes in the middleware logic, you'll need to write Django code. This will all be done inside the ```/website/``` directory, in different subdirectories based on function.
- A required python package can be added to the web container by first updating ```/website/requirements.txt``` with the desired requirement (e.g. django==5.0.2)
- Evironment variables can be added to the .env file (e.g. TWILIO_AUTH_TOKEN='1234'), and then passed through to a container using ```docker-compose.yml``` under environment (e.g. USER: ${POSTGRES_USER}). This allows any container to reference variables from the project's .env file, so secrets can be safely obscured from the repository
- For a more in-depth description of the functionality or layout of any service, look at the README in the services top level directory. Each top level directory in this repo corresponds to a specific service in the compose. The redis container is the only one that does not have its own top level directory, as no custom code or configuration was required beyond the YAML specification.


### What compiler, languages?  What build management? Where are the dependencies listed?  Any automated builds?
- The vast majority of the actionable code in this repo is Python. It runs python 3.12 in an alpine environment. Python dependencies are listed in /website/requirements.txt.
- Builds are handled by docker. The production branch, tate-ci, has automated deployments handled by a Jenkins CI/CD server. This is not absolutely necessary for deployment, but is a nice bonus feature for hands-off deployments. Jenkins is free and open source, and if you have a couple servers laying around and want to try it out, you can check it out here: https://www.jenkins.io/.
- Each container runs from an alpine base, with the exception of the redis container. This keeps our images slimmer and more secure. The redis container runs from a chainguard base image, providing further security. We did attempt to migrate to chainguard images as a base, but the lack of a shell in their production images made such a migration more costly than beneficial.


### Where is the backlog and the project bug lists? Call out major issue such as migrating to better resources or new major versions that require retrofitting
TODO
### Should also communicate style expectations
TODO
### How to run any existing automated testing.  Location of test cases
TODO


## FAQs
1. How can I run the software locally?
- In the root directory of the project, use the run script ```./all.sh``` or the docker command ```docker compose up --build``` and connect to ```https://localhost/``` in your chosen web browser.
2. How can I create an account?
- Click the "login" button, and follow the prompts to create an account with a username and a password, and a valid phone number.
3. How can I add a show to my watchlist/favorites?
- Simply hover over a show you like and click the "star" icon to add to "favorites", or the "checkmark" icon to add to your watchlist.
- Shows can also be directly added to watchlist/favorites from their individual pages in the same manner using the "checkmark" and "star" icons.
4.

- Identify 3-4 frequency asked questions.  This should focus on the end user.
- Identify any gotchas or problems you encountered either in installing parts of the application
- Possible issues with external resources

## Gotchas/Notes for Devs
- If you're not familiar with docker, it's probably a good idea to invest in learning it up front. The most important concepts to grasp for further development of this project are: networking, storage/volumes, environment variables, images vs containers, and compose.
- Pay attention to the networking configuration. The NGINX container runs on the frontend network, while Postgres and Redis run on the backend network, and the web container bridges the two. There's no reason for the ingress controller to have access to the database or cache/message broker, except through the Django middleware. This can be modified for development, but security by isolation is the guiding principle of the internal networking setup.
- The Django application logic is served by a Gunicorn web server. The web server that ships with Django is plenty capable of serving an application for development, but is not optimized or secured for production deployment. Gunicorn makes it extremely easy to handle a larger volume of requests more efficiently, more securely, over a number of logical threads. This does mean, however, that any global variables will have to be maintained outside of the scope of the Django application. For example, if you want to increment a page-hits counter, you can't just increment a local Python variable in the a views.py file, because you're serving 2*(core count)+1 virtual threads of the app. Instead, use the cache (or the database), to make the data persist.
- If you're making changes to anything data-storage related (mainly just the models) in the Django application, make sure that you either make and migrate or you don't use the "pg-data" volume (not persisting the volume is a lot quicker/easier, but it's up to you). Changes to the structure/storage of data constitutes a database change, which won't be correctly applied if the volume containing all of the data is mounted to Postgres at startup.
- Main is not the production branch in this repo, it's tate-ci. The only significant differences are that the tate-ci branch mounts CA endorsed TLS certificates (and dh param), uses the registered domain name (tate-server.ddns.net) instead of localhost, and has an Airbyte installation that loads TMDB data to the postgres container.


## Individual Contributions
### Tate
1. Set up every container
- web: wrote dockerfile, compose entry, docker networking/volume/environment configuration, set up Django project, accounts application, our_app application, set up Gunicorn web server and celery task queue, managed settings/connections to postgres, redis, nginx
- db: wrote compose entry, set up schemas
- proxy: wrote Dockerfile, compose entry, handled routing, SSL/TLS/DH params, autogenerated certs for local HTTPS in development, set up volumes to handle serving static assets efficiently
- redis: didn't take much to set this up, basically just wrote the compose entry and we were good to go
- defined isolated networking (frontend/backend separation) and port bindings, volumes for storing persistent data and mount points for database initialization/SSL certs, healthcheck and dependency chain for correct startup procedure
- used alpine (or chainguard) base images for a lighter, more secure starting point for containers
2. Django application
- Wrote CustomUser, Show, Movie objects (/website/accounts/models.py)
- Wrote the forms, views, urls (views.py and urls.py in /website/accounts and /website/our_app) (reggie also contributed to the views and urls in our_app)
- Wrote interfaces directory for managing non Django-managed connections to external applications
- Wrote all queries in /website/our_app/SQL for filling models with data from postgres
- Managed settings for connecting to postgres as backend, redis as cache for quicker client-side rendering of select pages
3. Task queue
- Planned and implemented the celery task queue, integrated with web container (container that hosts the task queue) and redis (message broker), wrote all tasks to create objects from data from postgres backend, pull posters/backdrops from API (because Airbyte doesn't have a way to do it dynamically)
4. Data
- Gathered all of the data used in this project- chose Airbyte for ELT, deployed to production server
- Created Airbyte custom connector for TMDB to guarantee reliable, scheduled pipeline for normalized TV/movie data from TMDB (TMDB connector included in /database/tmdb.yaml, API key provided by Reiland)
- Designed and implemented all database input/output functionality that wasn't automatically handled by Django
- Added a pg_dump'ed init.sql file (containing the TV show/movie data) to the repo to allow local development without adding the overhead of a production ELT application running alongside it
5. Deployment
- Set up and hosted Jenkins server and production server, used personal domain for DDNS (tate-server.ddns.net)
- Wrote CI/CD pipelines to handle automated backups/deployments
- Merged all code from team members' branches to production branch for deployment
- Generated and maintained SSL/TLS certs, endorsed by CA, to provide secure web connections to the app
6. Odds and ends
- Set up django-dev repo to allow quick frontend development in a realistic environment without the need for the database/cache overhead
- Wrote external python package (etb-pg) for a standardized mode of database access
- Wrote all of the tests
- Wrote readmes for each top level directory, contributed to main readme
- Helped team with debugging container environments, making design choices
- Wrote a couple of non-production-worthy Django templates to demo use of templating system (loading static assets, using pythonic Django HTML features like conditionals/loops over python objects passed from backend)
- Ended up pushing 11k lines of backend/infrastructure to main (Github stats say it was 73k, but 62k of that was just the init.sql file generated by pg_dump)- this doesn't count code committed to my branch or the extra code on this (production) branch, or to other repos used in this project
- Created Github organization, repos, branch protection rules, team, and registered tvapp group email address

### Reggie
1.	Created and styled webpages
-	Created all webpages. (Will and I contributed on this together)
-	Styled webpages and made them interactive using CSS and Javascript. 
2.	Handled storing and fetching of user shows
-	Created a couple views and urls within Django to handle a user’s favorited shows, completed shows, and watchlist shows. 
-	Made icons functional allowing users to save shows to their profile.
-	Implemented ajax functions to handle the updating of a user’s show data upon the click of an icon, and used alert messages within the browser to inform a user the icon click was successful. 
-	Also changed the color of icons once an icon was successfully interacted with.
3.	Handled show recommendations
-	Used simple queries to give show recommendations if a user had shows added to their profile 
-	Added functionality to prompt a user to add shows to their profile if none had been added.
4.	Linked show cards with show profile page
-	Created show cards as components so they could easily be imported into our different webpages (this helped reduce repeated code)
-	Linked the show cards with the show profile template so a user can learn more about the show that was clicked.

### Will
1. Created and styled webpages
-  Cooperated with Reggie on the creation of and styling of all web pages.
-  Built upon Reggie's CSS and implemented his JavaScript into additional pages including the show profile template, settings page, and the user profile template
-  Assisted with the conversion of redundant code into components
-  Worked with Reggie on converting our template pages into utilizing loops that reference the back-end database
-  Added to Reggie's JavaScript to set conditions for fresh/rotten based on a show's Rotten Tomatoes score
2. Created the interactive calendar
-  Used an embedded calendar and tweaked it to work with our existing JavaScript for site functionality
-  Cooperated with Reggie on the CSS styling of the embedded calendar to match our consistent color scheme
3. Implemented the back end API for text message alerts
-  Created a Twilio account/phone number and inserted the credentials into our .env file
-  Added Twilio to the Docker file to enable it to use our credentials on startup
-  Wrote a simple Python script to test and affirm our ability to send SMS


## Functions and their inputs/outputs
All of the custom code that serves the python logic for this app are contained in /website. I'll start at the top of the subdirectories (as I'm viewing them in vscode) and work down. As our project is primarily object oriented, I'll also include details about relevant classes.
#### Accounts
- admin.py: No functions here, but this is where we register the user admin model with Django. Django makes this very simple, you just subclass the default admin class and specify the attributes you want to override
- forms.py: Following the Django framework, here it's again just subclassing their builtin user creation, modification, and login forms. The contained metaclass specified which model (and which attributes of these models) these forms apply to, and the regular attributes define what will be rendered by the template and how they will be processed
- models.py: This is where the Django magic really happens. Here we define the user, show, and movie models. By subclassing the django.db.models.Model class and dictating the specific attributes we'd like to track, along with their types and relationships, Django handles serializing this data to our backend and allows us to access database information as Python objects elsewhere in the project
- tests.py: This is where we write tests. The tests were a little tricky- I don't have a lot of web dev experience, and working within a web framework is very different than unit testing a pure, made-from-scratch backend application. Some of these work, some error, and some fail. More pass than fail. Here we are able to test our models, forms, and views, raising assertion errors when expected values don't match returned values after creating and processing inputs.
- urls.py: Here we define the url routing. It's pretty simple, the specified urls map to the specified views.
- views.py: This is where we define the logic that occurs behind the frontend when a user signs up or logs in. For crucial pieces like user registration/authentication, these deviated very little from the Django builtins. Django obscures things like input cleaning, password hashing, and uniqueness validations away from us, and allows us to just subclass their models.
#### Interfaces
This is a super simple directory. Used to centralize access to interfaces that access external (external to this container) resources.
- init.py: Init the module so you can "from interfaces import < object >"
- objs.py: This is where objects are instantiated. We have an interface for grabbing env variables, for interacting with the redis cache, and two database interfaces: one that is read-only, one that is read-write enabled
#### our_app
This is where the bulk of the logic that the user interacts with through the frontend resides.
- SQL/: This directory contains the queries for pulling data from postgres for creating objects. The pg_reader interface can execute raw string queries, but I figured it was better practice to make anything even remotely complex more observable and easier to version control.
- forms.py: Some legacy code exists here relating to user registration/authentication. I was trying to figure it out, ended up doing it in the accounts app. The fav movies and fav shows forms were used to demonstrate using Django templating with class based views/forms to avoid unnecessarily recreating processes that have been well established.
- tasks.py: This is where our celery tasks are defined. get_images() iterates over all show, movie, and topratedshow objects for which the images_loaded attribute is false. It pulls the backdrop and posters from the TMDB API, stores them in /imgVar/ (a directory mounted to the img-var volume to allow NGINX to render static assets more efficiently), and then sets the images_loaded attribute to prevent redundant, costly (in terms of time/efficiency) API calls (the img-var volume contains ~35k JPG files after full initialization of the application with the sample data provided). The insert_genre() functions uses the pg_writer interface to send the TMDB genre mapping to the database. The fill_objects() function initializes our Django models with data pulled via the custom Airbyte TMDB connector, using the queries stored in /website/our_app/SQL/. The app.task decorator allows celery to register these tasks automatically at startup.
- tests.py: Again, this is for our tests. Included are tests for the depreciated registration/authentication processes, but it doesn't hurt to include them anyways.
- urls.py: Again, this is for routing incoming requests to the appropriate views by the specified url. The cache_page decorator enables caching of static assets (through redis) to quickly render heavier pages.
- views.py: This is where the Python logic for rendering/manipulating data for templates is stored. The context passed to the template allows access to python objects from within the template. A mix of class based views (CBVs) and functional views are used, along with mixins/decorators for specifying pages that require authentication.
#### project
This directory is for the overarching Django project into which applications (accounts, our_app) are installed.
- celery.py: This is where the celery task queue is instantiated, and where the cron schedule for tasks is set.
- settings.py: This holds all of the project level settings, and varies in production vs development environments. It also holds connection settings for external services, like the cache and database, as well as user session level settings. Important production security settings, such as trusted domains and and debug status are contained here.
urls.py: This contains the top level urls, as well as the prefix routing schema for redirecting requests to their corresponding views.
- wsgi.py: This is autogenerated by Django and holds the WSGI (web server gateway interface) object that manages requests directed to the application (asgi.py is also autogenerated, but we didn't use an async gateway).
#### templates
This directory is for frontend Django templates. I didn't do any production frontend work, so I'll let someone else take this.
#### gunicorn_config.py
This file contains the gunicorn web server configuration. Django's inbuilt development server is handy for exactly what it was designed for- development. It's not suitable for a production deployment. Ingress and incoming request load balancing is handled by the reverse proxy, which sends them upstream to the gunicorn web server, which handles efficiently serving the python logic defined (basically load balancing and multithreading [virtually, not physically] the backend).
