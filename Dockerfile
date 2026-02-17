FROM python:3.11-slim-bookworm

# Set the working directory
WORKDIR /project

# Define a volume for credentials
VOLUME /creds


# Update the package list and install system dependencies
RUN apt update && apt install -y \
    python3-dev \
    gcc \
    g++ \
    libc-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    nmap \
    && apt-get clean

# Upgrade pip and install Python dependencies in one go
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install Cython \
    && python3 -m pip install ghunt shodan streamlit


# Add the current directory contents into the container
ADD . /project
RUN python3 -m pip install -r requirements.txt

# Define the default command to run the app
CMD ["streamlit", "run", "stapp.py"]
