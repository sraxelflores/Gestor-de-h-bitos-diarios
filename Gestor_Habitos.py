# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 20:01:00 2025
Description: "Gestor de habitos díarios."
Version: Primera version del Gestor de habitos diarios.
@author: axelr
"""
import json
from tkinter import Tk, Label, Button, Entry, Listbox, Scrollbar, END, messagebox
from datetime import datetime

# Archivo donde se guardaran los datos
DATA_FILE = "habits.json"

# Cargar datos de hábitos
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Guardar datos de hábitos
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Funciones para la interfaz gráfica
def refresh_habits_list():
    habit_listbox.delete(0, END)
    for habit in habits.keys():
        habit_listbox.insert(END, habit)

def add_habit():
    habit_name = habit_name_entry.get().strip()
    description = description_entry.get().strip()
    if habit_name and description:
        if habit_name in habits:
            messagebox.showerror("Error", "El hábito ya existe.")
        else:
            habits[habit_name] = {"description": description, "progress": []}
            save_data(habits)
            refresh_habits_list()
            habit_name_entry.delete(0, END)
            description_entry.delete(0, END)
            messagebox.showinfo("Éxito", f"Hábito '{habit_name}' agregado.")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

def delete_habit():
    try:
        selected_habit = habit_listbox.get(habit_listbox.curselection())
        if selected_habit:
            del habits[selected_habit]
            save_data(habits)
            refresh_habits_list()
            messagebox.showinfo("Éxito", f"Hábito '{selected_habit}' eliminado.")
    except IndexError:
        messagebox.showerror("Error", "Por favor, selecciona un hábito para eliminar.")

def mark_habit_completed():
    try:
        selected_habit = habit_listbox.get(habit_listbox.curselection())
        if selected_habit:
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in habits[selected_habit]["progress"]:
                habits[selected_habit]["progress"].append(today)
                save_data(habits)
                messagebox.showinfo("Éxito", f"Hábito '{selected_habit}' completado para hoy.")
            else:
                messagebox.showinfo("Aviso", "Ya marcaste este hábito como completado hoy.")
    except IndexError:
        messagebox.showerror("Error", "Por favor, selecciona un hábito.")

def show_progress():
    progress_window = Tk()
    progress_window.title("Progreso de Hábitos")
    Label(progress_window, text="Progreso de Hábitos", font=("Arial", 14)).pack(pady=10)
    for habit, info in habits.items():
        Label(progress_window, text=f"Hábito: {habit}", font=("Arial", 12)).pack(anchor="w", padx=10)
        Label(progress_window, text=f"Descripción: {info['description']}", font=("Arial", 10)).pack(anchor="w", padx=20)
        Label(progress_window, text=f"Días completados: {len(info['progress'])}", font=("Arial", 10)).pack(anchor="w", padx=20)
        Label(progress_window, text=f"Fechas: {', '.join(info['progress'])}", font=("Arial", 10)).pack(anchor="w", padx=20)
        Label(progress_window, text="-"*40).pack()
    Button(progress_window, text="Cerrar", command=progress_window.destroy).pack(pady=10)
    progress_window.mainloop()

# Interfaz principal
habits = load_data()
root = Tk()
root.title("Gestor de Hábitos")

# Etiquetas y campos de entrada
Label(root, text="Nombre del Hábito").grid(row=0, column=0, padx=10, pady=5)
habit_name_entry = Entry(root)
habit_name_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Descripción").grid(row=1, column=0, padx=10, pady=5)
description_entry = Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=5)

Button(root, text="Agregar Hábito", command=add_habit).grid(row=2, column=0, columnspan=2, pady=10)

# Lista de hábitos
Label(root, text="Hábitos").grid(row=3, column=0, columnspan=2, pady=5)
habit_listbox = Listbox(root, selectmode="single", width=40, height=10)
habit_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

scrollbar = Scrollbar(root)
scrollbar.grid(row=4, column=2, sticky="ns")
habit_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=habit_listbox.yview)

# Botones de acción
Button(root, text="Marcar Completado", command=mark_habit_completed).grid(row=5, column=0, pady=10)
Button(root, text="Ver Progreso", command=show_progress).grid(row=5, column=1, pady=10)
Button(root, text="Eliminar Hábito", command=delete_habit).grid(row=6, column=0, columnspan=2, pady=10)
Button(root, text="Cerrar Gestor", command=root.destroy).grid(row=7, column=0, columnspan=2, pady=10)

refresh_habits_list()
root.mainloop()
