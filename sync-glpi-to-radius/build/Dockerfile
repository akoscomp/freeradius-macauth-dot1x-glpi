# set base image
FROM python:3

# install cron
RUN apt-get update && apt-get install -y cron

# set the working directory in the container
WORKDIR /code

# copy files to the working directory
COPY . .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# run crontab
RUN crontab crontab

# start cron process
CMD ["cron", "-f"]
