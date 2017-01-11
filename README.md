# Reloop
[![Build Status](https://travis-ci.org/datawire/reloop.svg?branch=master)](https://travis-ci.org/datawire/reloop)

Reloop allows you to get a fast development cycle when working on containerized applications: just edit your code and your changes go live.

Theory of operation:

1. You mount your source code, or compiled binary, into a container.
2. Whenever your change your source code your process is restarted.

The effect is that you hit save and your change is almost immediately reflected.

## Known Limitations

This currently only works on Linux hosts; OS X is planned.

Docker Hub is laggy (or operator error is causing issues) so the necessary image may not be available yet.

## Quickstart: Python

Before we begin, move into the `example` directory.

`$ cd example/`

Let's imagine you just have the following structure in your repository:

* `hello/hello.py` (a Flask application that listens on port 5000 and uses PostgreSQL)
* `requirements.txt` (the dependencies your app needs)

To use Reloop you could create the following Docker Compose file:

```yaml
version: "2"
services:
  web:
    # Use the special reloop image:
    image: "datawire/reloopd"
    ports:
      - "5000:5000"
    volumes:
      # Mount the repository as /hello, read-only
      - ".:/code:ro"
    environment:
      # The file or directory to watch for updates:
      RELOOP_WATCH: "/code"
      # Run once as setup:
      RELOOP_BEFORE_CMD: "pip install -r /code/requirements.txt"
      # Run every time the watched files change:
      RELOOP_CMD: "python /code/hello/hello.py"
    depends_on:
      - mydatabase
  mydatabase:
    # The postgres dependency for hello.py:
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
