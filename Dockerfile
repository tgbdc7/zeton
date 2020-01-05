FROM python:3.7

WORKDIR  /zeton
COPY . .
RUN pip install -r requirements.txt
RUN python recreate_db.py
EXPOSE 5000
CMD ["python", "run.py"]