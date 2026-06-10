# ✨ Organizador Mágico Premium 🧹

¡El software de escritorio definitivo para mantener tus directorios ordenados y limpios de forma automática, segura y con un solo clic!

Desarrollado en **Python 3** y potenciado con **CustomTkinter** para ofrecer una interfaz gráfica de usuario (GUI) moderna, fluida y con un aspecto oscuro premium por defecto.

---

## 🚀 Características Clave

* **📁 Selector Dinámico de Directorio**: Olvídate de las rutas quemadas (*hardcoded*). Elige cualquier carpeta de tu ordenador (Descargas, Escritorio o cualquier otra) a través de un explorador de archivos nativo.
* **⚡ Lógica de Organización Asíncrona (Multihilo)**: La aplicación ejecuta el procesamiento de archivos en un hilo independiente (`threading`), lo que evita que la interfaz gráfica se congele o se muestre como "No responde".
* **⏳ La Máquina del Tiempo (Deshacer / Ctrl+Z)**: ¿Te equivocaste al ordenar o quieres volver atrás? Presiona el botón de **Deshacer** o pulsa el atajo de teclado universal `Ctrl + Z` para restaurar todos los archivos a sus ubicaciones originales al instante.
* **🛡️ Limpieza Automática de Carpetas**: Al deshacer los cambios, la aplicación detecta y elimina automáticamente las carpetas de clasificación que hayan quedado vacías para no dejar basura.
* **🥷 Historial Inteligente y Oculto**: Registra los movimientos en un archivo `.historial_movimientos.json` dentro del mismo directorio.
  * **En Windows**: Se oculta a nivel de sistema operativo utilizando las APIs nativas de Windows a través de la librería `ctypes`.
  * **En macOS/Linux**: Se oculta automáticamente usando la convención del punto inicial.
* **❌ Tolerancia a Fallos**: Si un archivo está abierto, bloqueado o en uso por otro programa, el script no se detendrá ni fallará; simplemente registrará el aviso en el log y continuará ordenando los demás archivos.
* **🖥️ Consola de Actividad en Tiempo Real**: Un Log estilo hacker neón que te muestra exactamente qué archivo se está moviendo y hacia dónde.

---

## 📂 Clasificación de Archivos (Estructura Estricta)

Los archivos sueltos del directorio raíz seleccionado se clasificarán de forma inteligente en las siguientes subcarpetas basándose en su extensión:

| Subcarpeta de Destino | Extensiones Agrupadas |
| :--- | :--- |
| **📄 Documentos** | `.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.pptx` |
| **📷 Imágenes** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg` |
| **⚙️ Instaladores** | `.exe`, `.msi`, `.dmg` |
| **📦 Comprimidos** | `.zip`, `.rar`, `.7z` |
| **🎵 Multimedia** | `.mp4`, `.mp3`, `.mkv`, `.wav` |
| **📂 Otros** | Cualquier archivo huérfano con extensión diferente a las anteriores |

*Nota: Los directorios o carpetas existentes en la raíz seleccionada serán ignorados explícitamente para proteger tus subcarpetas personales.*

---

## 🛠️ Instalación y Requisitos

### Requisitos Previos
* Tener instalado **Python 3.7** o superior. Puedes descargarlo desde [python.org](https://www.python.org/).

### Instrucciones de Instalación

1. **Clona o descarga este repositorio** en tu máquina:
   ```bash
   git clone https://github.com/tu-usuario/organizador-magico-premium.git
   cd organizador-magico-premium
   ```

2. **Instala las dependencias necesarias** ejecutando el siguiente comando en tu terminal/consola:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Modo de Uso

1. Ejecuta la aplicación principal:
   ```bash
   python organizador_premium.py
   ```
2. Haz clic en el botón **"Seleccionar"** para elegir la carpeta que deseas organizar (por ejemplo, tu carpeta de *Descargas*).
3. Presiona el botón gigante **"Limpiar y Organizar"** para iniciar la magia. Podrás ver el progreso detallado en el *Registro de Actividad*.
4. Si necesitas volver atrás, presiona el botón **"Deshacer"** o usa la combinación de teclas **`Ctrl + Z`** con la ventana de la aplicación enfocada.

---

## 📦 Estructura del Proyecto

```text
organizador-magico-premium/
│
├── organizador_premium.py  # Script principal de la aplicación (Lógica + GUI)
├── requirements.txt         # Dependencias externas necesarias (customtkinter)
└── README.md                # Documentación del proyecto (Este archivo)
```

---

## 🤝 Contribuciones

Las contribuciones, sugerencias y reportes de errores son bienvenidos. Siéntete libre de abrir un *Issue* o enviar un *Pull Request* para añadir nuevas extensiones, mejorar la estética de la UI o agregar traducciones.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo de licencia para obtener más detalles.

---

*Desarrollado con ❤️ para facilitarte el orden digital diario.*
