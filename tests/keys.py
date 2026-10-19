import ast, os, pty, sys, re, select, termios, tty, threading, time, io
src=open(sys.argv[1]).read(); t=ast.parse(src)
want={"ESC_PART","ESC_KEY","finish_escapes","read_choice"}
code=[n for n in t.body if (isinstance(n,ast.FunctionDef) and n.name in want) or (isinstance(n,ast.Assign) and n.targets[0].id in want if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) else False)]
def run(chunks):
    m,s=pty.openpty(); f=os.fdopen(s,"r")
    g=dict(re=re,os=os,select=select,termios=termios,tty=tty,RAW=io.StringIO(),sys=type("S",(),{"stdin":f}))
    exec(compile(ast.Module(body=code,type_ignores=[]),"x","exec"),g)
    def feed():
        for c,d in chunks: time.sleep(d); os.write(m,c.encode())
    threading.Thread(target=feed,daemon=True).start()
    try: return g["read_choice"]({"y":(5,12),"n":(15,21)})
    except KeyboardInterrupt: return "STOP"
scroll="".join(f"\x1b[<65;30;{i}M" for i in range(10))
cut=len(scroll)//2+3
print("split scroll then y:", run([(scroll[:cut],.4),(scroll[cut:],.01),("y",.1)]))
print("tail garbage then n:", run([("2;30M",.4),("n",.1)]))
print("lone esc:", run([("\x1b",.4)]))
print("arrow then y:", run([("\x1b[A",.4),("y",.1)]))
print("click on yes:", run([("\x1b[<0;7;5M",.4)]))
