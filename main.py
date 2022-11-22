import glob, os


class Base:
    # Foreground:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    NC = '\x1b[0m'  # No Color


def get_files(match=None):
    files = []
    os.chdir("presets")
    for f in glob.glob("*.syx"):
        if match is not None:
            if match in f:
                files.append(f)
        else:
            files.append(f)
    return files


def read_file(path):
    with open(path, mode='rb') as file:
        return file.read()


def read_bytes(path):
    bytes = []
    with open(path, "rb") as f:
        while (byte := f.read(1)):
            bytes.append(int.from_bytes(byte, 'little'))
    return bytes


if __name__ == "__main__":
    files = get_files("Preset_6")
    files.sort()
    color = read_bytes(files[0])
    for f in files:
        bytes = read_bytes(f)
        for i in range(len(bytes)):
            if color[i] != bytes[i]:
                color[i] = None

    for f in files:
        bytes = read_bytes(f)
        print(f)
        print('[ ', end='')
        count = 0
        i = 0
        i_total = 0
        first = True
        while bytes:
            # print(i)
            b = bytes.pop(0)
            use_color = Base.NC
            if b in [0xf0, 0xf7]:  # sysex header
                use_color = Base.WARNING
            elif i in [1, 2, 3, 4, 5]:  # ID
                use_color = Base.OKBLUE
            elif color[i_total] is not None:  # duplicates
                use_color = Base.OKGREEN
            if not first and i == 108:  # checksum
                use_color = Base.FAIL
            string = ""
            if first and i >= 11 and i <= 21 and b >= 32 and b <= 126:
                string = '%c  ' % (chr(b))
            else:
                string = '%02x ' % (b)
            print(use_color + string + Base.END, end='')
            count += 1
            if count >= 32:
                count = 0
                print('')
                print('  ', end='')
            i += 1
            i_total += 1
            if b == 0xf7:
                i = 0
                first = False
        print(']')
