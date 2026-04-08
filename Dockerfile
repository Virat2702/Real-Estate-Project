# 1. Use an official, lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install necessary system tools (helpful for some ML libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file first (for caching purposes)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project files (including the .pkl files)
COPY . .

# 7. Tell Docker which port Streamlit uses
EXPOSE 8501

# 8. Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]