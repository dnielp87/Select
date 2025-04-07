import streamlit as st
import pandas as pd
import re

# Intentar importar librerías para extracción de texto
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

# Intentar importar pipeline de transformers para resumen
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

# Función para extraer texto de archivos subidos (PDF, DOCX o TXT)
def extract_text(file):
    if file is None:
        return ""
    file.seek(0)  # Asegurarse de leer desde el inicio
    if file.type == "application/pdf":
        if PyPDF2 is not None:
            try:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
            except Exception as e:
                st.error(f"Error al extraer texto del PDF: {e}")
                return ""
        else:
            st.error("PyPDF2 no está instalado.")
            return ""
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        if docx is not None:
            try:
                document = docx.Document(file)
                text = "\n".join([para.text for para in document.paragraphs])
                return text
            except Exception as e:
                st.error(f"Error al extraer texto del DOCX: {e}")
                return ""
        else:
            st.error("python-docx no está instalado.")
            return ""
    elif file.type == "text/plain":
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error al leer el archivo de texto: {e}")
            return ""
    else:
        st.error("Tipo de archivo no soportado.")
        return ""

# Función para resumir el descriptor usando un pipeline de transformers (si está disponible)
def summarize_descriptor(text):
    if pipeline is not None:
        try:
            summarizer = pipeline("summarization")
            summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            st.error(f"Error en la summarization: {e}")
            return text[:500]  # Fallback: muestra los primeros 500 caracteres
    else:
        # Resumen simple: muestra las primeras 10 líneas
        lines = text.splitlines()
        return "\n".join(lines[:10])

# Función para analizar un CV en función de los requerimientos
def analyze_candidate(candidate_text, required_title, required_years, req_tech_skills, req_soft_skills, req_functions):
    score = 0
    comments = []
    
    # Evaluar Formación Académica
    if required_title.lower() in candidate_text.lower():
        score += 25
    else:
        comments.append("Título académico requerido no encontrado.")
    
    # Evaluar Años de Experiencia: buscar patrones de "X años" o "X años de experiencia"
    exp_matches = re.findall(r'(\d+)\s*(?:años|años de experiencia)', candidate_text, re.IGNORECASE)
    candidate_years = 0
    if exp_matches:
        candidate_years = max([int(x) for x in exp_matches])
    if candidate_years >= required_years:
        score += 25
    else:
        comments.append("Años de experiencia insuficientes.")
    
    # Evaluar Habilidades Técnicas
    found_tech = []
    for skill in req_tech_skills:
        if skill.lower() in candidate_text.lower():
            found_tech.append(skill)
    if len(found_tech) >= max(1, len(req_tech_skills)//2):
        score += 25
    else:
        comments.append("Falta de habilidades técnicas.")
    
    # Evaluar Competencias Blandas
    found_soft = []
    for skill in req_soft_skills:
        if skill.lower() in candidate_text.lower():
            found_soft.append(skill)
    if len(found_soft) >= max(1, len(req_soft_skills)//2):
        score += 15
    else:
        comments.append("Falta de competencias blandas.")
    
    # Evaluar Funciones Clave
    found_func = []
    for func in req_functions:
        if func.lower() in candidate_text.lower():
            found_func.append(func)
    if found_func:
        score += 10
    else:
        comments.append("No se detectan funciones clave.")
    
    # Determinar el nivel de afinidad
    if score >= 90:
        affinity = "Muy Alta"
    elif score >= 75:
        affinity = "Alta"
    elif score >= 50:
        affinity = "Media"
    elif score >= 25:
        affinity = "Baja"
    else:
        affinity = "Muy Baja"
    
    recommended = "Sí" if score >= 75 and not comments else "No"
    
    return score, affinity, ", ".join(comments), candidate_years

# --- Interfaz de la App con Streamlit ---
st.title("Sistema de Gestión de Descriptores de Cargo y Evaluación de CVs con IA")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Seleccione una opción", ["Generar Descriptor", "Resumir Descriptor", "Analizar CVs"])

if menu == "Generar Descriptor":
    st.header("Generar Descriptor de Cargo")
    with st.form("generar_descriptor"):
        nombre_cargo = st.text_input("Nombre del Cargo")
        area = st.text_input("Área / Gerencia")
        proposito = st.text_area("Propósito del Cargo")
        funciones = st.text_area("Principales Funciones (separar por coma)")
        requisitos_academicos = st.text_input("Requisitos Académicos")
        anos_experiencia = st.text_input("Años de Experiencia")
        habilidades_tecnicas = st.text_area("Habilidades Técnicas (separar por coma)")
        competencias_blandas = st.text_area("Competencias Blandas (separar por coma)")
        condiciones_especiales = st.text_area("Condiciones Especiales (si existen)")
        submit_descriptor = st.form_submit_button("Generar Descriptor")
        if submit_descriptor:
            descriptor = f"""Nombre del Cargo: {nombre_cargo}
Área / Gerencia: {area}
Propósito del Cargo: {proposito}
Principales Funciones: {funciones}
Requisitos Académicos: {requisitos_academicos}
Años de Experiencia: {anos_experiencia}
Habilidades Técnicas: {habilidades_tecnicas}
Competencias Blandas: {competencias_blandas}
Condiciones Especiales: {condiciones_especiales if condiciones_especiales.strip() else "Ninguna"}
"""
            st.subheader("Descriptor de Cargo Generado")
            st.code(descriptor, language="text")
            st.download_button("Descargar Descriptor", descriptor, file_name="descriptor_cargo.txt")

elif menu == "Resumir Descriptor":
    st.header("Resumir Descriptor de Cargo Existente")
    st.write("Suba el archivo del Descriptor de Cargo (PDF, DOCX o TXT):")
    uploaded_descriptor = st.file_uploader("Elija un archivo", type=["pdf", "docx", "txt"])
    if uploaded_descriptor is not None:
        text = extract_text(uploaded_descriptor)
        st.subheader("Texto Extraído del Descriptor")
        st.text_area("Descriptor", text, height=200)
        if st.button("Resumir Descriptor"):
            summary = summarize_descriptor(text)
            st.subheader("Resumen Ejecutivo del Descriptor")
            st.text_area("Resumen", summary, height=150)

elif menu == "Analizar CVs":
    st.header("Analizar CVs contra el Descriptor")
    st.write("Ingrese o suba el Resumen del Descriptor de Cargo:")
    descriptor_summary_input = st.text_area("Resumen del Descriptor", height=150)
    
    st.subheader("Especifique las Características Requeridas del Cargo")
    required_title = st.text_input("Título académico requerido")
    required_years = st.number_input("Años de experiencia requeridos", min_value=0, step=1, value=0)
    req_tech_skills = st.text_input("Habilidades Técnicas requeridas (separadas por coma)")
    req_soft_skills = st.text_input("Competencias Blandas requeridas (separadas por coma)")
    req_functions = st.text_input("Funciones clave requeridas (5-7, separadas por coma)")
    req_tech_skills_list = [x.strip() for x in req_tech_skills.split(",") if x.strip()]
    req_soft_skills_list = [x.strip() for x in req_soft_skills.split(",") if x.strip()]
    req_functions_list = [x.strip() for x in req_functions.split(",") if x.strip()]
    
    st.write("Suba los archivos de los CVs (PDF, DOCX o TXT):")
    uploaded_cvs = st.file_uploader("Cargar CVs", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
    if st.button("Analizar CVs"):
        results = []
        if uploaded_cvs:
            for cv in uploaded_cvs:
                cv_text = extract_text(cv)
                score, affinity, comments, candidate_years = analyze_candidate(
                    cv_text, 
                    required_title, 
                    required_years, 
                    req_tech_skills_list, 
                    req_soft_skills_list, 
                    req_functions_list
                )
                results.append({
                    "Nombre Archivo": cv.name,
                    "Puntaje": score,
                    "Afinidad": affinity,
                    "Comentarios": comments,
                    "Años de Experiencia (Extraídos)": candidate_years
                })
            df = pd.DataFrame(results)
            st.subheader("Resultados de la Evaluación")
            st.dataframe(df)
            st.subheader("Visualización de Puntajes")
            st.bar_chart(df.set_index("Nombre Archivo")["Puntaje"])
        else:
            st.error("Por favor, suba al menos un CV.")

