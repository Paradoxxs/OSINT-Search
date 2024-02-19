# OSINT Search

Docker container for automating the searching of OSINT sources

rename config.env.template to config.env

Building the container using:
```
docker build -t osint-search .
```

Running the container:

```
docker run -p 8080:8501 -d osint_search
``` 
