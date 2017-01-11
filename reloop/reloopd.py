#!/usr/bin/env python
import os
# Pacify Click:
if os.environ.get("LANG", None) is None:
    os.environ["LANG"] = os.environ["LC_ALL"] = "C.UTF-8"
import click

from twisted.internet import inotify, reactor
from twisted.python import filepath
from . import __version__

watch = os.getenv('RELOOP_WATCH', '.')
before_command = os.getenv('RELOOP_BEFORE_CMD', '[ ]')
command = os.getenv('RELOOP_CMD')


def on_change(ignored, path, mask):
    """
    @param ignored: DO NOT USE. Read: http://twistedmatrix.com/documents/current/api/twisted.internet.inotify.html
    @param path: FilePath on which the event happened.
    @param mask: inotify event as hexadecimal masks
    """
    import subprocess
    import shlex

    click.echo('inotify event (events: [{}], path: {})'.format(', '.join(inotify.humanReadableMask(mask)), path))
    if before_command:
        subprocess.call(shlex.split(before_command), shell=True)

    subprocess.call(shlex.split(command), shell=True)


@click.group(name='reloopd')
@click.version_option(version=__version__)
def reloopd():
    """reloopd - reloop daemon"""


@reloopd.command()
def run():
    if not watch:
        exit(1)

    if not command:
        click.echo('ERROR: environment variable RELOOP_CMD is not set! Exiting.')
        exit(1)

    click.echo('reloopd run {0} {1}'.format(('directory' if os.path.isdir(watch) else 'file'),
                                             os.path.abspath(watch)))
    notifier = inotify.INotify()
    notifier.startReading()
    # recursive=True causes this whole thing to barely work... no FS changes will be detected.
    notifier.watch(filepath.FilePath(str(s.path.abspath(watch))), autoAdd=True, callbacks=[on_change])
    # Start it up the first time:
    on_change(None, None, None)
    reactor.run()

if __name__ == '__main__':
    reloopd()
