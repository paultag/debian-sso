# file:///usr/share/doc/fabric/html/tutorial.html

from fabric.api import local, run, sudo, cd, env

ALIOTH_IS_DOWN = False
REMOTE_USER = "debsso"

env.hosts = ["diabelli.debian.org"]

def prepare_deploy():
    #local("./manage.py test my_app")
    #local("git add -p && git commit")
    local("test `git ls-files -cdmu | wc -l` = 0")
    if ALIOTH_IS_DOWN:
        local("git push diabelli")
    else:
        local("git push")

def deploy():
    prepare_deploy()
    deploy_dir = "/srv/sso.debian.org/debsso"
    with cd(deploy_dir):
        if ALIOTH_IS_DOWN:
            sudo("git pull --rebase ~enrico/debsso.git", user=REMOTE_USER)
        else:
            sudo("git pull --rebase", user=REMOTE_USER)
        sudo("./manage.py collectstatic --noinput", user=REMOTE_USER)
        sudo("./manage.py migrate", user=REMOTE_USER)
        sudo("psql service=debsso -c 'grant select,insert,update,delete on all tables in schema public to debssoweb'",
             user=REMOTE_USER)
        sudo("psql service=debsso -c 'grant usage on all sequences in schema public to debssoweb'", user=REMOTE_USER)
        sudo("touch debsso/wsgi.py", user=REMOTE_USER)
