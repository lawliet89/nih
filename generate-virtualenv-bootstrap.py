import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
    assert subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'django']) == 0
    assert subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'MySQL-python']) == 0
    assert subprocess.call([join(home_dir, 'bin', 'pip'), 'install', 'django_nose']) == 0
"""))
f = open('bootstrap.py', 'w').write(output)
