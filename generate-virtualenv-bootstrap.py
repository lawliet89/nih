import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
    subprocess.call([join(home_dir, 'bin', 'pip'), 'django'])
    subprocess.call([join(home_dir, 'bin', 'pip'), 'psycopg2'])
"""))
f = open('bootstrap.py', 'w').write(output)
