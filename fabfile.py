from __future__ import with_statement

import time

from fabric.api import *
from fabric.operations import *
from fabric.colors import *
from fabric.contrib import django

from contextlib import contextmanager

env.colors = True
env.format = True
env.colorize_errors=True

# Users and passwords request
print (white('-------------------',True))
print (blue('Matta site deploy',True))
print (white('-------------------',True))

env.user = 'matta'
env.path = '/home/matta/'
env.repository = 'https://github.com/diegoduncan21/matta.git'

django.project('matta')


# def execute(command):
#     with cd(env.path):
#         with cd('releases/current'):
#             run('python manage.py {0} --settings={1}'.format(command, env.settings))

# Enviroments

@task
def production():
    env.branch = 'master'
    env.hosts = ['julianmatta.com']
    env.release = time.strftime('%Y%m%d%H%M%S')
    env.settings = 'settings.production'

# End enviroments


def symlink_current_release():
    print yellow('>>> Updating current release links ...',True)
    with cd(env.path):
        with settings(warn_only=True):
            run('rm -f releases/previous')
            run('mv releases/current releases/previous')
            run('ln -s {release} releases/current'.format(**env))
            run('chmod -R 775 releases/current')


def clean():
    with cd(env.path + '/releases'):
        run('find . -type f -name "*.py[co]" -exec rm -f \{\} \;')
    with cd(env.path):
        with cd('logs'):
            run('truncate -s 0 *.log')


@task
def deploy():
    """Service can be:
        * flyersconcierge [by default]
        * affiliates
    """
    print yellow('>>> Deploying matta release {1} to {2}'.format(env.release,
                                                                 ', '.join(env.hosts)))

    with cd(env.path):
        run('git clone {repository} -b {branch} releases/{release}'.format(**env))
    symlink_current_release()
    stop_supervisor()
    build()
    start_supervisor()


@task()
def rollback():
    print red(
        '>>> Rollback current release to the version previously deployed', True)
    with cd(env.path):
        run('cp -R releases/current releases/previous_new')
        run('mv releases/previous releases/current')
        run('mv releases/previous_new releases/previous')


@task()
def migrate():
    print yellow('>>> Updating database schema structure', True)
    sudo('docker-compose run django python manage.py migrate')


@task()
def migrate_list():
    sudo('docker-compose run django python manage.py migrate --list')


@task
def start_supervisor(service="flyersconcierge"):
    sudo('supervisorctl start matta')


@task
def stop_supervisor(service="flyersconcierge"):
    sudo('supervisorctl stop matta')
