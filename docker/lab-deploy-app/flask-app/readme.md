docker build -t <YOUR_USERNAME>/myfirstapp .
docker run -p 8888:5000 --name myfirstapp YOUR_USERNAME/myfirstapp

or

docker run -p 8888:5000 --name myfirstapp ducnv95/flask:1.0