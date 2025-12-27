FROM python:3.10.13-slim

WORKDIR /app

COPY requirements.txt .

# Install your Python libraries
RUN pip install --no-cache-dir --upgrade pip==23.3.1 && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code (app.py, static/, templates/)
COPY . .

# Open the port Flask runs on (5000)
EXPOSE 5000

# Configure Flask app module for the `flask run` command
ENV FLASK_APP=app.py

# The command to run your app
# "0.0.0.0" is MANDATORY. It tells Flask to accept connections from outside the container.
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
