#How to install software
- If someone wanted to deploy your application on their own environment, what should they do?
1. Follow the instructions in .env.example to create your .env file.
2. From this directory, run "./run.sh"
3. If you get an error about permission denied for "localhost:5000", that means
I forgot to uncomment a line in a Dockerfile about using my local docker registry.
Go through the Dockerfiles (it's probably the one in /website), and comment the
"FROM localhost:5000/< image name >" and uncomment the "FROM < image name >" line above it.

- What software is needed?  (docker really shines here)
1. Docker
2. Postgres
3. Django
4. Redis
5. Gunicorn

- What are sources of
- What external resources are used (put any free/paid tier information here)
1. Twilio (free tier, for simple sending of SMS)
2. Open calendar (open source embedded calendar)

#How to use each feature (should link to sprint features in the project)
- List of features and how to use them (Should link to sprint features in the project)
1. Create an account
2. Browse top shows
3. Add and remove shows from watchlist/favorites

-  Document results of each function and how they link to other functions 
Ex: "placed orders that have not been fulfilled can be viewed on the in process screen"..."there are three types of user accounts"

- How are external resources incorporated?
1. Twilio is used to verify a user's phone number and send SMS reminders for air dates

#How to modify/extend software
- Assuming someone has followed the instruction for installing the application, how can they make changes?
1. Website pages are dynamically linked to the back-end database, but can be modified with simple HTML/CSS under "/495-website/website/templates".
2. A requirement can be added to the docker compose file by first updating "495-website/website/requirements.txt" with the desired requirement (e.g. django==5.0.2), then added to the .env file (e.g. TWILIO_AUTH_TOKEN='1234'), and then to "docker-compose.yml" under environment (e.g. USER: ${POSTGRES_USER}). This allows the site to run and directly reference the .env file without explicity exposing credentials or critical information.
3. Objects can be appended to the database by



- What compiler, languages?  What build management? Where are the dependencies listed?  Any automated builds?
1. FINISH_ME


- Where is the backlog and the project bug lists? Call out major issue such as migrating to better resources or new major versions that require retrofitting
- Should also communicate style expectations
- How to run any existing automated testing.  Location of test cases


#FAQs
1. How can I run the software locally?
- In the "/495-website/" directory, run docker compose up --build and connect to localhost 8080 in your chosen web browser.
2. How can I create an account?
- Click the "login" button, and follow the prompts to create an account with a username and a password, and a valid phone number.
3. How can I add a show to my watchlist/favorites?
- Simply hover over a show you like and click the "star" icon to add to "favorites", or the "checkmark" icon to add to your watchlist.
- Shows can also be directly added to watchlist/favorites from their individual pages in the same manner using the "checkmark" and "star" icons.

- Identify 3-4 frequency asked questions.  This should focus on the end user. 
- Identify any gotchas or problems you encourtered either in installing parts of the application
- Possible issues with external resources
