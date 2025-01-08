FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt ./

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt - uncomment this when you make changes to requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application files to the container
COPY ./ ./src

# Create an output folder inside the container
RUN mkdir -p /app/output

# Specify the command to run the application
CMD ["python", "src/main.py"]
