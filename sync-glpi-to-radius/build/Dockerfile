FROM python:3
RUN pip3 install mariadb
WORKDIR /usr/src/app

COPY *.py .

CMD ["test.py"]
CMD ["main.py"]

ENTRYPOINT ["python3"]
