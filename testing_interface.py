import tkinter as tk

from main import preprocesare, analiza_semantica, TIP_PUNCTUATIE

root = tk.Tk()
topframe = tk.Frame(root)
topframe.pack(pady=20,padx=20,expand=True, fill='both')

text1 = tk.Text(topframe, height=10, width=70)
scroll = tk.Scrollbar(topframe, command=text1.yview)
text1.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text1.pack(expand=True, fill='both')

b = tk.Button(root, text="EXTRACT")
b.pack()

bottomframe = tk.Frame(root)
bottomframe.pack(pady=20,padx=20,expand=True, fill='both')

text2 = tk.Text(bottomframe, height=10, width=70)
scroll = tk.Scrollbar(bottomframe, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text2.pack(expand=True, fill='both')


def highlight(start,end):
    text2.tag_add("highlight", "1."+str(start), "1."+str(end))
    text2.tag_config("highlight", background="pale green")

def run_app():
    text = ""
    propozitii = preprocesare(text1.get("1.0",'end-1c'))
    for propozitie in propozitii:
        text += " ".join([x[0] + "{" + x[1] + "}" if x[1] != TIP_PUNCTUATIE else "" for x in propozitie])

    sequences,positions = analiza_semantica(propozitii)

    text2.config(state=tk.NORMAL)
    text2.delete('1.0', tk.END)
    text2.insert(tk.END, text, 'color')
    text2.config(state=tk.DISABLED)

    print(*sequences,sep="\n")
    for position in positions:
        highlight(position[0],position[1])


b["command"] = run_app
root.mainloop()

