import os
import shutil
import json
import threading
import platform
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# ==========================================
# CONFIGURACIÓN INICIAL DE CUSTOMTKINTER
# ==========================================
ctk.set_appearance_mode("Dark")       # Modo oscuro por defecto para un look premium
ctk.set_default_color_theme("blue")    # Tema azul para los botones y elementos interactivos

# Nombre del archivo de historial oculto
HISTORIAL_FILE_NAME = ".historial_movimientos.json"

# Atributo de sistema para ocultar archivos en Windows (FILE_ATTRIBUTE_HIDDEN = 2)
FILE_ATTRIBUTE_HIDDEN = 0x02

# Mapeo de categorías y sus extensiones
MAPEO_CATEGORIAS = {
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Instaladores": [".exe", ".msi", ".dmg"],
    "Comprimidos": [".zip", ".rar", ".7z"],
    "Multimedia": [".mp4", ".mp3", ".mkv", ".wav"],
}

def ocultar_archivo(ruta_archivo: Path):
    """
    Establece de manera nativa el atributo de archivo 'Oculto' si la aplicación
    se ejecuta en Windows. En Unix (macOS/Linux) ya se oculta por iniciar con punto.
    """
    if os.name == 'nt':
        try:
            # ctypes se comunica directamente con la API de Windows Kernel32
            # para aplicar el atributo FILE_ATTRIBUTE_HIDDEN (valor 2).
            ctypes.windll.kernel32.SetFileAttributesW(str(ruta_archivo), FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            print(f"Error al establecer atributo oculto en Windows: {e}")

class OrganizadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Organizador Mágico Premium")
        self.geometry("500x600")
        self.resizable(False, False)

        # Variables de estado
        self.ruta_seleccionada = None
        self.operacion_en_progreso = False

        # Inicialización de la interfaz
        self.crear_diseno_ui()
        self.enlazar_atajos_teclado()

        # Log inicial de bienvenida
        self.agregar_a_log("✨ Bienvenido al Organizador Mágico Premium ✨")
        self.agregar_a_log("Selecciona una carpeta para comenzar a ordenar tus archivos.")

    def crear_diseno_ui(self):
        """
        Crea todos los componentes de la interfaz usando customtkinter
        siguiendo un patrón de diseño moderno, limpio y de alto contraste.
        """
        # --- Cabecera con Título ---
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Organizador Mágico Premium",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#1F6AA5"
        )
        self.lbl_titulo.pack(pady=(20, 5))

        self.lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Ordena y restaura tus carpetas con un solo clic",
            font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"),
            text_color="gray"
        )
        self.lbl_subtitulo.pack(pady=(0, 20))

        # --- Panel de Selección de Carpeta ---
        self.frame_carpeta = ctk.CTkFrame(self)
        self.frame_carpeta.pack(fill="x", padx=25, pady=10)

        self.entry_ruta = ctk.CTkEntry(
            self.frame_carpeta,
            placeholder_text="Ninguna carpeta seleccionada...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            width=300
        )
        self.entry_ruta.pack(side="left", padx=(10, 5), pady=10, fill="x", expand=True)
        # Hacemos que sea de solo lectura para evitar rutas manuales corruptas
        self.entry_ruta.configure(state="disabled")

        self.btn_seleccionar = ctk.CTkButton(
            self.frame_carpeta,
            text="Seleccionar",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            width=100,
            command=self.abrir_dialogo_carpeta
        )
        self.btn_seleccionar.pack(side="right", padx=(5, 10), pady=10)

        # --- Panel de Acciones (Botones Principales) ---
        self.frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_acciones.pack(fill="x", padx=25, pady=15)

        # Botón gigante destacado para limpiar y organizar
        self.btn_organizar = ctk.CTkButton(
            self.frame_acciones,
            text="🧹 Limpiar y Organizar",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            height=50,
            command=self.iniciar_organizacion_hilo
        )
        self.btn_organizar.pack(fill="x", pady=(0, 10))

        # Botón secundario para deshacer cambios (diseño estilo peligro/atención en rojizo/gris)
        self.btn_deshacer = ctk.CTkButton(
            self.frame_acciones,
            text="↩ Deshacer (Ctrl+Z)",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            height=40,
            fg_color="#D35400",       # Color naranja/rojizo premium
            hover_color="#A04000",
            command=self.iniciar_deshacer_hilo
        )
        self.btn_deshacer.pack(fill="x")

        # --- Log de Actividad ---
        self.lbl_log = ctk.CTkLabel(
            self,
            text="Registro de Actividad",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        self.lbl_log.pack(anchor="w", padx=25, pady=(15, 2))

        self.textbox_log = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=11),
            state="disabled",
            wrap="word",
            fg_color="#1E1E1E",
            text_color="#00FF66" # Estilo consola hacker verde neón premium
        )
        self.textbox_log.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    def enlazar_atajos_teclado(self):
        """
        Vincula los atajos de teclado del sistema a las funciones de control de la app.
        """
        # Event bindings para Ctrl+Z en minúscula y mayúscula para evitar fallas
        self.bind("<Control-z>", lambda e: self.iniciar_deshacer_hilo())
        self.bind("<Control-Z>", lambda e: self.iniciar_deshacer_hilo())

    def abrir_dialogo_carpeta(self):
        """
        Abre el explorador de archivos nativo del sistema para seleccionar el directorio de trabajo.
        """
        directorio = filedialog.askdirectory(title="Selecciona la carpeta a organizar")
        if directorio:
            self.ruta_seleccionada = Path(directorio)
            self.entry_ruta.configure(state="normal")
            self.entry_ruta.delete(0, "end")
            self.entry_ruta.insert(0, str(self.ruta_seleccionada))
            self.entry_ruta.configure(state="disabled")
            self.agregar_a_log(f"📁 Carpeta seleccionada: {self.ruta_seleccionada}")

    def agregar_a_log(self, mensaje: str):
        """
        Inserta de manera segura un mensaje al final de la consola de registro
        garantizando compatibilidad multihilo mediante after().
        """
        def escribir():
            self.textbox_log.configure(state="normal")
            self.textbox_log.insert("end", f"{mensaje}\n")
            self.textbox_log.see("end") # Auto-scroll al final del texto
            self.textbox_log.configure(state="disabled")
        
        # Ejecuta la modificación de la UI en el hilo principal de Tkinter
        self.after(0, escribir)

    def cambiar_estado_controles(self, activo: bool):
        """
        Habilita o deshabilita los botones de la interfaz gráfica para evitar
        operaciones concurrentes peligrosas mientras se procesan archivos.
        """
        estado = "normal" if activo else "disabled"
        self.btn_seleccionar.configure(state=estado)
        self.btn_organizar.configure(state=estado)
        self.btn_deshacer.configure(state=estado)

    # ==========================================
    # LÓGICA DE ORGANIZACIÓN (MULTIHILO)
    # ==========================================
    def iniciar_organizacion_hilo(self):
        """
        Dispara el proceso de organización en un hilo separado de ejecución
        para no bloquear la interfaz de usuario (GUI).
        """
        if not self.ruta_seleccionada:
            self.agregar_a_log("⚠️ Error: Por favor, selecciona una carpeta primero.")
            return

        if self.operacion_en_progreso:
            return

        self.operacion_en_progreso = True
        self.cambiar_estado_controles(False)
        self.agregar_a_log("\n🧹 Iniciando limpieza y ordenamiento...")
        
        # Creación del hilo de fondo para procesar la lógica de archivos
        hilo = threading.Thread(target=self.ejecutar_organizacion, daemon=True)
        hilo.start()

    def ejecutar_organizacion(self):
        try:
            ruta = self.ruta_seleccionada
            # 1. Escanear archivos sueltos en el directorio raíz
            # Ignoramos subcarpetas usando is_file()
            archivos = [f for f in ruta.iterdir() if f.is_file() and f.name != HISTORIAL_FILE_NAME]

            if not archivos:
                self.agregar_a_log("ℹ️ No hay archivos sueltos para organizar en esta carpeta.")
                self.operacion_en_progreso = False
                self.cambiar_estado_controles(True)
                return

            historial_movimientos = {}
            total_organizados = 0

            # 2. Iteración y clasificación de archivos
            for archivo in archivos:
                ext = archivo.suffix.lower()
                categoria = "Otros" # Categoría por defecto para archivos huérfanos

                # Buscar a qué categoría pertenece el archivo según su extensión
                for cat, extensiones in MAPEO_CATEGORIAS.items():
                    if ext in extensiones:
                        categoria = cat
                        break

                # Crear la carpeta de destino si no existe
                carpeta_destino = ruta / categoria
                try:
                    carpeta_destino.mkdir(exist_ok=True)
                except Exception as err:
                    self.agregar_a_log(f"⚠️ No se pudo crear la subcarpeta /{categoria}: {err}")
                    continue

                # Definir la ruta final del archivo
                ruta_final = carpeta_destino / archivo.name

                # Manejar colisión de nombres (si ya existe un archivo con el mismo nombre)
                if ruta_final.exists():
                    base = archivo.stem
                    extension = archivo.suffix
                    contador = 1
                    while (carpeta_destino / f"{base}_{contador}{extension}").exists():
                        contador += 1
                    ruta_final = carpeta_destino / f"{base}_{contador}{extension}"

                # Intentar mover el archivo a su nueva ubicación
                try:
                    shutil.move(str(archivo), str(ruta_final))
                    # Registrar en el historial usando rutas absolutas
                    historial_movimientos[str(ruta_final)] = str(archivo)
                    self.agregar_a_log(f"[✓] Movido: {archivo.name} -> /{categoria}")
                    total_organizados += 1
                except Exception as err:
                    self.agregar_a_log(f"❌ Error al mover {archivo.name}: {err} (¿Está abierto o en uso?)")

            # 3. Guardar el archivo de historial en formato JSON
            if historial_movimientos:
                ruta_historial = ruta / HISTORIAL_FILE_NAME
                try:
                    with open(ruta_historial, "w", encoding="utf-8") as f:
                        json.dump(historial_movimientos, f, indent=4, ensure_ascii=False)
                    
                    # Llamada a ocultación nativa del archivo en Windows
                    ocultar_archivo(ruta_historial)
                except Exception as err:
                    self.agregar_a_log(f"⚠️ No se pudo guardar el archivo de historial: {err}")

            self.agregar_a_log(f"\n🎉 ¡Listo! Se organizaron {total_organizados} archivos exitosamente.")
            
        except Exception as e:
            self.agregar_a_log(f"❌ Error general en la organización: {e}")
        finally:
            self.operacion_en_progreso = False
            self.cambiar_estado_controles(True)

    # ==========================================
    # LÓGICA DE DESHACER (MULTIHILO)
    # ==========================================
    def iniciar_deshacer_hilo(self):
        """
        Dispara el proceso de deshacer en un hilo separado de ejecución
        para no bloquear la interfaz gráfica.
        """
        if not self.ruta_seleccionada:
            self.agregar_a_log("⚠️ Error: Por favor, selecciona una carpeta primero.")
            return

        if self.operacion_en_progreso:
            return

        self.operacion_en_progreso = True
        self.cambiar_estado_controles(False)
        self.agregar_a_log("\n↩ Iniciando restauración de archivos (Deshacer)...")

        hilo = threading.Thread(target=self.ejecutar_deshacer, daemon=True)
        hilo.start()

    def ejecutar_deshacer(self):
        try:
            ruta = self.ruta_seleccionada
            ruta_historial = ruta / HISTORIAL_FILE_NAME

            # 1. Validar que exista un archivo de historial
            if not ruta_historial.exists():
                self.agregar_a_log("ℹ️ No se encontró ningún historial para deshacer en esta carpeta.")
                self.operacion_en_progreso = False
                self.cambiar_estado_controles(True)
                return

            # 2. Leer el historial guardado
            try:
                with open(ruta_historial, "r", encoding="utf-8") as f:
                    historial = json.load(f)
            except Exception as err:
                self.agregar_a_log(f"❌ Error al leer el historial: {err}")
                self.operacion_en_progreso = False
                self.cambiar_estado_controles(True)
                return

            total_restaurados = 0
            # Guardamos un set con las carpetas contenedoras para limpiarlas después si quedan vacías
            directorios_a_revisar = set()

            # 3. Procesar de forma inversa: nueva_ruta -> ruta_original
            for ruta_nueva_str, ruta_original_str in historial.items():
                ruta_nueva = Path(ruta_nueva_str)
                ruta_original = Path(ruta_original_str)

                if ruta_nueva.exists():
                    try:
                        # Asegurar que la ruta padre original exista (en caso de que haya sido borrada)
                        ruta_original.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Mover el archivo a su posición original
                        shutil.move(str(ruta_nueva), str(ruta_original))
                        self.agregar_a_log(f"[↺] Restaurado: {ruta_original.name} -> raíz")
                        
                        directorios_a_revisar.add(ruta_nueva.parent)
                        total_restaurados += 1
                    except Exception as err:
                        self.agregar_a_log(f"❌ Error al restaurar {ruta_nueva.name}: {err}")
                else:
                    self.agregar_a_log(f"⚠️ No se encontró: {ruta_nueva.name} (puede haber sido movido o eliminado)")

            # 4. Eliminar subcarpetas creadas si quedaron vacías
            for carpeta in directorios_a_revisar:
                if carpeta.exists() and carpeta.is_dir():
                    # any(carpeta.iterdir()) retorna False si la carpeta no contiene ningún elemento
                    if not any(carpeta.iterdir()):
                        try:
                            carpeta.rmdir()
                            self.agregar_a_log(f"[🧹] Carpeta vacía eliminada: /{carpeta.name}")
                        except Exception as err:
                            self.agregar_a_log(f"⚠️ No se pudo eliminar la carpeta vacía {carpeta.name}: {err}")

            # 5. Eliminar el archivo de historial de movimientos
            try:
                ruta_historial.unlink()
            except Exception as err:
                self.agregar_a_log(f"⚠️ No se pudo eliminar el archivo de historial: {err}")

            self.agregar_a_log(f"\n🎉 ¡Restauración completa! Se devolvieron {total_restaurados} archivos a su ubicación original.")

        except Exception as e:
            self.agregar_a_log(f"❌ Error general en la restauración: {e}")
        finally:
            self.operacion_en_progreso = False
            self.cambiar_estado_controles(True)

# ==========================================
# INICIO DE LA APLICACIÓN
# ==========================================
if __name__ == "__main__":
    app = OrganizadorApp()
    app.mainloop()
