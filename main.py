import array as arr
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import customtkinter
import tkinter
from tkinter import*
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo

from datetime import datetime

customtkinter.set_ctk_parent_class(tkinter.Tk)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

padX = 5
padY = 5

root = customtkinter.CTk()
root.geometry("1280x780")
root.title("DDG GRIN-TEX APP")

print(type(root), isinstance(root, tkinter.Tk))
useFilePath = ""
CurrentFileName = ""
calibr = 1
avg_print = True
add_plot = False

TokH = 309
coordsY = arr.array('f')
coordsX = arr.array('f')

interval_from = 0
interval_to = 0

coordsAvgX = arr.array('f')
coordsAvgY = arr.array('f')

max_point = 0
min_point = 0xffffffff

head = customtkinter.CTkFrame(master=root)
head.pack(padx=padX, pady=padY, side=TOP)


# _______________________________UI design_________________________________
# _________________________________HEAD____________________________________
btn = customtkinter.CTkButton(master=head, text="Выбрать файл")
btn.pack(padx=padX, pady=padY, side=LEFT)

but_print_plot = customtkinter.CTkButton(master=head, text="Нарисовать график")
but_print_plot.pack(padx=padX, pady=padY, after=btn, side=LEFT)

delimetr1 = customtkinter.CTkFrame(master=head, height=30, width=3, fg_color="white")
delimetr1.pack(padx=padX, pady=padY, after=but_print_plot, side=LEFT)

input_label = customtkinter.CTkLabel(master=head, text="Калибровочное значение")
input_label.pack(padx=padX, pady=padY, after=delimetr1, side=LEFT)

input_hz = customtkinter.CTkEntry(master=head, width=50)
input_hz.pack(padx=padX, pady=padY, after=input_label, side=LEFT)

delimetr2 = customtkinter.CTkFrame(master=head, height=30, width=3, fg_color="white")
delimetr2.pack(padx=padX, pady=padY, after=input_hz, side=LEFT)

# _________________________________PLOT____________________________________
plotBorder = customtkinter.CTkFrame(master=root, height=500, width=2000)
plotBorder.pack(after=head, padx=padX, pady=padY, side=TOP)

fig = Figure(figsize=(19, 6), dpi=100)
ax = fig.add_subplot(1,1,1)
fig.patch.set_facecolor("#242424")
canvas = FigureCanvasTkAgg(fig, master=plotBorder)
toolbar = NavigationToolbar2Tk(canvas, plotBorder).pack(padx=padX, pady=padY, side=BOTTOM)
# range_frame.pack_configure()

# _________________________________RANGE___________________________________
range_frame = customtkinter.CTkFrame(master=root)
range_frame.pack(padx=padX, pady=padY, after=plotBorder, side=LEFT)
btn_set_range = customtkinter.CTkButton(master=range_frame, text="Сократить график", width=160)
btn_set_range.pack(padx=padX, pady=padY, side=BOTTOM)

range_label_from = customtkinter.CTkLabel(master=range_frame, text="От")
range_label_from.pack(padx=padX, pady=padY, side=LEFT)

input_range_from = customtkinter.CTkEntry(master=range_frame, width=50)
input_range_from.pack(after=range_label_from, padx=padX, pady=padY, side=LEFT)

range_label_to = customtkinter.CTkLabel(master=range_frame, text="До")
range_label_to.pack(after=input_range_from, padx=padX, pady=padY, side=LEFT)

input_range_to = customtkinter.CTkEntry(master=range_frame, width=50)
input_range_to.pack(after=range_label_to, padx=padX, pady=padY, side=LEFT)

btn_save_file = customtkinter.CTkButton(master=range_frame, text="Сохранить интервал", width=160)
btn_save_file.pack(after=btn_set_range,padx=padX, pady=padY, side=BOTTOM)

# ________________________________FILTERS___________________________________
but_avg = customtkinter.CTkButton(master=root, text="Скользящее среднее")
but_avg.pack(padx=padX, pady=padY)
# _______________________________MAIN_DATA___________________________________

info_frame = customtkinter.CTkFrame(master=root)
info_frame.pack(padx=padX, pady=padY, after=range_frame, side=LEFT)

min_coord_lbl = customtkinter.CTkLabel(master=info_frame, text="Минимум:")
min_coord_lbl.pack(padx=padX, pady=padY, side=LEFT)

min_coord = customtkinter.CTkLabel(master=info_frame, text="1000")
min_coord.pack(padx=padX, pady=padY, after=min_coord_lbl, side=LEFT)

max_coord_lbl = customtkinter.CTkLabel(master=info_frame, text="Максимум:")
max_coord_lbl.pack(padx=padX, pady=padY, side=LEFT)

max_coord = customtkinter.CTkLabel(master=info_frame, text="1000")
max_coord.pack(padx=padX, pady=padY, after=max_coord_lbl, side=LEFT)

def checkbutton_changed():
    if enabled.get() == 1:
        showinfo(title="DDG SETTINGS", message="Наложение графиков включено")
    else:
        showinfo(title="DDG SETTINGS", message="Наложение графиков отключено")
 
enabled = IntVar()
  
enabled_checkbutton = customtkinter.CTkSwitch(master=head, text="Наложение графиков", variable=enabled, command=checkbutton_changed)
enabled_checkbutton.pack(after=delimetr2, padx=padX, pady=padY, side=LEFT)

but_clear = customtkinter.CTkButton(master=head, text="Отчистить")
but_clear.pack(padx=padX, pady=padY, after=enabled_checkbutton, side=LEFT)
def _quit():
    root.quit()  # остановка цикла
    root.destroy()  # закрытие приложения

def show_file_name():
    btn.configure(text = CurrentFileName)

def avg():
    sum = 0
    if useFilePath!="":
        global coordsAvgX
        del coordsAvgX[:]
        print_avg_plot()
        
def click_file_path():
    filePath = filedialog.askopenfiles(title="Выбор файла", defaultextension="bin")
    fileType = filePath[0].name
    fileType = fileType[len(fileType)-3:len(fileType)]

    if fileType == "bin":
        global useFilePath 
        useFilePath = filePath[0].name
        print("file path: " + useFilePath)
        print(type(useFilePath))
        count = 0
        for i in range(len(useFilePath)):
            if useFilePath[i] == '/' :
                count = i
        global CurrentFileName
        CurrentFileName = useFilePath[count:len(useFilePath)]
        show_file_name()

def open_file():
    print("file path: " + useFilePath)
    try:
        text = open(useFilePath,'rb')
    except FileNotFoundError:
        return
    bytes = text.read()
    count = 0
    del coordsX[:]
    del coordsY[:]
    coordsX.append(0)
    text.close()
    for i in range(0, len(bytes), 4):

        if (bytes[i] & 0b10000000) == 0x10000000 :
            dec = bytes[i] << 16
            dec = dec | (bytes[i + 1] << 8) | (bytes[i + 2] - 0b00000001)
            dec = dec ^ 0xffffff
        else:
            dec = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2]
            dec = dec >> 6
        count = count + 1
        coordsY.append(dec)
        if dec > max_point: max_point = dec
        if dec < min_point: min_point = dec

        if count % 15 == 0:
            coordsX.append(int(count /15))
        else:
            coordsX.append(coordsX[len(coordsX)-1] + 0.06)
        
    coordsX.pop(len(coordsX)-1)
    print("coordsX size: " + str(len(coordsX)) + "coordsY size: " + str(len(coordsY)))
    min_coord.configure(text=min_coord)
    max_point.configure(text=max_coord)

def open_file_with_calibr():
    global max_point, min_point
    max_point = 0
    min_point = 0xffffffff
    print("file path: " + useFilePath)
    try:
        text = open(useFilePath,'rb')
    except FileNotFoundError:
        return

    bytes = text.read()
    count = 0
    del coordsX[:]
    del coordsY[:]
    coordsX.append(0)

    text.close()

    name = useFilePath[0:len(useFilePath)-4]
    name +=".csv"
    f = open(name, "w")
    for i in range(0, len(bytes), 4):

        if (bytes[i] & 0b10000000) == 0x10000000 :
            dec = bytes[i] << 16
            dec = dec | (bytes[i + 1] << 8) | (bytes[i + 2] - 0b00000001)
            dec = dec ^ 0xffffff
        else:
            dec = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2]
            dec = dec >> 6
        count = count + 1
        dec = dec / calibr
        coordsY.append(dec)
        
        if dec > max_point: max_point = dec
        if dec < min_point: min_point = dec

        f.write(str(int(dec)) +'\n')
        if count % 15 == 0:
            coordsX.append(int(count /15))
        else:
            coordsX.append(coordsX[len(coordsX)-1] + 0.06)
    f.close()   
    coordsX.pop(len(coordsX)-1)
    print("coordsX size: " + str(len(coordsX)) + "coordsY size: " + str(len(coordsY)))
    min_coord.configure(text=min_point)
    max_coord.configure(text=max_point)

def print_plot():
    if input_hz.get == "":
        open_file()
    else :
        global calibr
        try:
            calibr = int(input_hz.get())
        except ValueError:
            input_hz.configure(textvariable=1)
            input_hz.update()
        open_file_with_calibr()
        if enabled.get() != True:
            ax.clear()
    ax.set_facecolor("#242424")
    ax.plot(coordsX, coordsY, linewidth=2, markersize=2, markerfacecolor='white', 
        label=useFilePath)
    ax.grid(color='white', linewidth=0.4)
    ax.legend(fontsize=12)
    ax.tick_params(labelcolor='white')
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def print_avg_plot():
    ax.plot(coordsAvgX, coordsY, linewidth=3, markersize=5, markerfacecolor='r', 
        label="AVG")
    canvas.draw()

def graph_range():
    global interval_from
    global interval_to
    try:
        range_f = float(input_range_from.get())
        range_t = float(input_range_to.get())
    except ValueError:
        showinfo(title="Error", message="Недопустимый симмвол")
        input_range_from.delete(0,END)
        input_range_from.insert(0,int(coordsX[0]))

        input_range_to.delete(0,END)
        input_range_to.insert(0,int(coordsX[len(coordsX)-1]))
    if len(coordsX) > 2:
        print(len(coordsX))
        ax.clear()
        if range_f < range_t:
            ax.plot(coordsX[coordsX.index(range_f):coordsX.index(range_t)], 
                coordsY[coordsX.index(range_f):coordsX.index(range_t)], 
                linewidth=3, markersize=5, markerfacecolor='b', 
                label=useFilePath)
            interval_from = range_f
            interval_to = range_t
        else:
            ax.plot(coordsX[coordsX.index(range_t):coordsX.index(range_f)], 
                coordsY[coordsX.index(range_t):coordsX.index(range_f)], 
                linewidth=3, markersize=5, markerfacecolor='b', 
                label=useFilePath)
            interval_from = range_t
            interval_to = range_f
        ax.grid(color='white', linewidth=0.4)
        ax.legend(fontsize=12)
        ax.tick_params(labelcolor='white')
        canvas.draw()

def save_interval_csv():
    saveFileName = filedialog.asksaveasfilename(initialfile="DDG_data_" + datetime.strftime(datetime.now(), '%d-%m-%Y'),
                                                )
    saveFile = open(saveFileName, "w")
    for i in range(interval_from, interval_to, 1):
        saveFile.write(str(coordsX[i]) + '\n')
    saveFile.close()

def clear_plot():
    ax.clear()
    ax.grid(color='white', linewidth=0.4)
    ax.legend(fontsize=12)
    ax.tick_params(labelcolor='white')
    canvas.draw()

btn.configure(command=click_file_path)
but_print_plot.configure(command=print_plot)
but_avg.configure(command=avg)
btn_set_range.configure(command=graph_range)
btn_save_file.configure(command=save_interval_csv)
but_clear.configure(command=clear_plot)
print_plot()
root.mainloop()





# name = 'Logs_00003'
    # plt.plot(coordsY)