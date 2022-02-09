# Written by Jake Schwarz

import sys

if len(sys.argv) != 3:
    print("Not the correct amount of arguments. Usage: vm.py [LRU][FIFO] filename")
    quit()

if sys.argv[1] != "LRU" and sys.argv[1] != "FIFO":
    print("Not a valid algorithm. Usage: vm.py [LRU][FIFO] filename")
    quit()

with open(sys.argv[2]) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

# with open("input.p443") as file:
#     lines = file.readlines()
#     lines = [line.rstrip() for line in lines]

# print(lines)
# print(len(lines))

# algorithm = "FIFO"
# algorithm = "LRU"
algorithm = sys.argv[1]
pages_referenced = 0
pages_ever_mapped = 0
page_misses = 0
frames_taken = 0
frames_written_disk = 0
frames_recovered_disk = 0
CLOCK = 0
DEBUG = 0
frame_table = []
page_table = []


# Frame object
class Frame:
    def __init__(self, number):
        self.number = number
        self.inuse = 0
        self.dirty = 0
        self.firstuse = 0
        self.lastuse = 0


# Page object. framenum = -1 means the frame is unassigned
class Page:
    def __init__(self, number):
        self.number = number
        self.type = "UnMapped"
        self.ondisk = 0
        self.framenum = -1


frames_num = 0
for line in lines:
    if line[0] != "#":
        break
    frames_num += 1
    # print(line[0])

number_of_frames = int(lines[frames_num])
number_of_pages = int(lines[frames_num+1])
# print(lines[frames_num])

for i in range(0, number_of_frames):
    frame_table.append(Frame(i))

for i in range(0, number_of_pages):
    page_table.append(Page(i))

print("Num frames: " + str(number_of_frames))
print("Num pages: " + str(number_of_pages))
print("Reclaim algorithm: " + algorithm)


def print_output():
    print("Frames")
    for frame in frame_table:
        print("%5d inuse:%d  dirty:%d  first_use:%7d  last_use:%7d" % (frame.number, frame.inuse, frame.dirty, frame.firstuse, frame.lastuse))
    print("Pages")
    for page in page_table:
        if page.framenum != -1:
            print("%5d type:%8s  ondisk:%d  frame_num:%d" % (page.number, page.type, page.ondisk, page.framenum))
        else:
            print("%5d type:%8s  ondisk:%d  frame_num:(unassigned)" % (page.number, page.type, page.ondisk))
    print("Pages referenced: %2d" % pages_referenced)
    print("Pages ever mapped: %2d" % pages_ever_mapped)
    print("Page misses: %2d" % page_misses)
    print("Frames taken: %2d" % frames_taken)
    print("Frames written to disk: %2d" % frames_written_disk)
    print("Frames recovered from disk: %2d" % frames_recovered_disk)


def print_frame(frame):
    print("Frame: %4d inuse:%d  dirty:%d  first_use:%7d  last_use:%7d" % (
        frame.number, frame.inuse, frame.dirty, frame.firstuse, frame.lastuse))


def print_page(page):
    if page.framenum != -1:
        print("Page: %5d type:%8s  ondisk:%d  frame_num:%d" % (page.number, page.type, page.ondisk, page.framenum))
    else:
        print("Page: %5d type:%8s  ondisk:%d  frame_num:(unassigned)" % (page.number, page.type, page.ondisk))


def read(line):
    global DEBUG
    global CLOCK
    global pages_referenced
    global page_misses
    global pages_ever_mapped
    global frames_taken
    global frames_written_disk
    global frames_recovered_disk
    if line[1] == " " and line[2] == " ":
        line_list = line.split("  ")
    else:
        line_list = line.split(" ")
    if DEBUG:
        print("===============================================================================")
        print("Clock: " + str(CLOCK))
        print("Read, %d" % int(line_list[1]))
    page_num = int(line_list[1])
    if page_num > number_of_pages-1:
        print("Not a valid page.")
        exit()
    if page_table[page_num].type == "UnMapped" or page_table[page_num].type == "Taken":
        if page_table[page_num].type == "UnMapped":
            pages_ever_mapped += 1

        available_frame = 0
        available_frame_index = -1
        for (index, frame) in enumerate(frame_table):
            # if DEBUG:
            #     print("Checking frame: " + str(index))
            if frame.inuse == 0:
                available_frame = 1
                available_frame_index = index
                if DEBUG:
                    print("Index of available frame: " + str(available_frame_index))
                break

        if available_frame:
            frame_table[available_frame_index].inuse = 1
            frame_table[available_frame_index].firstuse = CLOCK
            frame_table[available_frame_index].lastuse = CLOCK
            page_table[page_num].type = "Mapped"
            page_table[page_num].framenum = available_frame_index
            page_misses += 1
            if DEBUG:
                print_page(page_table[page_num])
                print_frame(frame_table[available_frame_index])

        else:
            if algorithm == "FIFO":
                frame_index = -1
                low_firstuse = CLOCK
                for (index, frame) in enumerate(frame_table):
                    if frame.firstuse < low_firstuse:
                        low_firstuse = frame.firstuse
                        frame_index = index

            elif algorithm == "LRU":
                frame_index = -1
                low_lastuse = CLOCK
                for (index, frame) in enumerate(frame_table):
                    if frame.lastuse < low_lastuse:
                        low_lastuse = frame.lastuse
                        frame_index = index

            for page in page_table:
                if page.framenum == frame_index:
                    if DEBUG:
                        print("Old page and frame:")
                        print_page(page)
                        print_frame(frame_table[frame_index])
                        print("Taking frame " + str(frame_index) + " from page " + str(page.number) + " for page " + str(page_num))
                    page.framenum = -1
                    if frame_table[frame_index].dirty == 1:
                        page.ondisk = 1
                        frames_written_disk += 1
                    page.type = "Taken"

                    if DEBUG:
                        print("Updated old page and frame: ")
                        print_page(page)
                        print_frame(frame_table[frame_index])
                    break

            frame_table[frame_index].firstuse = CLOCK
            frame_table[frame_index].lastuse = CLOCK
            frame_table[frame_index].dirty = 0
            if page_table[page_num].ondisk == 1:
                frames_recovered_disk += 1
            page_table[page_num].type = "Mapped"
            page_table[page_num].framenum = frame_index
            page_misses += 1
            frames_taken += 1

            if DEBUG:
                print("New page and frame:")
                print_page(page_table[page_num])
                print_frame(frame_table[frame_index])
    else:
        frame_table[page_table[page_num].framenum].lastuse = CLOCK
        if DEBUG:
            print("Page hit with page " + str(page_num))
            print_page(page_table[page_num])
            print_frame(frame_table[page_table[page_num].framenum])

    if DEBUG:
        print("===============================================================================")

    pages_referenced += 1


def write(line):
    global DEBUG
    global CLOCK
    global pages_referenced
    global page_misses
    global pages_ever_mapped
    global frames_taken
    global frames_written_disk
    if line[1] == " " and line[2] == " ":
        line_list = line.split("  ")
    else:
        line_list = line.split(" ")
    if DEBUG:
        print("===============================================================================")
        print("Clock: " + str(CLOCK))
        print("Write, %d" % int(line_list[1]))
    page_num = int(line_list[1])
    if page_num > number_of_pages-1:
        print("Not a valid page.")
        exit()
    if page_table[page_num].type == "UnMapped" or page_table[page_num].type == "Taken":
        if page_table[page_num].type == "UnMapped":
            pages_ever_mapped += 1

        available_frame = 0
        available_frame_index = -1
        for (index, frame) in enumerate(frame_table):
            # if DEBUG:
            #     print("Checking frame: " + str(index))
            if frame.inuse == 0:
                available_frame = 1
                available_frame_index = index
                if DEBUG:
                    print("Index of available frame: " + str(available_frame_index))
                break

        if available_frame:
            frame_table[available_frame_index].inuse = 1
            frame_table[available_frame_index].dirty = 1
            frame_table[available_frame_index].firstuse = CLOCK
            frame_table[available_frame_index].lastuse = CLOCK
            page_table[page_num].type = "Mapped"
            page_table[page_num].framenum = available_frame_index
            page_misses += 1
            if DEBUG:
                print_page(page_table[page_num])
                print_frame(frame_table[available_frame_index])

        else:
            if algorithm == "FIFO":
                frame_index = -1
                low_firstuse = CLOCK
                for (index, frame) in enumerate(frame_table):
                    if frame.firstuse < low_firstuse:
                        low_firstuse = frame.firstuse
                        frame_index = index

            elif algorithm == "LRU":
                frame_index = -1
                low_lastuse = CLOCK
                for (index, frame) in enumerate(frame_table):
                    if frame.lastuse < low_lastuse:
                        low_lastuse = frame.lastuse
                        frame_index = index

            for page in page_table:
                if page.framenum == frame_index:
                    if DEBUG:
                        print("Old page and frame:")
                        print_page(page)
                        print_frame(frame_table[frame_index])
                        print(
                            "Taking frame " + str(frame_index) + " from page " + str(page.number) + " for page " + str(
                                page_num))
                    page.framenum = -1
                    if frame_table[frame_index].dirty == 1:
                        page.ondisk = 1
                        frames_written_disk += 1
                    page.type = "Taken"
                    if DEBUG:
                        print("Updated old page and frame: ")
                        print_page(page)
                        print_frame(frame_table[frame_index])
                    break

            frame_table[frame_index].firstuse = CLOCK
            frame_table[frame_index].lastuse = CLOCK
            page_table[page_num].type = "Mapped"
            page_table[page_num].framenum = frame_index
            page_misses += 1
            frames_taken += 1

            if DEBUG:
                print("New page and frame:")
                print_page(page_table[page_num])
                print_frame(frame_table[frame_index])
    else:
        frame_table[page_table[page_num].framenum].lastuse = CLOCK
        if DEBUG:
            print("Page hit with page " + str(page_num))
            print_page(page_table[page_num])
            print_frame(frame_table[page_table[page_num].framenum])

    if DEBUG:
        print("===============================================================================")

    pages_referenced += 1


# line_num = 0
for line in lines[frames_num+2:]:
    # line_num += 1
    # print("line_num: " + str(line_num))
    # print(line)
    if line[0] == "r":
        read(line)
        CLOCK += 1
    elif line[0] == "w":
        write(line)
        CLOCK += 1
    elif line == "debug":
        DEBUG = 1
        CLOCK += 1
    elif line == "nodebug":
        DEBUG = 1
        CLOCK += 1
    elif line == "print":
        print_output()
        CLOCK += 1
    elif line[0] != "#":
        print("Invalid line.")
        quit()

print_output()
