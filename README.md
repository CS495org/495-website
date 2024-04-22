# 495 Website

To run it locally:
1. Follow the instructions in .env.example to create your .env file.
2. From this directory, run "./run.sh"
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
Go through the Dockerfiles (it's probably the one in /website), and comment the
"FROM localhost:5000/< image name >" and uncomment the "FROM < image name >" line above it.

### What software is needed?  (docker really shines here)
1. Docker + Compose Plugin
2. That's it! Docker takes care of installs for you

### What are sources of
### What external resources are used (put any free/paid tier information here)
1. Twilio (free tier, for simple sending of SMS)
2. Open calendar (open source embedded calendar)
3. Gmail SMTP (Free, but you must set up a gmail account and an app password to use SMTP)

### Other installation questions
1. What is AirByte and how does that work?
- AirByte is an ELT tool, but put simply it will query TMDB and accumulate all of the information about all of the 10k most popular TV shows on their site
and place it into the postgres volume to be used by our app. It keeps our database in sync with the latest shows, but it does not need to be managed much
once it has done the initial sync. You will need a TMDB API key to interact with AirByte's built in connector for TMDB

## How to use each feature (should link to sprint features in the project)
### List of features and how to use them (Should link to sprint features in the project)
1. Create an account
2. Browse top shows
3. Add and remove shows from watchlist/favorites

###  Document results of each function and how they link to other functions 
Ex: "placed orders that have not been fulfilled can be viewed on the in process screen"..."there are three types of user accounts"

### How are external resources incorporated?
1. Twilio is used to verify a user's phone number and send SMS reminders for air dates

## How to modify/extend software
### Assuming someone has followed the instruction for installing the application, how can they make changes?
1. Website pages are dynamically linked to the back-end database, but can be modified with simple HTML/CSS under "/495-website/website/templates".
2. A required python package can be added to the docker compose file by first updating "495-website/website/requirements.txt" with the desired requirement (e.g. django==5.0.2)
3. Environment variables can be added to the .env file (e.g. TWILIO_AUTH_TOKEN='1234'), and then passed through to a container using "docker-compose.yml" under environment (e.g. USER: ${POSTGRES_USER}). This allows any container to reference variables from the project's .env file, so secrets can be safely obscured from the reposiroty.
4. Objects can be appended to the database by



### What compiler, languages?  What build management? Where are the dependencies listed?  Any automated builds?
- All builds are automated through docker compose. Running the build script (```all.sh```) or the standard ```docker compose up --build``` will build and set up all containers, no need to install compilers, the python interpreter, or any other tools. 


### Where is the backlog and the project bug lists? Call out major issue such as migrating to better resources or new major versions that require retrofitting
### Should also communicate style expectations
### How to run any existing automated testing.  Location of test cases


## FAQs
1. How can I run the software locally?
- In the root directory of the repository, use the run script ```./all.sh``` or the docker command ```docker compose up --build``` and connect to ```https://localhost/``` in your chosen web browser.
2. How can I create an account?
- Click the "login" button, and follow the prompts to create an account with a username and a password, and a valid phone number.
3. How can I add a show to my watchlist/favorites?
- Simply hover over a show you like and click the "star" icon to add to "favorites", or the "checkmark" icon to add to your watchlist.
- Shows can also be directly added to watchlist/favorites from their individual pages in the same manner using the "checkmark" and "star" icons.
4. 

- Identify 3-4 frequency asked questions.  This should focus on the end user. 
- Identify any gotchas or problems you encountered either in installing parts of the application
- Possible issues with external resources
