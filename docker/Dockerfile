# Use the official lightweight Python 3.9 image as the base image  
FROM python:3.9-slim  

# Set the working directory inside the container to /app  
WORKDIR /app  

# Copy the requirements.txt file from the host to the container  
COPY requirements.txt .  

# Install dependencies from requirements.txt without caching to reduce image size  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy all project files from the host to the container  
COPY . .  

# Expose port 4200 (though ensure the application actually listens on this port)  
EXPOSE 4200  

# Command to run the ETL pipeline script when the container starts  
CMD ["python", "dags/etl_pipeline.py"]  
