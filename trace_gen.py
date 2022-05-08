from os import listdir
from os.path import isfile, join

file_start = "#define FSTART(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\nEntering " \
             ": [%s] at [%s:%d]\",__func__,__FILE__, __LINE__); fclose(fp);}} "
file_end = "#define FEND(filename) {FILE* fp = fopen((filename),\"a\"); if (fp != NULL){fprintf(fp,\"\\nLeaving : [" \
           "%s] at [%s:%d]\",__func__,__FILE__, __LINE__); fclose(fp);}} "

fs = "FSTART();"
fe = "FEND();"


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
    debugList = []
    with open(filePath) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    debugList.append(file_start)
    debugList.append(file_end)

    bop = 0
    mlComm = 0
    clsOrStruct = 0
    i = 0;
    ll = len(lines)
    #for line in lines:
    while i < ll:
        line = lines[i];
        i = i+1;
        if clsOrStruct == 1:
            debugList.append(line)
            if line.find("};") != -1:
                print("ENDDDDDD")
                clsOrStruct = 0
            continue

        if line.strip().startswith("class") or line.strip().startswith("struct"):
            clsOrStruct = 1
            debugList.append(line)
            print("SASAS")
            continue

        if mlComm == 1:
            if line.index("*/") != -1:
                mlComm = 0
                debugList.append(line)
                continue

        if(line.startswith("/*")):
            debugList.append(line)
            mlComm = 1
            continue

        if line.startswith("//") or line.startswith("#"):
            debugList.append(line)
            continue


        temp = removePattern(line, "//")
        temp = str(removePattern(temp, "/*"))
        newLine = ""
        if temp.find("{") != -1:
            bop = bop+1
            if bop == 1:
                #looks like function begin
                newLine = temp[:temp.find("{") + 1] + "\n" + fs + "\n" + temp[temp.find("{") + 1:]

        if temp.find("}") != -1:
            bop = bop - 1
            if bop == 0:
                # function end
                newLine = newLine + temp[:temp.find("}")] + "\n" + fe + "\n" + temp[temp.find("}"):]
        if len(newLine) > 0:
            debugList.append(newLine)
        else:
            debugList.append(line)

    with open(filePath+"_debug", 'w') as f:
        for item in debugList:
            f.write("%s\n" % item)


processDir("./")
