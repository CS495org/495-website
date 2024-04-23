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