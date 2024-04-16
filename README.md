# 495 Website

To run it locally:
1. Follow the instructions in .env.example to create your .env file.
2. From this directory, run "./run.sh"
3. If you get an error about permission denied for "localhost:5000", that means
I forgot to uncomment a line in a Dockerfile about using my local docker registry.
Go through the Dockerfiles (it's probably the one in /website), and comment the "FROM localhost:5000/< image name >" and uncomment the "FROM < image name >" line above it.

More docs to come.