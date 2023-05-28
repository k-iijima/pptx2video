import subprocess
import os
import tempfile
import psutil
import time
def process_started(name):
    try:    
        for proc in psutil.process_iter():
            #print("process id:" + str(proc.pid))
            #print("exe:" + proc.exe())
            #print("cmdline:" + str(proc.cmdline()))
            #print("cwd:" + proc.cwd())
            if (str(proc.exe()).find(name) >= 0):
                print("alredy staertd:"+ name)
                return True
    except psutil.AccessDenied:
        print("AccessDenied")
    return False

def waiting_process_startup(timeout):
    for i in range(timeout):
        if process_started("oosplash") and process_started("soffice.bin"):
            return True
        time.sleep(1)
    return False

def pptx2jpg(input_path,density,output_dir):

    #with tempfile.TemporaryDirectory() as dname:
    dname = output_dir
    if os.path.exists(dname):
        output_path= dname + "/tmp.pdf"

        if not waiting_process_startup(1):
            command = 'unoserver --daemon'
            punoserver = subprocess.Popen(['/bin/bash', '-c', command])
            punoserver.wait()
            print("start unoserver")
            if waiting_process_startup(10):
                print("time out")
                return False

        # まず unoconvert で PDF に変換
        # convert -density 144 office/sample.pdf -resize 1270x720 output/images/pptx_page_%d.jpg
        print(input_path)
        print(output_path)
        command = '/usr/local/bin/unoconvert --convert-to {convert2} {input_path} {output_path}'.format(convert2="pdf", input_path=input_path, output_path=output_path)
        print(command)
        punoconvert = subprocess.run(['/bin/bash', '-c', command])
        #punoconvert.wait()

        # PDF を ImageMagicで jpg に変換
        print(output_dir)            
        command = '/usr/bin/convert -density {density} {input_path} -resize 1270x720 {output_path}/pptx_page_%d.jpg'.format( density=density,input_path=output_path, output_path=output_dir)
        print(command)
        pconvert = subprocess.run(['/bin/bash', '-c', command])
        #pconvert.wait()
    return True
# pptx2jpg("/root/src/office/sample.pptx","/root/src/output/")