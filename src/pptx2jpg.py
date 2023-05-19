import subprocess
import os
import tempfile
import psutil
import time
def process_check():
    try:    
        for proc in psutil.process_iter():
            print("----------------------")
            print("プロセスID:" + str(proc.pid))

            print("実行モジュール：" + proc.exe())
            print("コマンドライン:" + str(proc.cmdline()))
            print("カレントディレクトリ:" + proc.cwd())
            if str(proc.cmdline()).find('unoserver') >= 0:
                print("OK uno")
                return True
    except psutil.AccessDenied:
        print("このプロセスへのアクセス権がありません。")
    return False

def pptx2jpg(input_path,output_dir):
    #    unoserver --daemon が必要
#    output_path= output_dir + "images/sample.pdf"
    with tempfile.TemporaryDirectory() as dname:
        print(dname)                 # /tmp/tmpl2cvqpq5
        if os.path.exists(dname):
            output_path= dname + "/tmp.pdf"

            if process_check() == False:
                command = 'unoserver --daemon'
                #subprocess.Popen(command, shell=True, executable = "/bin/bash")
                punoserver = subprocess.Popen(['/bin/bash', '-c', command])
                punoserver.wait()
                #command = ['/usr/lib/libreoffice/program/oosplash', '--headless', '--invisible', '--nocrashreport', '--nodefault', '--nologo', '--nofirststartwizard', '--norestore', '-env:UserInstallation=file:///tmp/tmp_u9lnc3k', '--accept=socket,host=127.0.0.1,port=2002,tcpNoDelay=1;urp;StarOffice.ComponentContext']
                #subprocess.Popen(command, shell=True, executable = "/bin/bash")
                #command = ['/usr/lib/libreoffice/program/soffice.bin', '-env:UserInstallation=file:///tmp/tmp_u9lnc3k', '--headless', '--invisible', '--nocrashreport', '--nodefault', '--nologo', '--nofirststartwizard', '--norestore', '--accept=socket,host=127.0.0.1,port=2002,tcpNoDelay=1;urp;StarOffice.ComponentContext']
                #subprocess.Popen(command, shell=True, executable = "/bin/bash")
                print("unoserver 起動")
                time.sleep(8)
                #process_check()

            # まず unoconvert で PDF に変換
            # convert -density 144 office/sample.pdf -resize 1270x720 output/images/pptx_page_%d.jpg
            print(input_path)
            print(output_path)
            command = '/usr/local/bin/unoconvert --convert-to {convert2} {input_path} {output_path}'.format(convert2="pdf", input_path=input_path, output_path=output_path)
            print(command)
            #subprocess.run(command.split(), executable = "/bin/bash")
            #subprocess.run(command, shell=True, executable = "/bin/bash")
            punoconvert = subprocess.Popen(['/bin/bash', '-c', command])
            punoconvert.wait()

            # PDF を ImageMagicで jpg に変換
            print(output_dir)            
            command = '/usr/bin/convert -density 144 {input_path} -resize 1270x720 {output_path}/pptx_page_%d.jpg'.format( input_path=output_path, output_path=output_dir)
            print(command)
            #subprocess.run(command.split(), executable = "/bin/bash")
            #subprocess.run(command, shell=True, executable = "/bin/bash")
            pconvert = subprocess.Popen(['/bin/bash', '-c', command])
            pconvert.wait()

# pptx2jpg("/root/src/office/sample.pptx","/root/src/output/")