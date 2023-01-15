FROM python:3.10-alpine
WORKDIR /app
COPY filetracker ./filetracker
COPY main.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8000
