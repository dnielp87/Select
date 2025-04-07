def generar_descriptor_cargo():
    print("=== Generar Descriptor de Cargo ===")
    print("Por favor, ingrese la siguiente información:")
    nombre_cargo = input("Nombre del Cargo: ")
    area = input("Área / Gerencia: ")
    proposito = input("Propósito del Cargo: ")
    funciones = input("Principales Funciones (separe por comas): ")
    requisitos_academicos = input("Requisitos Académicos: ")
    anos_experiencia = input("Años de Experiencia: ")
    habilidades_tecnicas = input("Habilidades Técnicas (separe por comas): ")
    competencias_blandas = input("Competencias Blandas (separe por comas): ")
    condiciones_especiales = input("Condiciones Especiales (si existen, de lo contrario presione Enter): ")
    
    descriptor = f"""
Nombre del Cargo: {nombre_cargo}
Área / Gerencia: {area}
Propósito del Cargo: {proposito}
Principales Funciones: {funciones}
Requisitos Académicos: {requisitos_academicos}
Años de Experiencia: {anos_experiencia}
Habilidades Técnicas: {habilidades_tecnicas}
Competencias Blandas: {competencias_blandas}
Condiciones Especiales: {condiciones_especiales if condiciones_especiales else "Ninguna"}
"""
    print("\n--- Descriptor de Cargo Generado ---")
    print(descriptor)
    # Guarda el descriptor en un archivo de texto
    with open("descriptor_cargo.txt", "w", encoding="utf-8") as f:
        f.write(descriptor)
    print("El descriptor se ha guardado en 'descriptor_cargo.txt'.\n")


def resumir_descriptor_cargo():
    print("=== Resumir Descriptor de Cargo Existente ===")
    print("Por favor, adjunte (copie y pegue) el Descriptor de Cargo existente:")
    descriptor = input("Ingrese el descriptor completo: ")
    
    # Se asume que el descriptor sigue el formato estándar generado anteriormente.
    summary_dict = {}
    for line in descriptor.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            summary_dict[key.strip()] = value.strip()
    
    resumen = f"""
Nombre del Cargo: {summary_dict.get("Nombre del Cargo", "No especificado")}
Área: {summary_dict.get("Área / Gerencia", "No especificado")}
Propósito Principal: {summary_dict.get("Propósito del Cargo", "No especificado")}
Funciones Clave: {summary_dict.get("Principales Funciones", "No especificado")}
Requisitos Principales: {summary_dict.get("Requisitos Académicos", "No especificado")}, 
Años de Experiencia: {summary_dict.get("Años de Experiencia", "No especificado")}, 
Habilidades Técnicas: {summary_dict.get("Habilidades Técnicas", "No especificado")}
Competencias Relevantes: {summary_dict.get("Competencias Blandas", "No especificado")}
"""
    print("\n--- Resumen Ejecutivo del Descriptor de Cargo ---")
    print(resumen)


def analizar_cvs():
    print("=== Analizar CVs Adjuntos y Evaluarlos contra el Descriptor ===")
    print("Primero, ingrese el resumen del Descriptor de Cargo (obtenido del paso anterior):")
    resumen = input("Ingrese el resumen: ")
    
    print("\nNúmero de candidatos a evaluar:")
    num_candidates = int(input("Ingrese el número: "))
    
    candidates = []
    for i in range(num_candidates):
        print(f"\n--- Datos del Candidato {i+1} ---")
        nombre = input("Nombre del Candidato: ")
        formacion = input("Formación Académica (ingrese título obtenido): ")
        experiencia = float(input("Años de Experiencia: "))
        funciones_candidato = input("Funciones clave en su experiencia (separe por comas): ")
        habilidades_tecnicas = input("Habilidades Técnicas (separe por comas): ")
        competencias = input("Competencias Blandas (separe por comas): ")
        liderazgo = input("¿Ha liderado equipos? (si/no): ").lower().strip()
        candidates.append({
            "nombre": nombre,
            "formacion": formacion,
            "experiencia": experiencia,
            "funciones": [f.strip() for f in funciones_candidato.split(",")],
            "habilidades_tecnicas": [ht.strip() for ht in habilidades_tecnicas.split(",")],
            "competencias": [cb.strip() for cb in competencias.split(",")],
            "liderazgo": liderazgo
        })
    
    print("\n=== Especificaciones del Cargo ===")
    titulo_requerido = input("Ingrese el título académico requerido: ")
    anos_requeridos = float(input("Ingrese los años de experiencia requeridos: "))
    habilidades_requeridas = [h.strip() for h in input("Ingrese las habilidades técnicas requeridas (separe por comas): ").split(",")]
    competencias_requeridas = [c.strip() for c in input("Ingrese las competencias blandas requeridas (separe por comas): ").split(",")]
    funciones_requeridas = [f.strip() for f in input("Ingrese las funciones clave requeridas (5-7, separe por comas): ").split(",")]
    
    results = []
    for candidate in candidates:
        score = 0
        comments = []
        
        # Evaluar Formación Académica
        if titulo_requerido.lower() in candidate["formacion"].lower():
            score += 25
        else:
            comments.append("Brecha crítica: no tiene el título requerido.")
        
        # Evaluar Experiencia Laboral
        if candidate["experiencia"] >= anos_requeridos:
            score += 25
        else:
            comments.append("Experiencia insuficiente.")
        
        # Evaluar Habilidades Técnicas
        habilidades_cumplen = [ht for ht in candidate["habilidades_tecnicas"]
                                if any(hr.lower() in ht.lower() for hr in habilidades_requeridas)]
        if len(habilidades_cumplen) >= max(1, len(habilidades_requeridas)//2):
            score += 25
        else:
            comments.append("Falta de habilidades técnicas requeridas.")
        
        # Evaluar Competencias Blandas
        competencias_cumplen = [cb for cb in candidate["competencias"]
                                if any(cr.lower() in cb.lower() for cr in competencias_requeridas)]
        if len(competencias_cumplen) >= max(1, len(competencias_requeridas)//2):
            score += 15
        else:
            comments.append("Poca demostración de competencias blandas.")
        
        # Evaluar Funciones Clave
        funciones_cumplen = [fc for fc in candidate["funciones"]
                             if any(fr.lower() in fc.lower() for fr in funciones_requeridas)]
        if funciones_cumplen:
            score += 10
        else:
            comments.append("No se detectan funciones clave requeridas.")
        
        # Validación adicional: si el cargo requiere liderazgo y el candidato no ha liderado equipos.
        if ("liderar" in " ".join(funciones_requeridas).lower() or 
            "liderazgo" in " ".join(competencias_requeridas).lower()):
            if candidate["liderazgo"] != "si":
                comments.append("No ha liderado equipos, debilidad relevante.")
        
        # Asignar nota de afinidad según el puntaje obtenido.
        if score >= 90:
            afinidad = "Muy Alta"
        elif score >= 75:
            afinidad = "Alta"
        elif score >= 50:
            afinidad = "Media"
        elif score >= 25:
            afinidad = "Baja"
        else:
            afinidad = "Muy Baja"
        
        results.append({
            "Nombre": candidate["nombre"],
            "Puntaje": score,
            "Afinidad": afinidad,
            "Comentarios": "; ".join(comments) if comments else "Ninguno",
            "Recomendado": "Sí" if score >= 75 and not comments else "No"
        })
    
    print("\n--- Resultados de Evaluación de Candidatos ---")
    for r in results:
        print(f"\nCandidato: {r['Nombre']}")
        print(f"Puntaje: {r['Puntaje']}")
        print(f"Afinidad: {r['Afinidad']}")
        print(f"Comentarios: {r['Comentarios']}")
        print(f"Recomendado para entrevista: {r['Recomendado']}")
    
    print("\nTabla Resumen:")
    print("Nombre\tPuntaje\tAfinidad\tRecomendado")
    for r in results:
        print(f"{r['Nombre']}\t{r['Puntaje']}\t{r['Afinidad']}\t{r['Recomendado']}")


def main():
    print("Bienvenido al sistema de gestión de Descriptores de Cargo y Evaluación de CVs.")
    print("Seleccione una opción:")
    print("1. Generar Descriptor de Cargo")
    print("2. Resumir Descriptor de Cargo Existente")
    print("3. Analizar CVs Adjuntos y Evaluarlos contra el Descriptor")
    opcion = input("Ingrese el número de la opción: ")
    
    if opcion == "1":
        generar_descriptor_cargo()
    elif opcion == "2":
        resumir_descriptor_cargo()
    elif opcion == "3":
        analizar_cvs()
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
