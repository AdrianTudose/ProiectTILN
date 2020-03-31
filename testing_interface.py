import tkinter as tk

from main import preprocesare, analiza_semantica

propozitii = list()
positions = list()
width = 0

root = tk.Tk()
topframe = tk.Frame(root)
topframe.pack(pady=20, padx=20, expand=True, fill='both')

text1 = tk.Text(topframe, height=10, width=70)
scroll = tk.Scrollbar(topframe, command=text1.yview)
text1.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text1.pack(expand=True, fill='both')

b = tk.Button(root, text="EXTRACT")
b.pack()

bottomframe = tk.Frame(root)
bottomframe.pack(pady=20, padx=20, expand=True, fill='both')

text2 = tk.Text(bottomframe, height=10, width=70)
scroll = tk.Scrollbar(bottomframe, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text2.pack(expand=True, fill='both')

def highlight(start, end):
    text2.tag_add("highlight", start, end)
    text2.tag_config("highlight", background="pale green")


def run_app():
    global propozitii,positions
    text_input = text1.get("1.0", 'end-1c')

    propozitii = preprocesare(text_input)

    positions = analiza_semantica(propozitii)

    update_text("null")


def update_text(event):
    global width,propozitii,positions
    if event!="null":
        width = event.width
    if len(propozitii)>0:
        print("ok")
        text = ""
        text_cuvinte = ""
        text_pv = ""

        current_pos = 0
        current_line = 1

        for propozitie in propozitii:
            for x in propozitie:
                if(x[1]!="ALINIERE"):
                    word_width = max(len(x[0]),len(x[1])) + 4
                    if current_pos + word_width > width/8:
                        text += text_pv + "\n" + text_cuvinte + "\n\n"
                        text_cuvinte = ""
                        text_pv = ""
                        current_pos = 0
                        current_line += 3
                    text_cuvinte += ("{:<" + str(word_width) + "}").format(x[0])
                    text_pv += ("{:<" + str(word_width) + "}").format(x[1])
                    start_index1 = "1.0 + " + str(current_line) + " lines + " + str(current_pos) + " chars"
                    end_index1 = "1.0 + " + str(current_line) + " lines + " + str(current_pos + word_width - 4) + " chars"
                    start_index2 = "1.0 + " + str(current_line-1) + " lines + " + str(current_pos) + " chars"
                    end_index2 = "1.0 + " + str(current_line-1) + " lines + " + str(current_pos + word_width - 4) + " chars"
                    if len(x)==2:
                        x.append([start_index1,start_index2])
                        x.append([end_index1,end_index2])
                    else:
                        x[2]=[start_index1,start_index2]
                        x[3]=[end_index1,end_index2]
                    current_pos += word_width
        text += text_pv + "\n" + text_cuvinte + "\n\n"

        text2.config(state=tk.NORMAL)
        text2.delete('1.0', tk.END)
        text2.insert(tk.END, text, 'color')
        text2.config(state=tk.DISABLED)

        for position in positions:
            print("".join(
                [x[0] for x in [propozitii[position[1][0]][y] for y in range(position[1][1], position[1][-1] + 1)]]))
            highlight(propozitii[position[1][0]][position[1][1]][2][0], propozitii[position[1][0]][position[1][-1]][3][0])
            highlight(propozitii[position[1][0]][position[1][1]][2][1], propozitii[position[1][0]][position[1][-1]][3][1])

        text2.config(state=tk.DISABLED)

text2.bind( "<Configure>", update_text)
b["command"] = run_app
root.mainloop()
