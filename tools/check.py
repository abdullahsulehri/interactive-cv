"""One command before every publish:   python tools/check.py
Runs: content sync check -> lint (S1-S8) -> audit at 9 sizes (Q1) -> alignment report.
Serves the repo locally, so it checks YOUR changes, not the live site. Exit code 1 = do not publish."""
import subprocess,sys,time,pathlib,socket
root=pathlib.Path(__file__).resolve().parent.parent;py=sys.executable
def step(name,cmd):
    print(f'\n== {name} ==',flush=True);r=subprocess.run(cmd,cwd=root);return r.returncode==0
ok=step('content sync',[py,'tools/sync_content.py','--check']) and step('lint',[py,'tools/lint.py'])
if ok:
    s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
    srv=subprocess.Popen([py,'-m','http.server',str(port),'--bind','127.0.0.1'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(2);url=f'http://127.0.0.1:{port}/'
        ok=step('audit (9 sizes)',[py,'tools/audit.py',url])
        step('alignment report (needs the real fonts: trust it on GitHub, not offline)',[py,'tools/align.py',url])
    finally: srv.kill()
print('\nCHECK PASS: safe to publish' if ok else '\nCHECK FAILED: do not publish');sys.exit(0 if ok else 1)
