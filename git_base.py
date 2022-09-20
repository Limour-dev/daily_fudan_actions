from datetime import datetime
import subprocess
import traceback
import locale
from sys import argv as sys_argv

def fuck_windows(std):
    lines = std.readlines()
    try:
        return ''.join(line.decode('utf-8') for line in lines)
    except UnicodeDecodeError:
        encoding = locale.getpreferredencoding()
        return ''.join(line.decode(encoding) for line in lines)

def fuck_cmd(cmd):
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    child.stdin.close()
    ret = child.wait()
    val = fuck_windows(child.stdout)
    if val:
        val += '\n' + fuck_windows(child.stderr)
    else:
        val = fuck_windows(child.stderr)
    return ret, val

subprocess.getstatusoutput = fuck_cmd

def try_call(call, *arg, **kw):
    try:
        call(*arg, **kw)
    except:
        print(traceback.format_exc())

def run_pythonfile(f):
    ret, val = subprocess.getstatusoutput(f"python3 ./{f}")
    print(ret, val)
    if ret:
        ret, val = subprocess.getstatusoutput(f"python ./{f}")
        print(ret, val)
    return ret

def cmd_lines(lines):
    for line in lines:
        ret, val = subprocess.getstatusoutput(line)
        if ret:
            print(ret, val)
            return ret

def git_setIdentity():
    lines = [
            'git config --global user.name  "github-actions"',
            'git config --global user.email "github-actions@github.com"'
            ]
    return cmd_lines(lines)

def git_rm_upstream():
    lines = [
            "git remote rm upstream"
        ]
    return cmd_lines(lines)

def git_add_upstream(url):
    try_call(git_rm_upstream)
    lines = [
            "git config --global pull.rebase true",
            "git config --global merge.ours.driver true",
            f"git remote add upstream {url}"
        ]
    return cmd_lines(lines)

def git_revoke():
    lines = [
            'git reset --hard "HEAD^"',
            'git push origin main --force'
            ]
    return cmd_lines(lines)

def git_c2upstream():
    lines = [
            'git fetch upstream --depth=1',
            'git checkout upstream/main'
            ]
    return cmd_lines(lines)

def git_push():
    ret, val = subprocess.getstatusoutput("git status")
    if ret or "nothing to commit" in val:
        print(ret, val)
        return 1
    lines = [
            "git add .",
            'git commit -m "autocreated by git_base.py"',
            "git push origin main --force"
        ]
    return cmd_lines(lines)

def run_pythonfile_arg(f, arg):
    ret, val = subprocess.getstatusoutput(f'python3 ./{f} "{arg}"')
    print(ret, val)
    if ret:
        ret, val = subprocess.getstatusoutput(f'python ./{f} "{arg}"')
        print(ret, val)
    return ret

def get_arg():
    if (len(sys_argv) != 2) or (not sys_argv[1]):
        print('no arg')
        return ''
    return sys_argv[1]

def pip_install():
    lines = [
            'python3 -m pip install --upgrade pip',
            'pip3 install -r requirements.txt'
            ]
    ret = cmd_lines(lines)
    if ret:
        lines = [
                'python -m pip install --upgrade pip',
                'pip install -r requirements.txt'
                ]
        return cmd_lines(lines)

try_call(git_setIdentity)
