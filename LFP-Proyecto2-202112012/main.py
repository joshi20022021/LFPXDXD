import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from prettytable import PrettyTable
from analizadorlexico import AnalizadorLexicoSintactico
from analizadorlexico import NoSQLToMongoDBTranslator


class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Analizador Léxico")

        # Estilo de los botones
        BOTON_ESTILO = {
            "font": ('Roboto', 12),
            "background": '#000000',
            "foreground": 'white',
            "width": 10,
            "borderwidth": 0,
            "highlightthickness": 0,
            "padx": 10,
            "pady": 5,
            "relief": tk.FLAT,
        }

        # Crear contenedor del menú
        self.menu = tk.Frame(master, bg="gray", width=150)  # Ancho fijo del contenedor
        self.menu.pack(side="left", fill="y", expand=False)  # No expandir en la dirección horizontal
        self.menu.pack_propagate(False)  # Para que el contenedor mantenga su tamaño

        # Crear botones en el menú
        self.btn1 = tk.Button(self.menu, text="Nuevo", command=self.nuevo_archivo, **BOTON_ESTILO)
        self.btn1.pack(pady=10)
        self.btn1.bind("<Enter>", self.on_enter)
        self.btn1.bind("<Leave>", self.on_leave)

        self.btn2 = tk.Button(self.menu, text="Abrir archivo", command=self.abrir_archivo, **BOTON_ESTILO)
        self.btn2.pack(pady=10)
        self.btn2.bind("<Enter>", self.on_enter)
        self.btn2.bind("<Leave>", self.on_leave)

        self.btn3 = tk.Button(self.menu, text="Analizar", command=self.traducir, **BOTON_ESTILO)
        self.btn3.pack(pady=10)
        self.btn3.bind("<Enter>", self.on_enter)
        self.btn3.bind("<Leave>", self.on_leave)

        self.btn4 = tk.Button(self.menu, text="Ver tokens", command=self.ver_tokens, **BOTON_ESTILO)
        self.btn4.pack(pady=10)
        self.btn4.bind("<Enter>", self.on_enter)
        self.btn4.bind("<Leave>", self.on_leave)

        self.btn5 = tk.Button(self.menu, text="Ver errores", command=self.ver_errores, **BOTON_ESTILO)
        self.btn5.pack(pady=10)
        self.btn5.bind("<Enter>", self.on_enter)
        self.btn5.bind("<Leave>", self.on_leave)

        self.btn6 = tk.Button(self.menu, text="Salir", command=self.salir, **BOTON_ESTILO)
        self.btn6.pack(pady=10)
        self.btn6.bind("<Enter>", self.on_enter)
        self.btn6.bind("<Leave>", self.on_leave)

        # Text areas para entrada y salida
        self.text1_frame = tk.Frame(master)
        self.text1_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.text1 = tk.Text(self.text1_frame, bg="white", fg="black", font=("Courier", 10), wrap="word", width=60)
        self.text1.pack(side="left", fill="both", expand=True)
        
        self.scrollbar1 = Scrollbar(self.text1_frame, orient="vertical", command=self.text1.yview)
        self.scrollbar1.pack(side="right", fill="y")
        self.text1.config(yscrollcommand=self.scrollbar1.set)
        
        self.linenumbers1 = tk.Text(self.text1_frame, width=4, bg="lightgray", fg="black", font=("Courier", 10), wrap="none")
        self.linenumbers1.pack(side="left", fill="y")
        self.linenumbers1.tag_configure("center", justify="center")
        self.linenumbers1.insert("1.0", "1\n")
        self.linenumbers1.config(state="disabled")

        self.text1.bind("<Key>", self.update_linenumbers)
        self.text1.bind("<MouseWheel>", self.scroll_linenumbers)

        self.text2_frame = tk.Frame(master)
        self.text2_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.text2 = tk.Text(self.text2_frame, bg="white", fg="black", font=("Courier", 10), wrap="word", height=10)
        self.text2.pack(side="left", fill="both", expand=True)
        
        self.scrollbar2 = Scrollbar(self.text2_frame, orient="vertical", command=self.text2.yview)
        self.scrollbar2.pack(side="right", fill="y")
        self.text2.config(yscrollcommand=self.scrollbar2.set)
        
        self.linenumbers2 = tk.Text(self.text2_frame, width=4, bg="lightgray", fg="black", font=("Courier", 10), wrap="none")
        self.linenumbers2.pack(side="left", fill="y")
        self.linenumbers2.tag_configure("center", justify="center")
        self.linenumbers2.insert("1.0", "1\n")
        self.linenumbers2.config(state="disabled")

        self.text2.bind("<Key>", self.update_linenumbers)
        self.text2.bind("<MouseWheel>", self.scroll_linenumbers)

    def on_enter(self, event):
        event.widget.config(background='#FFFFFF', foreground='black')  # Color de fondo más oscuro al pasar el cursor

    def on_leave(self, enter):
        enter.widget.config(background='#000000', foreground='white')  # Restaurar color de fondo original

    def nuevo_archivo(self):
        # Aquí puedes agregar la lógica para crear un nuevo archivo o limpiar el contenido del área de texto
        pass

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=(("Archivos LFP", "*.lfp"), ("Todos los archivos", "*.*")))
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.text1.delete("1.0", "end")
                self.text1.insert("1.0", contenido)

    def traducir(self):
        texto_nosql = self.text1.get("1.0", "end-1c")
        translator = NoSQLToMongoDBTranslator()
        comandos_mongodb, errores = translator.traducir(texto_nosql)

        self.text2.delete("1.0", tk.END)
        if comandos_mongodb:
            for comando in comandos_mongodb:
                self.text2.insert(tk.END, comando + "")
        else:
            self.text2.insert(tk.END, "Error: Error al traducir los comandos.\n")
            for error in errores:
                descripcion_error = error.get("descripcion", "Error desconocido")
                self.text2.insert(tk.END, descripcion_error + "\n")


    def ver_tokens(self):
        contenido = self.text1.get("1.0", "end-1c")
        analizador = AnalizadorLexicoSintactico()
        tokens, errores_lexicos, _ = analizador.analizar(contenido)

        if tokens:
            self.text2.delete("1.0", "end")
            table = PrettyTable(["Número", "Tipo de Token", "Token", "Línea"])
            for i, token in enumerate(tokens, start=1):
                table.add_row([i, token.tipo, token.contenido, token.linea])
            self.text2.insert("end", str(table))

    def ver_errores(self):
        contenido = self.text1.get("1.0", "end-1c")
        analizador = AnalizadorLexicoSintactico()
        tokens, errores_lexicos, errores_sintacticos = analizador.analizar(contenido)

        self.text2.delete("1.0", "end")
        table = PrettyTable(["Tipo de Error", "Línea", "Columna", "Caracter", "Token Esperado", "Descripción"])

        # Agrega los errores léxicos a la tabla
        for error in errores_lexicos:
            table.add_row([error["tipo"], error["linea"], error["columna"], error["caracter"], error.get("token_esperado", ""), error.get("descripcion", "")])

        # Agrega los errores sintácticos a la tabla
        for error in errores_sintacticos:
            table.add_row([error["tipo"], error["linea"], error["columna"], error["caracter"], error.get("token_esperado", ""), error["descripcion"]])

        self.text2.insert("end", str(table))

        # Guardar la tabla de errores en un archivo .txt
        with open("errores.txt", "w") as archivo:
            archivo.write(str(table))


    def salir(self):
        self.master.quit()

    def update_linenumbers(self, event=None):
        widget = event.widget
        lines = widget.get("1.0", "end-1c").count("\n") + 1
        widget_height = widget.winfo_height() // widget.winfo_pixels("1c")
        if lines < widget_height:
            lines = widget_height
        line_numbers = "\n".join(str(i) for i in range(1, lines + 1))
        linenumbers_widget = self.linenumbers1 if widget == self.text1 else self.linenumbers2
        linenumbers_widget.config(state="normal")
        linenumbers_widget.delete("1.0", "end")
        linenumbers_widget.insert("1.0", line_numbers)
        linenumbers_widget.config(state="disabled")

    def scroll_linenumbers(self, event=None):
        widget = event.widget
        if widget == self.text1:
            self.linenumbers1.yview_scroll(-1*(event.delta//120), "units")
        elif widget == self.text2:
            self.linenumbers2.yview_scroll(-1*(event.delta//120), "units")

root = tk.Tk()
ventana_principal = VentanaPrincipal(root)
root.mainloop()
