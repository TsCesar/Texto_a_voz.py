#Import de todo lo necesario
import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from docx import Document

def RutaLimpia(path): #Limpia la ruta del archio si contiene comillas adicionales
    return path.strip(' "\'')

def BuscarTexto(url): #Extrae el texto de un artículo de una URL que proporciona el usuario
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string if soup.title else "Sin título" #Introduce el título
        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text() for p in paragraphs)#Extra el texto de la URL
        
        if not text.strip(): #Si no se puede extraer nada de la URL
            raise ValueError("No se pudo extraer el contenido del artículo.")

        return title, text
    except Exception as e:
        print(f"Error al procesar el artículo: {e}")
        return None, None

def TextoAudio(text, output_file): #Convierte el texto extraido a audio en formato MP3
    try:
        tts = gTTS(text, lang='es')
        tts.save(output_file)
        print(f"Audio guardado como {output_file}")
    except Exception as e:
        print(f"Error al generar el audio: {e}")

def ExtraerTextoArchivo(file_path): #Lee texto desde un archivo local, soportando .txt y .docx.
    try:
        if file_path.endswith('.docx'):
            doc = Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            raise ValueError("Formato de archivo no soportado. Use un archivo .txt o .docx.")
        
        return text
    except Exception as e: #Si da error 
        print(f"Error al leer el archivo: {e}")
        return None

def main(option, value): #Función principal para el desarrollo del audio
    if option == "1":
        print("Extrayendo contenido del artículo...")
        title, text = BuscarTexto(value)
        if text:
            print(f"Título: {title}")
            print("Convirtiendo el texto a audio...")
            output_file = "output.mp3"
            TextoAudio(text, output_file)
        else:
            print("No se pudo extraer el texto del artículo.")
    elif option == "2":
        value = RutaLimpia(value)
        print("Leyendo contenido del archivo...")
        text = ExtraerTextoArchivo(value)
        if text:
            print("Convirtiendo el texto a audio...")
            output_file = "output.mp3"
            TextoAudio(text, output_file)
        else:
            print("No se pudo leer el archivo.")
    else:
        print("Opción no válida.")

if __name__ == "__main__": #Inicio del programa
    simulated_option = input("Selecciona entre las opcciones '1' para URL, '2' para archivo: ") #Pregunta por la opcción que se va a utilizar
    simulated_value = input("Introduce la URL o la ruta de archivo: ") #Pide la URL o la ruta del archivo
    main(simulated_option, simulated_value)
