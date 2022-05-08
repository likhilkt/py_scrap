#  Copyright (c) 2022 Likhil M
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the
#  Software is furnished to do so.

#  USAGE
#  python3 trace_gen_v3.py sourceDir [0|1] logFileName
#  0 = printf, 1 = print to log file

usage = "USAGE\npython3 trace_gen_v3.py sourceDir [0|1] logFileName\n0 = printf, 1 = print to log file"
import os
import re
import sys
from os import listdir
from os.path import isfile, join

file_start_def = "#define FSTART(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\n[PID = %d] Entering " \
                 ": [%s] at [%s:%d]\",getpid(),__func__,__FILE__, __LINE__); fclose(fp);}} "
file_end_def = "#define FEND(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\n[PID = %d] Leaving : [" \
               "%s] at [%s:%d]\",getpid(),__func__,__FILE__, __LINE__); fclose(fp);}} "

file_start_print = "#define FSTART() {printf(\"\\n[PID = %d] Entering " \
                   ": [%s] at [%s:%d]\",getpid(),__func__,__FILE__, __LINE__);} "
file_end_print = "#define FEND() {printf(\"\\n[PID = %d] Leaving : [" \
                 "%s] at [%s:%d]\",getpid(),__func__,__FILE__, __LINE__);} "

file_start = file_start_print
file_end = file_end_print

fs = "FSTART();"
fe = "FEND();"

# fun pat
PATold = r'[a-zA-Z_]+[0-9]*[\s]+[a-zA-Z_]+[0-9]*[:]*[a-zA-Z_]+[0-9]*[\s]*[\(]+[a-zA-Z0-9_\*&\s\.\,]*[\)][\s]*[{]'
PAT = r'[a-zA-Z_]+[0-9]*[\s]+[a-zA-Z_]+[0-9]*[:]*[a-zA-Z_]+[0-9]*[\s]*[\(]+[a-zA-Z0-9_\*&\s\.\,]*[\)][\s]*[{]'


def processDir(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        if f.lower().endswith(".c") or f.lower().endswith(".cpp"):
            processFile(f)
    pass


def removePattern(text, patt):
    index = text.find(patt)
    if index == -1:
        return text
    else:
        return text[:index]


def processFile(filePath):
    print("Processing : " + filePath)
    lines = []
    singleLine = " "
    debugList = []
    with open(filePath) as file:
        lines = file.readlines()
        # lines = [line.rstrip() for line in lines]
    for line in lines:
        singleLine = singleLine + line
    debugList.append("#include <unistd.h>\n")
    debugList.append(file_start)
    debugList.append(file_end)
    nf = "#include <unistd.h>\n" + file_start + "\n" + file_end + "\n"

    match = re.search(PAT, singleLine)
    temp = singleLine
    while match is not None:
        # print('Start Index:', match.start())
        # print('End Index:', match.end())
        # print(temp[match.start():match.end()])
        piece = temp[match.start():match.end()]
        if piece.strip().startswith("#") or piece.strip().startswith("//") or piece.strip().startswith("/*"):
            nf = nf + temp[:match.end()]
            temp = temp[match.end():]
        else:
            # nf = nf + temp[:match.end()] + "\n" + fs + "\n"
            bop = 1
            bi = match.end()
            while bop != 0:
                if temp[bi] == '{':
                    bop = bop + 1
                elif temp[bi] == '}':
                    bop = bop - 1
                bi = bi + 1

            body = temp[match.end():bi]
            nf = nf + temp[:match.end()] + "\n" + fs + "\n"
            voidRet = body.find("return")
            while body.find("return") != -1:
                si = body.find("return")
                nf = nf + body[:si] + fe + "return"
                body = body[si + 6:]
            if voidRet == -1:
                # print("NEW " + body)
                body = body.rstrip()
                xlen = len(body)
                if body.endswith('}'):
                    body = body[:xlen - 1] + "\n" + fe + "\n}"
                nf = nf + body
            else:
                if re.search(r'[a-zA-Z]', body) is not None:
                    xlen = len(body)
                    if body.endswith('}'):
                        body = body[:xlen - 1] + "\n" + fe + "\n}"
                        nf = nf + body
                    else:
                        nf = nf + body
                else:
                    nf = nf + body
            # nf = nf + temp[match.end():(bi - 2)] + "\n" + fe +"\n}"
            temp = temp[bi:]
        match = re.search(PAT, temp)
    nf = nf + temp

    with open(filePath + "_debug", 'w') as f:
        f.write(nf)

    # with open(filePath+"_debug", 'w') as f:
    #    for item in debugList:
    #        f.write("%s\n" % item)


# main
n = len(sys.argv)
if n == 0 or n == 1:
    print(usage)
    sys.exit(0)
elif n == 4:
    if (sys.argv[2] == '1'):
        fs = "FSTART(\"" + sys.argv[3] + ".log\");"
        fe = "FEND(\"" + sys.argv[3] + ".log\");"
        file_start = file_start_def
        file_end = file_end_def
elif n == 2:
    pass
else:
    print(usage)
    sys.exit(0)

path = sys.argv[1]
if os.path.isfile(path):
    processFile(path)
elif os.path.isdir(path):
    processDir(path)
