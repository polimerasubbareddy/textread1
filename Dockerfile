FROM python:3.7

RUN apt-get update && sudo apt install tesseract-ocr && sudo apt install libtesseract-dev

# copy your application code to the container
COPY . /app

# set the working directory to your application's directory
WORKDIR /app

# install your Python dependencies
RUN pip install -r requirements.txt

# start your application
CMD ["python", "app.py"]
