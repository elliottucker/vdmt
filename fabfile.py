from fabric.api import local

def commit():
    local("git add -p && git commit")

def push():
    local("git push")


def prepare_deploy():
    commit()
    push()

