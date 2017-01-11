#!/usr/bin/env python
import click
import os
import click
import shlex
import subprocess

from twisted.internet import inotify, reactor
from twisted.python import filepath
from . import __version__

# Pacify Click:
if os.environ.get("LANG", None) is None:
    os.environ["LANG"] = os.environ["LC_ALL"] = "C.UTF-8"

watch = os.getenv('RELOOP_WATCH', '.')
before_command = os.getenv('RELOOP_BEFORE_CMD', None)
command = os.getenv('RELOOP_CMD')
debug = os.getenv('RELOOP_DEBUG', '0').lower() in {'1', 'true'}

proc = None


def on_change(ignored, path, mask):
    """
    @param ignored: DO NOT USE. Read: http://twistedmatrix.com/documents/current/api/twisted.internet.inotify.html
    @param path: FilePath on which the event happened.
    @param mask: inotify event as hexadecimal masks
    """

    global proc
    events = set(inotify.humanReadableMask(mask))
    print(events)
    if debug:
        click.echo('==> reloopd, DEBUG : inotify event(s) - [{}], path: {}'.format(', '.join(inotify.humanReadableMask(mask)), path))

    if ('create' or 'delete' or 'modify') in events:

        if proc is not None and proc.poll() is None:
            click.echo('==> reloopd, INFO  : terminating previous process')
            proc.kill()

        if before_command:
            subprocess.call(shlex.split(before_command), shell=True)

        proc = subprocess.Popen(shlex.split(command))


@click.group(name='reloopd')
@click.version_option(version=__version__)
def reloopd():
    """reloopd - reloop daemon"""


@reloopd.command()
def run():
    if not watch:
        exit(1)

    if before_command:
        click.echo('==> reloopd, INFO  : running RELOOP_BEFORE_CMD')
        cmd = shlex.split(before_command)
        print(cmd)
        subprocess.call(cmd)

    if not command:
        click.echo('ERROR: environment variable RELOOP_CMD is not set! Exiting.')
        exit(1)

    global proc
    proc = subprocess.Popen(shlex.split(command))

    click.echo('==> reloopd, INFO  : watching {0} {1})'.format(('directory' if os.path.isdir(watch) else 'file'),
                                                               os.path.abspath(watch)))

    notifier = inotify.INotify()
    notifier.startReading()
    # recursive=True causes this whole thing to barely work... no FS changes will be detected.
    notifier.watch(filepath.FilePath(str(os.path.abspath(watch))), autoAdd=True, callbacks=[on_change])
    reactor.run()

if __name__ == '__main__':
    reloopd()
