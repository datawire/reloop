#!/usr/bin/env python
import click
import os

from pathlib import Path
from twisted.internet import inotify, reactor
from twisted.python import filepath
from . import __version__

watch = Path(os.getenv('RELOOP_WATCH', '.'))
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
        subprocess.call(before_command, shell=True)

    subprocess.call(command)


@click.group(name='reloopd')
@click.version_option(version=__version__)
def reloopd():
    """reloopd - reloop daemon"""


@reloopd.command()
def run():
    if not command:
        click.echo('ERROR: environment variable RELOOP_CMD is not set! Exiting.')
        exit(1)

    click.echo('reloopd run {0} {1})'.format(('directory' if watch.is_dir() else 'file'),
                                             watch.absolute()))
    notifier = inotify.INotify()
    notifier.startReading()
    notifier.watch(filepath.FilePath(str(watch.absolute())), watch.is_dir(), autoAdd=True, callbacks=[on_change])
    reactor.run()

if __name__ == '__main__':
    reloopd()
