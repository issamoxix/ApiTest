# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim as base

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install system dependencies for production (e.g., build-essential for compiling)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

# Step 4: Copy the current directory contents into the container at /app
COPY . /app

# Step 5: Install Python dependencies (using a requirements.txt file)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the port FastAPI will run on
EXPOSE 80

# Step 7: Use Gunicorn for production, and run the FastAPI app
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:80"]
