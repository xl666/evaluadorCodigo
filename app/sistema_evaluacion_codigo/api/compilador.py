
import os
import shutil
import subprocess

"""
Compiler module
"""


def compile(arch, outPath, cplusplusCompiler = 'g++', cCompiler = 'gcc'):
    """
    arch: path file to compile
    outPath: where is going to be the compiled file
    writes a copiled file
    Returns True if the complilation was successful and the name of the compiled file
    """
    aux = arch.split('/')[-1].split('.')[:-1] #take care with \ in windows, strip extentsion
    name = ''
    finalName = ''
    for s in aux: #concatenate all
        name += s
    comand = ''

    if arch.endswith('.java'):
        comand = 'javac %s -d %s' % (arch, outPath)
        finalName = name + '.class'
    elif arch.endswith('py'): #just copy the file, python is interpreted
        shutil.copyfile(arch, '%s/%s.py' % (outPath, name) )
        finalName = name + '.py'
        return (True, finalName)
    elif arch.endswith('prolog'): #just copy the file, prolog is interpreted
        shutil.copyfile(arch, '%s/%s.prolog' % (outPath, name) )
        finalName = name + '.prolog'
        return (True, finalName)
    elif arch.endswith('.cpp'):
        comand = '%s %s -o %s/%s.o' % (cplusplusCompiler, arch, outPath, name)
        finalName = name + '.o'
    elif arch.endswith('.c'):
        comand = '%s %s -o %s/%s.o' % (cCompiler, arch, outPath, name)
        finalName = name + '.o'
    elif arch.endswith('.lisp'): #sbcl
        print(os.getcwd())
        comand = './compilarLisp.sh %s' % (arch)
        finalName = name + '.fasl'
        process = subprocess.Popen(comand.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        tup = process.communicate()
        if (not arch.endswith('lisp') and tup[1] != b'') or (b'ERROR' in tup[1]): # hay que validar tambien si no era solo un warning, esto solo esta bien para lisp
            return (False, None)
        #shutil.copyfile(arch[:arch.rfind('.')]+'.fasl', '%s/%s.fasl' % (outPath, name) )
        return (True, finalName)
    else:
        return (False, None) #not supported

    process = subprocess.Popen(comand.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    tup = process.communicate()
    if tup[1] == b'': #no errors
        return (True, finalName)
    return (False, None)
