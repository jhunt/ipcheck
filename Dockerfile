FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
