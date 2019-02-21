# Install

```
sudo apt install docker.io
sudo apt install docker-compose
```

# Run

- Name your file app.py (like one in exemple):

```
docker-compose up -d
```

- To check logs (first check container name with 'docker ps'):

```
docker logs <container name>
```

- After code change, you can relaunch container with:

```
docker restart <container name>
```

NB: 
```
docker logs | less (for search in logs)
```