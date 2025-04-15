# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install stuff
RUN pip install requests
RUN pip install Pillow
RUN pip install numpy
RUN pip install tensorflow==2.18.0
RUN pip install --no-cache-dir Flask==3.1.0

# Copy API script into 
COPY models/ models/
COPY api.py .

# Expose the default Flask port
EXPOSE 5000

# Command to run your API
CMD ["python", "api.py"]