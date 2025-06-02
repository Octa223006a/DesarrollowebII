import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class IntegracionNumericaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Integración Numérica")
        self.root.geometry("1000x700")
        
        # Variables de instancia
        self.funcion = None
        self.expr_funcion = ""
        self.a = 0.0
        self.b = 1.0
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 10), padding=5)
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        config_frame.pack(fill=tk.X, pady=5)
        
        # Función
        ttk.Label(config_frame, text="Función f(x):").grid(row=0, column=0, sticky=tk.W)
        self.func_entry = ttk.Entry(config_frame, width=40)
        self.func_entry.grid(row=0, column=1, padx=5, pady=2)
        self.func_entry.insert(0, "x**2")
        
        ttk.Button(config_frame, text="Establecer función", 
                  command=self.establecer_funcion).grid(row=0, column=2, padx=5)
        
        # Intervalo
        ttk.Label(config_frame, text="Intervalo [a, b]:").grid(row=1, column=0, sticky=tk.W)
        
        self.a_entry = ttk.Entry(config_frame, width=10)
        self.a_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.a_entry.insert(0, "0")
        
        ttk.Label(config_frame, text="a").grid(row=1, column=1, padx=(40,0))
        
        self.b_entry = ttk.Entry(config_frame, width=10)
        self.b_entry.grid(row=1, column=1, padx=(70,5), pady=2, sticky=tk.W)
        self.b_entry.insert(0, "1")
        
        ttk.Label(config_frame, text="b").grid(row=1, column=1, padx=(110,0))
        
        ttk.Button(config_frame, text="Establecer intervalo", 
                  command=self.establecer_intervalo).grid(row=1, column=2, padx=5)
        
        # Frame de métodos
        methods_frame = ttk.LabelFrame(main_frame, text="Métodos de Integración", padding=10)
        methods_frame.pack(fill=tk.X, pady=5)
        
        # Métodos simples
        ttk.Button(methods_frame, text="Trapecio Simple", 
                  command=lambda: self.calcular_metodo('trapecio')).grid(row=0, column=0, padx=5, pady=2)
        
        ttk.Button(methods_frame, text="Simpson 1/3 Simple", 
                  command=lambda: self.calcular_metodo('simpson_13')).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(methods_frame, text="Simpson 3/8 Simple", 
                  command=lambda: self.calcular_metodo('simpson_38')).grid(row=0, column=2, padx=5, pady=2)
        
        # Métodos compuestos
        ttk.Button(methods_frame, text="Trapecio Compuesto", 
                  command=lambda: self.calcular_metodo_compuesto('trapecio_compuesto')).grid(row=1, column=0, padx=5, pady=2)
        
        ttk.Button(methods_frame, text="Simpson 1/3 Compuesto", 
                  command=lambda: self.calcular_metodo_compuesto('simpson_13_compuesto')).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(methods_frame, text="Simpson 3/8 Compuesto", 
                  command=lambda: self.calcular_metodo_compuesto('simpson_38_compuesto')).grid(row=1, column=2, padx=5, pady=2)
        
        # Botón para todos los métodos
        ttk.Button(methods_frame, text="Todos los métodos", 
                  command=self.mostrar_todos_metodos).grid(row=2, column=0, columnspan=3, pady=5)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(result_frame, height=8, font=('Courier', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de gráfica
        graph_frame = ttk.LabelFrame(main_frame, text="Gráfica", padding=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configuración inicial
        self.actualizar_configuracion()
    
    def establecer_funcion(self):
        expr = self.func_entry.get()
        
        try:
            # Reemplazar ^ por ** si el usuario lo ingresa
            expr = expr.replace('^', '**')
            
            # Validar la expresión
            test_val = 1.0
            eval(expr, {'x': test_val, 'math': math, 'np': np})
            
            self.expr_funcion = expr
            self.funcion = lambda x, e=expr: eval(e, {'x': x, 'math': math, 'np': np})
            
            # Verificar en el intervalo actual
            try:
                _ = self.funcion(self.a)
                _ = self.funcion(self.b)
                _ = self.funcion((self.a + self.b)/2)
            except Exception as e:
                if not messagebox.askyesno("Advertencia", 
                                         f"La función tiene problemas en el intervalo actual: {str(e)}\n¿Desea continuar así mismo?"):
                    return
            
            self.actualizar_configuracion()
            messagebox.showinfo("Éxito", f"Función establecida: f(x) = {expr}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la expresión: {str(e)}\n\nEjemplos válidos:\n"
                                        "x**2 + 3*x - 2\n"
                                        "math.sin(x) + 0.5\n"
                                        "math.exp(-x**2)\n"
                                        "(x^2)/6")
    
    def establecer_intervalo(self):
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            
            if a >= b:
                messagebox.showerror("Error", "El límite inferior 'a' debe ser menor que el límite superior 'b'")
                return
            
            # Verificar que la función sea válida en el nuevo intervalo
            if self.funcion is not None:
                try:
                    _ = self.funcion(a)
                    _ = self.funcion(b)
                    _ = self.funcion((a + b)/2)
                except Exception as e:
                    messagebox.showerror("Error", f"La función no es válida en todo el intervalo: {str(e)}")
                    return
            
            self.a = a
            self.b = b
            self.actualizar_configuracion()
            messagebox.showinfo("Éxito", f"Intervalo establecido: [{self.a}, {self.b}]")
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para a y b")
        except AttributeError:
            messagebox.showerror("Error", "Primero debe definir una función")
    
    def actualizar_configuracion(self):
        """Actualiza la visualización de la configuración actual"""
        config_text = f"Configuración actual:\n"
        config_text += f"Función: f(x) = {self.expr_funcion if self.expr_funcion else 'No definida'}\n"
        config_text += f"Intervalo: [{self.a}, {self.b}]" if self.funcion else "Intervalo: No definido"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, config_text)
    
    def validar_configuracion(self):
        """Verifica que la función y el intervalo estén configurados"""
        if self.funcion is None:
            messagebox.showerror("Error", "Primero debe ingresar una función")
            return False
        return True
    
    def calcular_metodo(self, metodo):
        if not self.validar_configuracion():
            return
            
        try:
            if metodo == 'trapecio':
                resultado = self.trapecio()
                nombre = "Trapecio Simple"
            elif metodo == 'simpson_13':
                resultado = self.simpson_13()
                nombre = "Simpson 1/3 Simple"
            elif metodo == 'simpson_38':
                resultado = self.simpson_38()
                nombre = "Simpson 3/8 Simple"
            
            self.mostrar_resultado(nombre, resultado)
            self.graficar_metodo(metodo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def calcular_metodo_compuesto(self, metodo):
        if not self.validar_configuracion():
            return
            
        try:
            if metodo == 'trapecio_compuesto':
                n = simpledialog.askinteger("Trapecio Compuesto", 
                                           "Ingrese el número de divisiones (n):",
                                           minvalue=1, initialvalue=4)
                if n is None: return
                resultado = self.trapecio_compuesto(n)
                nombre = f"Trapecio Compuesto (n={n})"
                
            elif metodo == 'simpson_13_compuesto':
                n = simpledialog.askinteger("Simpson 1/3 Compuesto", 
                                           "Ingrese el número de divisiones (n, debe ser par):",
                                           minvalue=2, initialvalue=4)
                if n is None: return
                if n % 2 != 0:
                    messagebox.showerror("Error", "n debe ser un número par para Simpson 1/3 compuesto")
                    return
                resultado = self.simpson_13_compuesto(n)
                nombre = f"Simpson 1/3 Compuesto (n={n})"
                
            elif metodo == 'simpson_38_compuesto':
                n = simpledialog.askinteger("Simpson 3/8 Compuesto", 
                                           "Ingrese el número de divisiones (n, debe ser múltiplo de 3):",
                                           minvalue=3, initialvalue=6)
                if n is None: return
                if n % 3 != 0:
                    messagebox.showerror("Error", "n debe ser múltiplo de 3 para Simpson 3/8 compuesto")
                    return
                resultado = self.simpson_38_compuesto(n)
                nombre = f"Simpson 3/8 Compuesto (n={n})"
            
            self.mostrar_resultado(nombre, resultado)
            self.graficar_metodo(metodo, n)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def mostrar_resultado(self, nombre, resultado):
        if resultado is None:
            return
            
        self.result_text.delete(1.0, tk.END)
        text = f"Configuración actual:\n"
        text += f"Función: f(x) = {self.expr_funcion}\n"
        text += f"Intervalo: [{self.a}, {self.b}]\n\n"
        text += f"Resultado {nombre}:\n"
        text += f"Integral ≈ {resultado:.8f}"
        
        self.result_text.insert(tk.END, text)
    
    def mostrar_todos_metodos(self):
        if not self.validar_configuracion():
            return
            
        try:
            resultados = []
            
            # Métodos simples
            resultados.append(("Trapecio simple", self.trapecio()))
            resultados.append(("Simpson 1/3 simple", self.simpson_13()))
            resultados.append(("Simpson 3/8 simple", self.simpson_38()))
            
            # Métodos compuestos con valores por defecto
            resultados.append(("Trapecio compuesto (n=4)", self.trapecio_compuesto(4)))
            resultados.append(("Simpson 1/3 compuesto (n=4)", self.simpson_13_compuesto(4)))
            resultados.append(("Simpson 3/8 compuesto (n=6)", self.simpson_38_compuesto(6)))
            
            # Mostrar resultados
            self.result_text.delete(1.0, tk.END)
            text = f"Configuración actual:\n"
            text += f"Función: f(x) = {self.expr_funcion}\n"
            text += f"Intervalo: [{self.a}, {self.b}]\n\n"
            text += "RESULTADOS DE TODOS LOS MÉTODOS:\n"
            text += "-"*50 + "\n"
            
            for nombre, res in resultados:
                text += f"{nombre:<30} {res:.8f}\n"
            
            self.result_text.insert(tk.END, text)
            
            # Mostrar gráficas
            self.graficar_metodo('trapecio')
            self.graficar_metodo('trapecio_compuesto', 4)
            self.graficar_metodo('simpson_13')
            self.graficar_metodo('simpson_13_compuesto', 4)
            self.graficar_metodo('simpson_38')
            self.graficar_metodo('simpson_38_compuesto', 6)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    # Métodos de integración numérica (igual que en la versión anterior)
    def trapecio(self):
        h = self.b - self.a
        integral = (self.funcion(self.a) + self.funcion(self.b)) * h / 2
        return integral
    
    def trapecio_compuesto(self, n):
        h = (self.b - self.a) / n
        integral = self.funcion(self.a)
        
        for i in range(1, n):
            integral += 2 * self.funcion(self.a + i * h)
        
        integral += self.funcion(self.b)
        return integral * h / 2
    
    def simpson_13(self):
        h = (self.b - self.a) / 2
        integral = (self.funcion(self.a) + 4 * self.funcion((self.a + self.b)/2) + self.funcion(self.b)) * h / 3
        return integral
    
    def simpson_13_compuesto(self, n):
        h = (self.b - self.a) / n
        integral = self.funcion(self.a)
        
        for i in range(1, n):
            x = self.a + i * h
            integral += 4 * self.funcion(x) if i % 2 else 2 * self.funcion(x)
        
        integral += self.funcion(self.b)
        return integral * h / 3
    
    def simpson_38(self):
        h = (self.b - self.a) / 3
        x0, x1, x2, x3 = self.a, self.a + h, self.a + 2*h, self.b
        integral = (self.funcion(x0) + 3*self.funcion(x1) + 3*self.funcion(x2) + self.funcion(x3)) * 3*h / 8
        return integral
    
    def simpson_38_compuesto(self, n):
        h = (self.b - self.a) / n
        integral = self.funcion(self.a)
        
        for i in range(1, n):
            x = self.a + i * h
            integral += 3 * self.funcion(x) if i % 3 else 2 * self.funcion(x)
        
        integral += self.funcion(self.b)
        return integral * 3 * h / 8
    
    def graficar_metodo(self, metodo, n=None):
        """Grafica la función y la aproximación numérica con mejoras visuales"""
        self.ax.clear()
        
        # Función real
        x_real = np.linspace(self.a, self.b, 1000)
        y_real = [self.funcion(x) for x in x_real]
        self.ax.plot(x_real, y_real, 'b-', linewidth=2, label=f'f(x) = {self.expr_funcion}')
        
        # Configurar según el método
        if metodo == 'trapecio':
            integral = self.trapecio()
            x_approx = [self.a, self.b]
            titulo = f"Método del Trapecio Simple\nIntegral ≈ {integral:.6f}"
        elif metodo == 'trapecio_compuesto':
            integral = self.trapecio_compuesto(n)
            x_approx = np.linspace(self.a, self.b, n+1)
            titulo = f"Método del Trapecio Compuesto (n={n})\nIntegral ≈ {integral:.6f}"
        elif metodo == 'simpson_13':
            integral = self.simpson_13()
            x_approx = [self.a, (self.a+self.b)/2, self.b]
            titulo = f"Método de Simpson 1/3 Simple\nIntegral ≈ {integral:.6f}"
        elif metodo == 'simpson_13_compuesto':
            integral = self.simpson_13_compuesto(n)
            x_approx = np.linspace(self.a, self.b, n+1)
            titulo = f"Método de Simpson 1/3 Compuesto (n={n})\nIntegral ≈ {integral:.6f}"
        elif metodo == 'simpson_38':
            integral = self.simpson_38()
            h = (self.b - self.a)/3
            x_approx = [self.a, self.a+h, self.a+2*h, self.b]
            titulo = f"Método de Simpson 3/8 Simple\nIntegral ≈ {integral:.6f}"
        elif metodo == 'simpson_38_compuesto':
            integral = self.simpson_38_compuesto(n)
            x_approx = np.linspace(self.a, self.b, n+1)
            titulo = f"Método de Simpson 3/8 Compuesto (n={n})\nIntegral ≈ {integral:.6f}"
        
        y_approx = [self.funcion(x) for x in x_approx]
        
        # Graficar aproximación
        if metodo in ['trapecio', 'trapecio_compuesto']:
            for i in range(len(x_approx)-1):
                self.ax.plot([x_approx[i], x_approx[i+1]], [y_approx[i], y_approx[i+1]], 'r-')
                self.ax.fill_between([x_approx[i], x_approx[i+1]], [y_approx[i], y_approx[i+1]], alpha=0.2, color='red')
        elif metodo in ['simpson_13', 'simpson_13_compuesto']:
            for i in range(0, len(x_approx)-1, 2):
                x_seg = np.linspace(x_approx[i], x_approx[i+2], 20)
                coef = np.polyfit([x_approx[i], x_approx[i+1], x_approx[i+2]], 
                                 [y_approx[i], y_approx[i+1], y_approx[i+2]], 2)
                y_seg = np.polyval(coef, x_seg)
                self.ax.plot(x_seg, y_seg, 'r-')
                self.ax.fill_between(x_seg, y_seg, alpha=0.2, color='red')
        elif metodo in ['simpson_38', 'simpson_38_compuesto']:
            for i in range(0, len(x_approx)-1, 3):
                x_seg = np.linspace(x_approx[i], x_approx[i+3], 20)
                coef = np.polyfit([x_approx[i], x_approx[i+1], x_approx[i+2], x_approx[i+3]], 
                                 [y_approx[i], y_approx[i+1], y_approx[i+2], y_approx[i+3]], 3)
                y_seg = np.polyval(coef, x_seg)
                self.ax.plot(x_seg, y_seg, 'r-')
                self.ax.fill_between(x_seg, y_seg, alpha=0.2, color='red')
        
        # Graficar puntos de aproximación y líneas desde los ejes
        self.ax.plot(x_approx, y_approx, 'ro', label='Puntos de aproximación')
        for x, y in zip(x_approx, y_approx):
            self.ax.plot([x, x], [0, y], 'k--', linewidth=0.8)  # Línea vertical
            self.ax.plot([0, x], [y, y], 'k--', linewidth=0.8)  # Línea horizontal
            self.ax.text(x, y, f'({x:.2f}, {y:.2f})', fontsize=8, ha='right', va='bottom', color='purple')
        
        # Configuración de la gráfica
        self.ax.set_title(titulo, fontsize=12, fontweight='bold')
        self.ax.set_xlabel('x', fontsize=10)
        self.ax.set_ylabel('f(x)', fontsize=10)
        self.ax.legend()
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.axhline(0, color='black', linewidth=0.8, alpha=0.8)  # Eje x
        self.ax.axvline(0, color='black', linewidth=0.8, alpha=0.8)  # Eje y
        
        # Mostrar números en los ejes
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegracionNumericaGUI(root)
    root.mainloop()
