FROM python:3.10.6
COPY requirements.txt ./app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn","--bind","0.0.0.0:5000","app:app"]
