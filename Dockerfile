FROM python:3.11

WORKDIR /app
ADD ZarScrapy.py /app
ADD requirements.txt /app


RUN pip install -r requirements.txt

CMD ["python", "./ZarScrapy.py"]