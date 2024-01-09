from tkinter import filedialog as fd
from colorama import Fore, init
from os import system, path
from sys import argv

init()
system('title Smdcut for goldsrc')

files=[]

print(Fore.YELLOW + "\n\n                                 SmdCut" + Fore.RESET)
print("    Utility for cuting .SMD files to bypass GoldSrc engine's limits.\n")

if len(argv)<2:
    filenames = fd.askopenfilenames(
        title='Select smd reference files',
        initialdir='/',
        filetypes=(
            ('Goldsrc model reference file', '*.smd'),
        )
    )
    for file in filenames:
        files.append(file)
elif argv[1].lower()=="help" or argv[1].lower()=="?":
    print(Fore.GREEN + "    Usage:" + Fore.RESET + " smdcut.exe <file1> <file2> <file3> ...")
    print("    Or you can simply drag and drop the files you want to cut into " + Fore.GREEN + "smdcut.exe" + Fore.RESET + ".\n\n")
    exit(0)
else:
    for file in argv[1:]:
        files.append(file)

if files==[]:
    print(Fore.GREEN + "    Usage:" + Fore.RESET + " smdcut.exe <file1> <file2> <file3> ...")
    print("    Or you can simply drag and drop the files you want to cut into " + Fore.GREEN + "smdcut.exe" + Fore.RESET + ".\n\n\n")
    exit(1)

print(Fore.YELLOW + "INFO" + Fore.RESET + ": GoldSrc supports a maximum of 4080 triangles!\n")
max_triangles = input("How many triangles should a file have at most? (3000 recommending)  "+ Fore.GREEN)
if max_triangles=="": max_triangles = 3000
else: max_triangles = int(max_triangles)
print(Fore.RESET)

def cut(filename, total, this):
    ismesh=False
    refcon = []
    pref = []
    suffix = "end\n"

    with open(filename, "r") as f:
        refcon = f.readlines()

    for l in refcon:
        if "triangles" in l:
            ismesh=True
            pi = refcon.index(l)
            pref = refcon[:pi] + ["triangles\n"]
            refcon = refcon[pi + 1 :]
            refcon.pop()
            break

    num_triangles = len(refcon) // 4

    if not ismesh:
        print('"'+Fore.RED+path.basename(filename)+Fore.RESET+f'" is not a reference file. ({str(this)}/{str(total)})')
        return
    elif num_triangles<=max_triangles:
        print('"'+Fore.LIGHTMAGENTA_EX+path.basename(filename)+Fore.YELLOW+f'": cuting not needed, mesh fits into limit.{Fore.RESET} ({str(this)}/{str(total)})')
        return
    else:
        print('Cuting "'+Fore.LIGHTBLUE_EX+path.basename(filename)+Fore.RESET+f'"...')

    num_files = (num_triangles + max_triangles - 1) // max_triangles

    i = 0
    while i < num_files:
        print(\
            "Writing \""+
            path.basename(filename).replace(".SMD", "").replace(".smd", "") + "_P" + str(i + 1) + ".smd"+
            '"'
            )
        with open(filename.replace(".SMD", "").replace(".smd", "") + "_P" + str(i + 1) + ".smd", "w") as f:
            start = i * max_triangles * 4
            end = min(start + (max_triangles * 4), len(refcon))
            f.writelines(pref + refcon[start:end] + [suffix])
        i += 1

    print(Fore.GREEN + f"\"{path.basename(filename)}\" successfuly cuted, {num_files} files created.  ({str(this)}/{str(total)})" + Fore.RESET)
    print(Fore.YELLOW + "INFO" + Fore.RESET + ": You can copy this lines and paste to .qc file content.")
    i = 0
    while i < num_files:
        print(\
            "$body \"studio\" \""+
            path.basename(filename).replace(".SMD", "").replace(".smd", "") + "_P" + str(i + 1)+
            '"'
            )
        i+=1
    print("\n")

for fi in range(0, len(files)):
    cut(files[fi], len(files), fi+1)

system("pause")