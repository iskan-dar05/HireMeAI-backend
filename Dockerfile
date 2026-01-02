# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /

# Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN apt-get update \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app

# Default command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
