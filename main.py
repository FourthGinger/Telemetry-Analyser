import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

from tkinter import Tk, Frame, Label, Entry, Button, IntVar, StringVar, filedialog, Checkbutton

from file_handler import FileHander, Telemetry, Channels

class GUI:

    def __init__(self):
        self.win = Tk()
        self.win.title("GUI")
        self.win.geometry("1000x700")
        self.filePath = ""

        self.OpeningFrame()

        self.win.mainloop()

    def OpeningFrame(self):
        self.opening_frame = Frame(self.win)

        self.opening_frame.grid(column=0, row=0, sticky="nsew")
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)

        openFileButton = Button(self.opening_frame, text="Open file", command=self.openFile, width=25, height=5)
        openFileButton.place(relx=0.4, rely=0.6, anchor="center")

        analyseButton = Button(self.opening_frame, text="Analyse", command=self.MainFrame, width=25, height=5)
        analyseButton.place(relx=0.6, rely=0.6, anchor="center")

    def MainFrame(self):
        if self.filePath == "":
             tempLabel = Label(self.opening_frame, text="No File Selected", width=25, height=5)
             tempLabel.place(relx=0.6, rely=0.6, anchor="center")
             tempLabel.after(2000, tempLabel.destroy)
        else:
            self.opening_frame.grid_remove()
            self.main_frame = Frame(self.win)
            
            self.main_frame.grid(column=0, row=0, sticky="nsew")
            self.win.grid_rowconfigure(0, weight=1)
            self.win.grid_columnconfigure(0, weight=1)

            backButton = Button(self.main_frame, text="Back", command=self.BackToOpening, width=15, height=2)
            backButton.place(relx=0.02, rely=0.02, anchor="nw")

            sampleRateLabel = Label(self.main_frame, text=f"File Name: {self.fileName}")
            sampleRateLabel.place(relx=0.005, rely=0.15, anchor="w")

            sampleRateLabel = Label(self.main_frame, text=f"Sample Rate: {self.sampleRate}Hz")
            sampleRateLabel.place(relx=0.005, rely=0.2, anchor="w")


            channelFrame = Frame(self.main_frame)
            channelFrame.place(relx=0.02, rely=0.28, anchor="nw")

            Label(channelFrame, text="Channels:").pack(anchor="w")

            self.channel_vars = {}

            for channel in self.channels:
                self.channel_vars[channel] = IntVar(
                    value=1 if channel == "corrspeed" else 0
                )

                display_name = channel.replace("_", " ").title()

                Checkbutton(
                    channelFrame,
                    text=display_name,
                    variable=self.channel_vars[channel],
                    command=self.UpdateGraph
                ).pack(anchor="w")


            self.figure = plt.Figure(figsize=(8, 5), dpi=100)
            self.axis = self.figure.add_subplot(111)

            self.canvas = FigureCanvasTkAgg(
                self.figure,
                master=self.main_frame
            )
            self.canvas.draw()
            self.canvas.get_tk_widget().place(
                relx=0.6,
                rely=0.5,
                anchor="center"
            )

            self.UpdateGraph()

            

    def BackToOpening(self):
        self.main_frame.grid_remove()
        self.opening_frame.grid(column=0, row=0, sticky="nsew")

    def openFile(self):
            self.filePath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

            if self.filePath == "":
                 pass
            else:
                self.sampleRate, self.fileName = FileHander(self.filePath)

                self.channels = Channels(self.filePath)

                self.telemetry = Telemetry(
                self.filePath,
                self.channels
)

    def UpdateGraph(self):
        self.axis.clear()

        selected_channels = [
            channel
            for channel, var in self.channel_vars.items()
            if var.get() == 1
        ]

        for channel in selected_channels:
            self.axis.plot(
                self.telemetry[channel],
                label=channel.replace("_", " ").title()
            )

        self.axis.set_xlabel("Sample")
        self.axis.set_title("Telemetry")

        self.axis.yaxis.set_major_locator(MaxNLocator(nbins=6))

        if selected_channels:
            self.axis.legend()

        self.canvas.draw()


gui = GUI()
