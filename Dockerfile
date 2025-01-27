# Step 1: Use Python 3.11 slim image
FROM python:3.11-slim as base

# Step 2: Set up working directory inside the container
WORKDIR /app

# Step 3: Install system dependencies needed for production (e.g., gcc for compiling C extensions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Step 4: Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code into the container
COPY . .

# Step 6: Expose port 8000 for the application
EXPOSE 8000

# Step 7: Use Gunicorn with Uvicorn worker for production (don't use --reload in prod)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
