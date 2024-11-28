import streamlit as st
import json
from pathlib import Path
import bcrypt
from acciones2 import ejecutar_acciones  # Función para analizar acciones
from alianz2 import ejecutar_etfs  # Función para analizar ETFs

# Archivo JSON para guardar usuarios
USERS_FILE = Path("users.json")

# Función para cargar usuarios
def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as file:
            try:
                data = json.load(file)
                if "users" in data and isinstance(data["users"], dict):
                    return data
                else:
                    return {"users": {}}
            except json.JSONDecodeError:
                st.error("El archivo users.json está corrupto. Se reiniciará.")
                return {"users": {}}
    return {"users": {}}

# Función para guardar usuarios
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Función para registrar usuarios
def register_user(name, username, password):
    users = load_users()
    if username in users["users"]:
        return False, "El nombre de usuario ya existe."
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users["users"][username] = {"name": name, "password": hashed_password}
    save_users(users)
    return True, "Usuario registrado exitosamente."

# Función para autenticar usuarios
def authenticate_user(username, password):
    users = load_users()
    user = users["users"].get(username)
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return False, None
    return True, user["name"]

# Configuración inicial
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Interfaz principal
if st.session_state["logged_in"]:
    st.sidebar.write(f"Bienvenido, {st.session_state['name']} 👋")
    st.title("Simulador de Inversión")

    # Selección entre acciones y ETFs
    opcion = st.sidebar.radio("¿Qué deseas analizar?", ["Acciones", "ETFs"], horizontal=True)

    if opcion == "Acciones":
        ejecutar_acciones()  # Ejecutar análisis de acciones
    elif opcion == "ETFs":
        ejecutar_etfs()  # Ejecutar análisis de ETFs

    if st.button("Cerrar Sesión"):
        st.session_state["logged_in"] = False
        st.session_state["name"] = ""
        st.experimental_set_query_params()  # Reinicia la página
else:
    # Elementos comunes en la página de registro e inicio de sesión
    st.image(
        "https://lh3.googleusercontent.com/a/ACg8ocJRBWqWITdSZLCQpa9b-htwGwyA_KwQ_PQbAWgXP-b7x8mv7ug0INBi1YEZbuse4oKDTiYlptGQ_uX275FjzP5Yl2YRDiDp=s411-c-no",
        width=300,
    )
    st.title("Bienvenido a DiviGrowth")
    st.write("""
        **DiviGrowth** es una empresa que se dedica a ayudarte a hacer crecer tu capital. 
        Nuestro objetivo es ofrecerte herramientas de fácil acceso para que puedas evaluar las mejores opciones de inversión disponibles. 
        Ya sea que busques diversificar tu portafolio o encontrar la opción más rentable para ti, 
        en DiviGrowth encontrarás las herramientas necesarias para tomar decisiones informadas y rentables.
    """)

    # Selección entre Registro e Inicio de Sesión
    opcion = st.radio("¿Qué deseas hacer?", ["Iniciar Sesión", "Registrar"], horizontal=True)

    if opcion == "Registrar":
        st.title("Registro de Usuario")
        name = st.text_input("Nombre")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input("Confirmar Contraseña", type="password")

        if st.button("Registrar"):
            if password != confirm_password:
                st.error("Las contraseñas no coinciden.")
            elif len(password) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                success, message = register_user(name, username, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

    elif opcion == "Iniciar Sesión":
        st.title("Inicio de Sesión")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar Sesión"):
            success, name = authenticate_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["name"] = name
                st.success(f"Bienvenido, {name} 👋")
                st.experimental_set_query_params()
            else:
                st.error("Usuario o contraseña incorrectos.")
