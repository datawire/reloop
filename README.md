# Reloop

Reloop allows you to get a fast development cycle when working on containerized applications: just edit your code and your changes go live.

Theory of operation:

1. You mount your source code, or compiled binary, into a container.
2. Whenever your change your source code your process is restarted.

The effect is that you hit save and your change is almost immediately reflected.


## Quickstart: Python

Let's imagine you just have the following structure in your repository:

* `hello.py` (a Flask application that listens on port 5000 and uses PostgreSQL)
* `requirements.txt` (the dependencies your app needs)

To use Reloop you could create the following Docker Compose file:

```yaml
version: "2"
services:
  web:
    image: "datawire/reloop"
    ports:
      - "5000:5000"
    volumes:
      # Mount the repository as /code, read-only
      - ".:/code:ro"
    environment:
      # The file or directory to watch for updates:
      WATCH: "/code/hello.py"
      # Run once as setup:
      BEFORE_CMD: "pip install -r /code/requirements.txt"
      # Run every time the watched files change:
      CMD: "python /code/hello.py"
  postgres:
    # The postgres dependency for Flask:
    image: "postgres"
```

Now start the containers:

```console
$ docker-compose up
```

You can now access your server at `http://localhost:5000/`.
If you edit `hello.py` it will be immediately restarted.

## License

Project is open-source software licensed under **Apache 2.0**. Please see [LICENSE](LICENSE) for further details.