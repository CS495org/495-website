cd cs495_website

sudo docker build -t website .

sudo docker run -p 8000:8000 website

http://localhost:8000/