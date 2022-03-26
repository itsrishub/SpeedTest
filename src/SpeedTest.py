import tkinter
import tkinter.messagebox
import customtkinter
import sys
import os
import threading
from random import shuffle
from time import perf_counter as time
from time import sleep

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class DiskSpeed:
    def __init__(self, path, blocks_count=128, block_size=1048576):
        self.path = path+"\\DiskSpeedTest"
        self.results = {}
        self.get_write_speed(blocks_count, block_size)
        self.get_read_speed(blocks_count, block_size)
        os.remove(self.path)
        
    def get_write_speed(self, blocks_count, block_size):
        f = os.open(self.path, os.O_CREAT | os.O_WRONLY, 0o777)
        w_times = []
        for i in range(blocks_count):
            sys.stdout.write('\rWriting: {:.2f} %'.format(
                    (i + 1) * 100 / blocks_count))
            sys.stdout.flush()
            buff = os.urandom(block_size)
            start = time()
            os.write(f, buff)
            os.fsync(f)
            w_times.append(time()-start)
        os.close(f)
        
        write_speed = blocks_count/sum(w_times)
        self.results['Write Speed'] = write_speed
    
    def get_read_speed(self, blocks_count, block_size):
        f = os.open(self.path, os.O_RDONLY, 0o777)
        offsets = list(range(0, blocks_count * block_size, block_size))
        shuffle(offsets)

        r_times = []
        for i, offset in enumerate(offsets, 1):
            start = time()
            os.lseek(f, offset, os.SEEK_SET)
            buff = os.read(f, block_size)
            t = time() - start
            if not buff: 
                break
            r_times.append(t)
        os.close(f)
        
        read_speed = blocks_count/sum(r_times)
        self.results['Read Speed'] = read_speed



class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("SpeedTest")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="SpeedTest",
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=2, column=0, pady=10, padx=20)

        for i in [0, 1, 2, 3]:
            self.frame_right.rowconfigure(i, weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")


        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Test speed of storage unit.\n~by Rishub",
                                                   height=80,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="we", padx=15, pady=15)

        

        

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Test",
                                                command=self.test)
        self.button_5.grid(row=7, column=1, pady=20, padx=20, sticky="w")

        self.switch_2.select()

    def foo(self):
        drive_name = ""
        disk_speed = DiskSpeed(drive_name)
        results = disk_speed.results
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Testing",
                                                   height=80,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="we", padx=15, pady=15)
        progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        progressbar.set(0)
        
        for i in range(0, 11, 1):
            progressbar.set(i/10)
            sleep(0.2)
        progressbar.grid_forget()
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="\n\tResult\n\nWrite Speed: {:.2f} MB/s\n\n".format(results['Write Speed']) +
                                                        "Read Speed: {:.2f} MB/S\n".format(results['Read Speed']),
                                                   height=80,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="we", padx=15, pady=15)

    def test(self):
        
        threading.Thread(target=self.foo).start()

        
    

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()