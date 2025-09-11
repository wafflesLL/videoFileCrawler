import os


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
    if movieExts[extension]:
        print("This file seems to be a have a video extension, are you sure you want to delete it? (y/n)")
        if input("> ") == 'n':
            g.skip = False
            return
    os.remove(g.file)
    print(f"Deleted {g.file}")
    g.skip = True
    return


def CreateFolder(g):
    ListDirs(g.cwd)


def RenameFile(g):
    ListDirs(g.cwd)


def Skip(g):
    g.skip = True


def PrintFile(g):
    ListDirs(g.cwd)


def main():
    commands = {
        'l': ListDirs,
        'd': DeleteFile,
        'c': CreateFolder,
        'r': RenameFile,
        'p': PrintFile
    }
    g = Globals()

    cwd = os.getcwd()

    dirnames = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]

    print("\033[1;34mChoose which directory to start crawling, or input . for the current directory:\033[0m");
    ListDirs(g)

    root = input("Folder to crawl: ")
    globals = os.path.join(g.cwd, root)

    filenames = [f for f in os.listdir(root) if os.path.isfile(os.path.join(g.cwd,f))]

    # Movie Name (year).filetype
    for filename in filenames:
        g.skip = False
        print("\033[1;34mOptions:\033[0m")
        print(f"\033[37m(l) list directories in {root} \033[0m")
        print("\033[37m(d) delete file\033[0m")
        print("\033[37m(c) create new folder for file\033[0m")
        print("\033[37m(r) rename file\033[0m")
        print("\033[37m(s) skip file / done\033[0m")
        print("\033[37m(p) list file contents\033[0m")
        print("\033[1;34mFile:\033[0m", filename)
        g.file = filename
        while True:
            command = input("> ")
            commands[command](g)
            if g.skip:
                break
    return


main()
