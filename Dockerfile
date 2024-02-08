FROM python:3.10.12-slim-buster
WORKDIR /project
ADD . /project
RUN apt update && apt install -y python3-dev \
                        gcc \
                        g++ \
                        libc-dev \
                        libffi-dev \
			libxml2-dev \
			libxslt-dev
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Cython
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ghunt
RUN python3 -m pip install shodan
volume /creds
CMD ["python3","-u", "app.py"]