FROM python:3.9.19
COPY . /app
WORKDIR /app
RUN pip install flask
CMD ["python", "main.py"]