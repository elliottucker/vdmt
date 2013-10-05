from __future__ import with_statement
from fabric.api import local,settings,abort,run,cd
from fabric.contrib.console import confirm



def test():
    with settings(warn_only=True):
        result = local('./manage test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue"):
        abort("Aborting")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")


def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    keydir = '/home/vagrant/keys'
    with settings(warn_only=True):
        if run("test -d %s" % keydir).failed:
            run("git clone git@github.com:elliottucker/junk.git %s" % keydir)
        with cd(keydir):
            run("git pull")
            run("ls")
    
    with cd(keydir):
        run("git pull")
        run("ls")