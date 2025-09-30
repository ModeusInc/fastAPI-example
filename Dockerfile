FROM python:3.13.7  

WORKDIR /usr/src/app  

COPY requirements.txt ./  

RUN pip install --no-cache-dir -r requirements.txt  
COPY . .  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#All steps explained

# your base image
# sets the working directory inside the container
# copies requirements.txt into the container at /usr/src/app
# copies the rest of your code into the container
# runs your app