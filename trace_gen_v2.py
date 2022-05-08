import re
from os import listdir
from os.path import isfile, join

file_start = "#define FSTART(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\nEntering " \
             ": [%s] at [%s:%d]\",__func__,__FILE__, __LINE__); fclose(fp);}} "
file_end = "#define FEND(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\nLeaving : [" \
           "%s] at [%s:%d]\",__func__,__FILE__, __LINE__); fclose(fp);}} "

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

    debugList.append(file_start)
    debugList.append(file_end)
    nf = file_start + "\n" + file_end

    match = re.search(PAT, singleLine)
    temp = singleLine
    while match is not None:
        print('Start Index:', match.start())
        print('End Index:', match.end())
        print(temp[match.start():match.end()])
        piece = temp[match.start():match.end()]
        if piece.strip().startswith("#") or piece.strip().startswith("//") or piece.strip().startswith("/*"):
            nf = nf + temp[:match.end()]
            temp = temp[match.end():]
        else:
            #nf = nf + temp[:match.end()] + "\n" + fs + "\n"
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
            while body.find("return ") != -1:
                si = body.find("return ")
                nf = nf + body[:si] + "\n" + fe + "\n" + "return "
                body = body[si + 7:]
            if voidRet == -1:
                print(body)
                body = body.rstrip()
                xlen = len(body)
                if body.endswith('}'):
                    body = body[:xlen-1] + "\n" + fe + "\n}"
                nf = nf + body
            else:
                nf = nf + body
            #nf = nf + temp[match.end():(bi - 2)] + "\n" + fe +"\n}"
            temp = temp[bi:]
        match = re.search(PAT, temp)
    nf = nf + temp

    with open(filePath + "_debug", 'w') as f:
        f.write(nf)

    # with open(filePath+"_debug", 'w') as f:
    #    for item in debugList:
    #        f.write("%s\n" % item)


processDir("./")
