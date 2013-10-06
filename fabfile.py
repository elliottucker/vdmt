from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import append,contains

from hashlib import md5

env.hosts = ['127.0.0.1:2222','127.0.0.1:2200']
env.user = 'vagrant'
env.password= 'vagrant'
env.key_filename = "~/.ssh/key_1.pem"
keyname = "key_1.pub"
tmp = '/tmp/vdmt'
binarystore = '~/Projects/Vold'
VOLDEMORT_HOME="/opt/voldemort"



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


def  deploy():
    
    run("mkdir -p %s" % tmp)
    # copy binaries
    put("%s/voldemort/*" % (binarystore,VOLDEMORT_HOME))
    run("git clone https://github.com/elliottucker/vdmt.git %s" % tmp)
    with cd(tmp):
        run("mv config/* %s/config/" % VOLDEMORT_HOME)
        
        
    

    # checkout config

    
def setup_host():
    # make sure git is installed.
    with settings(warn_only=True):
        if run("git  --version").failed:
            run("sudo apt-get install git -y")

    run("git clone https://github.com/elliottucker/vdmt.git %s" % tmp)

    # check keys   
    run("mkdir -p ~/.ssh")
    with settings(warn_only=True), cd(tmp):
        keystring= open(keyname,'r').read()
        localkeyhash = md5(keystring).hexdigest()
        remotekeyhash = run("md5sum %s | cut  -f 1 -d ' '" % keyname)

        print "local %s  -  remote %s" % (localkeyhash,remotekeyhash)

        if localkeyhash==remotekeyhash:
            if append("~/.ssh/authorized_keys",keystring):
                print "key added"

        else:
            abort("hashes don't match.  oops")
