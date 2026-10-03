import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


class Vehiculo:
    def __init__(self, numero, imagen, x, y):
        self.numero = numero
        self.imagen = imagen
        self.x_inicial = x
        self.y = y

        self.x = x
        self.direccion = 1
        self.vueltas = 0
        self.tiempo_inicio = 0
        self.tiempo_final = 0
        self.intervalo = random.randint(20, 80)
        self.timer_id = None
        self.terminado = False
        self.elemento_canvas = None
        self.widget_imagen = None

    def reiniciar(self):
        self.x = self.x_inicial
        self.direccion = 1
        self.vueltas = 0
        self.tiempo_inicio = 0
        self.tiempo_final = 0
        self.intervalo = random.randint(20, 80)
        self.timer_id = None
        self.terminado = False


class Carrera:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Carrera de 10 personajes")
        self.ventana.geometry("1150x850")
        self.ventana.minsize(1000, 750)

        self.vehiculos = []
        self.imagenes = []
        self.en_curso = False
        self.velocidad = 1.0

        self._cargar_imagenes()
        self._crear_interfaz()
        self._crear_vehiculos()
        self._dibujar_pista()

        self.ventana.protocol(
            "WM_DELETE_WINDOW", self.cerrar
        )

    def _cargar_imagenes(self):
        for i in range(1, 11):
            imagen = None

            imagen = tk.PhotoImage(
                file=f"roxy{i}.png"
            )
           
            if imagen is not None:
                ancho = imagen.width()
                alto = imagen.height()
                factor = max(
                    1,
                    (ancho + 119) // 120,
                    (alto + 59) // 60
                )

            self.imagenes.append(imagen)

    def _crear_interfaz(self):
        ttk.Label(
            self.ventana,
            text="CARRERA DE 10 PERSONAJES",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        controles = ttk.Frame(
            self.ventana, padding=8
        )
        controles.pack(fill="x")

        ttk.Label(
            controles, text="vueltas :"
        ).grid(row=0, column=0, padx=5)

        self.rondas_var = tk.IntVar(value=3)

        self.rondas_spin = ttk.Spinbox(
            controles,
            from_=1,
            to=20,
            width=5,
            textvariable=self.rondas_var
        )
        self.rondas_spin.grid(
            row=0, column=1, padx=5
        )

        ttk.Label(
            controles, text="Tu apuesta:"
        ).grid(row=0, column=2, padx=10)

        self.apuesta_var = tk.StringVar(
            value="roxy 1"
        )

        self.apuesta_combo = ttk.Combobox(
            controles,
            textvariable=self.apuesta_var,
            values=[
                f"roxy {i}"
                for i in range(1, 11)
            ],
            state="readonly",
            width=14
        )
        self.apuesta_combo.grid(
            row=0, column=3, padx=5
        )

        ttk.Label(
            controles, text="Velocidad:"
        ).grid(row=0, column=4, padx=10)

        self.velocidad_var = tk.DoubleVar(
            value=1.0
        )

        self.slider = ttk.Scale(
            controles,
            from_=0.3,
            to=2.5,
            variable=self.velocidad_var,
            orient="horizontal",
            length=150,
            command=self._cambiar_velocidad
        )
        self.slider.grid(
            row=0, column=5, padx=5
        )

        self.velocidad_label = ttk.Label(
            controles, text="1.0x"
        )
        self.velocidad_label.grid(
            row=0, column=6, padx=5
        )

        botones = ttk.Frame(
            self.ventana, padding=8
        )
        botones.pack(fill="x")

        self.iniciar_btn = ttk.Button(
            botones,
            text="Iniciar carrera",
            command=self.iniciar
        )
        self.iniciar_btn.pack(
            side="left", padx=5
        )

        ttk.Button(
            botones,
            text="Reiniciar",
            command=self.reiniciar
        ).pack(side="left", padx=5)

        self.estado_label = ttk.Label(
            botones,
            text="Selecciona tu apuesta."
        )
        self.estado_label.pack(
            side="left", padx=10
        )
        self.canvas = tk.Canvas(
            self.ventana,
            width=1100,
            height=570,
            bg="white",
            highlightthickness=1
        )
        self.canvas.pack(
            padx=10,
            pady=5,
            fill="both",
            expand=True
        )

        tabla_frame = ttk.LabelFrame(
            self.ventana,
            text="Resultados de la carrera",
            padding=6
        )
        tabla_frame.pack(
            fill="x", padx=10, pady=10
        )

        columnas = (
            "puesto", "vehiculo",
            "tiempo", "rondas"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=5
        )

        self.tabla.heading(
            "puesto", text="Puesto"
        )
        self.tabla.heading(
            "vehiculo", text="Personaje"
        )
        self.tabla.heading(
            "tiempo", text="Tiempo (s)"
        )
        self.tabla.heading(
            "rondas", text="Idas y vueltas"
        )

        self.tabla.column(
            "puesto", width=80,
            anchor="center"
        )
        self.tabla.column(
            "vehiculo", width=220,
            anchor="center"
        )
        self.tabla.column(
            "tiempo", width=150,
            anchor="center"
        )
        self.tabla.column(
            "rondas", width=150,
            anchor="center"
        )

        self.tabla.pack(fill="x")

    def _crear_vehiculos(self):
        for i in range(10):
            y = 45 + i * 50

            vehiculo = Vehiculo(
                numero=i + 1,
                imagen=self.imagenes[i],
                x=130,
                y=y
            )

            self.vehiculos.append(vehiculo)

    def _dibujar_pista(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            550, 15,
            text="PISTA DE CARRERAS",
            font=("Arial", 12, "bold")
        )

        self.canvas.create_line(
            130, 30, 130, 530,
            fill="white", width=4
        )

        self.canvas.create_line(
            950, 30, 950, 530,
            fill="white", width=4
        )

        self.canvas.create_text(
            130, 545,
            text="SALIDA",
            anchor="s"
        )

        self.canvas.create_text(
            950, 545,
            text="META",
            anchor="s"
        )
        for v in self.vehiculos:
            self.canvas.create_line(
                70, v.y + 20,
                1010, v.y + 20,
                fill="green",
                dash=(4, 4)
            )

            self.canvas.create_text(
                35, v.y + 15,
                text=str(v.numero),
                font=("Arial", 10, "bold")
            )

            self._dibujar_personaje(v)
            
    def _dibujar_personaje(self, v):
        if v.elemento_canvas is not None:
            self.canvas.delete(
                v.elemento_canvas
            )

        if v.imagen is not None:
            if v.widget_imagen is None:
                v.widget_imagen = tk.Label(
                    self.canvas,
                    image=v.imagen,
                    bd=0,
                    bg="white"
                )

            v.elemento_canvas = (
                self.canvas.create_window(
                    v.x,
                    v.y + 15,
                    window=v.widget_imagen,
                    anchor="center"
                )
            )

        else:
            v.elemento_canvas = (
                self.canvas.create_rectangle(
                    v.x - 25,
                    v.y,
                    v.x + 25,
                    v.y + 30,
                    fill="red",
                    outline="black"
                )
            )

            self.canvas.create_text(
                v.x,
                v.y + 15,
                text=str(v.numero),
                fill="white"
            )

    def _cambiar_velocidad(self, valor):
        self.velocidad = float(valor)

        self.velocidad_label.config(
            text=f"{self.velocidad:.1f}x"
        )

    def _cancelar_timers(self):
        for v in self.vehiculos:
            if v.timer_id is not None:
                try:
                    self.ventana.after_cancel(
                        v.timer_id
                    )
                except tk.TclError:
                    pass

                v.timer_id = None

    def iniciar(self):
        if self.en_curso:
            return

        try:
            rondas = int(
                self.rondas_var.get()
            )

            if not 1 <= rondas <= 20:
                raise ValueError

        except (ValueError, tk.TclError):
            messagebox.showerror(
                "Error",
                "Introduce entre 1 y 20 rondas."
            )
            return

        self._cancelar_timers()

        for v in self.vehiculos:
            v.reiniciar()

        self._dibujar_pista()

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.rondas_objetivo = rondas
        self.en_curso = True

        self.estado_label.config(
            text="¡Carrera en curso!"
        )

        self.iniciar_btn.config(
            state="disabled"
        )
        self.rondas_spin.config(
            state="disabled"
        )
        self.apuesta_combo.config(
            state="disabled"
        )

        for v in self.vehiculos:
            v.tiempo_inicio = time.perf_counter()
            self._programar_timer(v)

    def _programar_timer(self, v):
        if self.en_curso and not v.terminado:
            demora = max(
                10,
                int(v.intervalo / self.velocidad)
            )

            v.timer_id = self.ventana.after(
                demora,
                lambda auto=v: self._mover(auto)
            )

    def _mover(self, v):
        v.timer_id = None

        if not self.en_curso or v.terminado:
            return

        v.x += 7 * v.direccion

        if v.x >= 950:
            v.x = 950
            v.direccion = -1
            v.vueltas += 1
            v.intervalo = random.randint(20, 80)

        elif v.x <= 130:
            v.x = 130
            v.direccion = 1
            v.vueltas += 1
            v.intervalo = random.randint(20, 80)

        self._dibujar_personaje(v)

        if v.vueltas >= self.rondas_objetivo * 2:
            v.terminado = True
            v.tiempo_final = (
                time.perf_counter() -
                v.tiempo_inicio
            )

            if all(
                auto.terminado
                for auto in self.vehiculos
            ):
                self._finalizar()

            return

        self._programar_timer(v)

    def _finalizar(self):
        self.en_curso = False

        self.iniciar_btn.config(state="normal")
        self.rondas_spin.config(state="normal")
        self.apuesta_combo.config(state="readonly")

        ordenados = sorted(
            self.vehiculos,
            key=lambda v: v.tiempo_final
        )

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for puesto, v in enumerate(
            ordenados, start=1
        ):
            self.tabla.insert(
                "",
                "end",
                values=(
                    puesto,
                    f"Vehículo {v.numero}",
                    f"{v.tiempo_final:.2f}",
                    self.rondas_objetivo
                )
            )

        ganador = ordenados[0]
        nombre = f"Vehículo {ganador.numero}"

        if self.apuesta_var.get() == nombre:
            mensaje = f"¡Acertaste! Ganó {nombre}."
        else:
            mensaje = (
                f"Ganó {nombre}. "
                f"Tu apuesta fue {self.apuesta_var.get()}."
            )

        self.estado_label.config(
            text=f"Ganador: {nombre}"
        )

        messagebox.showinfo(
            "Carrera finalizada",
            mensaje
        )

    def reiniciar(self):
        self.en_curso = False
        self._cancelar_timers()

        for v in self.vehiculos:
            v.reiniciar()

        self._dibujar_pista()

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.iniciar_btn.config(state="normal")
        self.rondas_spin.config(state="normal")
        self.apuesta_combo.config(state="readonly")

        self.estado_label.config(
            text="Carrera reiniciada."
        )

    def cerrar(self):
        self.en_curso = False
        self._cancelar_timers()
        self.ventana.destroy()


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = Carrera(ventana)
    ventana.mainloop()