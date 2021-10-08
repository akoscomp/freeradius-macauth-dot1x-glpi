FROM python:3
RUN pip3 install mariadb
WORKDIR /usr/src/app
COPY test.py .
CMD ["test.py"]
ENTRYPOINT ["python3"]
