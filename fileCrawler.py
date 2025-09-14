#!/usr/bin/env python
import os
import pydoc
import shlex
from pathlib import Path


class Globals:
    cwd = os.getcwd()
    file = None
    skip = False


def ListDirs(g):
    dirs = [d for d in os.listdir(g.cwd) if os.path.isdir(os.path.join(g.cwd, d))]
    for dirname in dirs:
        print(f"-> {dirname} ")


def DeleteFile(g):
    movieExts = {
        ".mp4",
    }
    extension = os.path.splitext(g.file)[1]
    if extension in movieExts:
        print("This file seems to have a video extension, are you sure you want to delete it? (y/n)")
        if input("> ") == 'n':
            g.skip = False
            return
    os.remove(g.file)
    print(f"Deleted {g.file}")
    g.skip = True
    return


def CreateFolder(g):
    fname = None
    while True:
        try:
            fname = input("Name New Folder> ")
            if fname == 'q':
                break
            os.mkdir(fname)
        except FileExistsError:
            print("Folder Exists already, try again or quit folder creation (q)")
            continue
        os.rename(os.path.join(g.cwd, g.file), os.path.join(g.cwd, fname, g.file))
        break
    return


def RenameFile(g):
    extension = os.path.splitext(g.file)[1]
    print("\033[1;33mDo not include file extension\033[0m")
    while True:
        try:
            fileName = input("RenameFile> ") + extension
            os.rename(os.path.join(g.cwd, g.file), os.path.join(g.cwd, fileName))
        except FileNotFoundError:
            print("File Naming error, Use a valid Name")
            continue
        break
    print(f"File renamed to {fileName}")


def Skip(g):
    g.skip = True


def PrintFile(g):
    path = Path(os.path.join(g.cwd, g.file))
    text = path.read_text(encoding="utf-8", errors="replace")
    pydoc.pager(text)


def Open(g):
    os.system(f"xdg-open {shlex.quote(os.path.join(g.cwd, g.file))}")


def Quit(g):
    exit(0)


def Help(g):
    print("\033[1;34mOptions:\033[0m")
    print(f"\033[37m(l) list directories in {g.cwd} \033[0m")
    print("\033[37m(d) delete file\033[0m")
    print("\033[37m(c) create new folder for file\033[0m")
    print("\033[37m(r) rename file\033[0m")
    print("\033[37m(s) skip file / done\033[0m")
    print("\033[37m(p) list file contents\033[0m")
    print("\033[37m(o) open file\033[0m")
    print("\033[37m(q) quit\033[0m")
    print("\033[1;34mFile:\033[0m", g.file)


def main():
    commands = {
        'l': ListDirs,
        's': Skip,
        'd': DeleteFile,
        'c': CreateFolder,
        'r': RenameFile,
        'p': PrintFile,
        'h': Help,
        'o': Open,
        'q': Quit
    }
    g = Globals()

    cwd = os.getcwd()

    dirnames = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]

    print("\033[1;34mChoose which directory to start crawling, or input . for the current directory:\033[0m");
    ListDirs(g)

    root = input("Folder to crawl: ")
    g.cwd = os.path.join(g.cwd, root)

    filenames = [f for f in os.listdir(root) if os.path.isfile(os.path.join(g.cwd,f))]

    # Movie Name (year).filetype
    for filename in filenames:
        g.skip = False
        g.file = filename
        Help(g)
        while True:
            command = input(f"{g.file}> ")
            if command not in commands:
                print("Invalid command, \'h\' for help")
                continue
            commands[command](g)
            if g.skip:
                break
    return


main()
