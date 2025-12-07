def build_prompt_master(cv_text: str, new_studies: str) -> str:
    """
    Construye el prompt para generar el CV Maestro Actualizado.
    """
    return f"[PROMPT CV MAESTRO]\nCV Base: {cv_text}\nNuevos estudios: {new_studies}"


def build_prompt_targeted(master_cv: str, job_description: str) -> str:
    """
    Construye el prompt para generar un CV optimizado para un puesto específico.
    """
    return f"[PROMPT CV TARGET]\nCV Maestro: {master_cv}\nPuesto: {job_description}"


