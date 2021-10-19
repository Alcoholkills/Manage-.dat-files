from tkinter import filedialog
import tkinter, os, sys, pprint, re, traceback


def get_file():
    root = tkinter.Tk()
    root.withdraw()
    return filedialog.askopenfile(initialdir=os.getcwd(), filetypes=[("Dat files", ".dat")])

# USELESS
def loop_file(f):
    while True:
        line = f.readline()
        if not line:
            break
    f.close()


def create_dictionnary_of_meta_data(f):
    d = dict()
    f.seek(0, 0)
    while True:
        line = f.readline()
        if not line:
            break
        if "METADATA|" in line:
            d[line]=list()
    return d

def create_out_file(file_name):
    try:
        with open(f"{file_name}.dat", "x"):
            print("File created")
    except FileExistsError:
        print("File already exists")
    finally:
        return file_name

def get_current_dict_as_string(dictonnary):
    s = ""
    for key in dictonnary:
        temp = key.replace('\n','')
        s += f"{temp}\n"
        for value in dictonnary[key]:
            temp = value.replace('\n','')
            s += f"{temp}\n"
        s+="\n"
    return s

def add_user_to_dict(user_input, dictionnary, file):
    current_metada = ""
    file.seek(0, 0)
    while True:
        line = file.readline()
        if not line:
            break
        if "METADATA|" in line:
            current_metada = line
            if current_metada not in dictionnary:
                print("add_user_to_dict(metadata not in dictionnay of meta data)")
                raise
        if user_input in line:
            dictionnary[current_metada].append(user_input)

def write_string_to_file(file_name, string):
    with open(f"{file_name}.dat", "w") as f:
            f.write(string)

def check_file_name(name):
    l = [i for i in name]
    l_res = list()
    lever = True
    for char in l:
        if char.isalnum() or char in ["-","_"]:
            l_res.append(char)
            lever = True
        elif char == " " and lever == True:
            lever = False
            l_res.append(char)
    if l_res:
        return "".join(l_res)
    else:
        return "output_file"
            
    

def main():
    try:
        pp = pprint.PrettyPrinter(indent=4)
        f = get_file()
        d = create_dictionnary_of_meta_data(f)
        file_name_default = "output_file"
        regex_save_file = "save[0-9]+.dat$"
        help_string = "\
            <Commandes> --------------\n\
            \t'h' to display help\n\
            \t'd' to display current data model\n\
            \t'e' to parse another file\n\
            \t'f' to print active file\n\
            \t'b' to display history\n\
            \t'n' to change file output name (default 'output_file')\n\
            \t's' to create a save\n\
            \t'sd' to delete a save\n\
            \t'sdd' to delete all saves\n\
            \t'q' to exit\n\
            \t'x' to save and exit\n\
            \twhatever else to look it up in file\n\
            --------------------------"
        print(help_string)
        history = list()
        while True:
            s = input("Enter une commande ('-h' for help) ou un pattern a chercher dans le document: ")
            if  s == 'b':
                for item in history[::-1]:
                    print(item)
            elif s == "d":
                pp.pprint(d)
            elif s == "e":
                f.close()
                f = get_file()
            elif s == "f":
                print(os.path.basename(f.name))
            elif s == "h":
                print(help_string)
            elif s == "n":
                file_name_to_be_checked = input("Enter un nome de fichier valide: ")
                file_name_default = check_file_name(file_name_to_be_checked)
                print(f"Output file name changed to: {file_name_default}")
            elif s == "s":
                saves = [-1]
                for file in os.listdir('.'):
                    first_regex = re.compile(regex_save_file).match(file)
                    if first_regex == None:
                        continue
                    found_regex = re.compile(r"\d+").findall(first_regex.group())
                    if found_regex:
                        saves.append(int(found_regex[0]))
                save_name = f"save{max(saves) + 1}"
                s = get_current_dict_as_string(d)
                n = create_out_file(save_name)
                write_string_to_file(n, s)
                print(f"Data written to {n}")
                
            elif s == "sd":
                list_saves = list()
                for file in os.listdir('.'):
                    if re.search(regex_save_file,file):
                        list_saves.append(f"{len(list_saves)} -\t{file}")    
                while list_saves:
                    print("--"*25)
                    for save in list_saves:
                        print(save)
                    to_delete = int(input("Selectionner la sauvegarde a effacer (0, 1, 2 ...). Taper -1 pour annuler.\n"))
                    if to_delete > to_delete:
                        continue
                    elif to_delete < 0:
                        break
                    else:
                        try:
                            file_to_delete = list_saves.pop(to_delete)
                            os.remove(re.search(regex_save_file,file_to_delete).group())
                        except IndexError:
                            print("Index out of range")
                            continue
            elif s == "ssd":
                for file in os.listdir('.'):
                    if re.search(regex_save_file,file):
                        os.remove(file)
            elif s == "q":
                exit()
            elif s == 'x':
                raise KeyboardInterrupt
            elif s == "":
                continue
            else:
                add_user_to_dict(s, d, f)
                history.append(f"{len(history)} -\t{s}")  
    except KeyboardInterrupt:
        s = get_current_dict_as_string(d)
        n = create_out_file(file_name_default)
        write_string_to_file(n, s)
        print(f"Data written to {n}")
        f.close()
    except SystemExit:
        f.close()
    except AttributeError:
        exit()
    except:
        f.close()
        print("Unexpected error:", sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
