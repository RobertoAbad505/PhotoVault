import sys
from Pipeline.orchestrator import PipelineOrchestrator

PICTURES_DIR = "/Users/RobertoAbad/Pictures"


# --------------------------------------------------
# UI helpers
# --------------------------------------------------

def print_banner():
    print("\n" + "=" * 50)
    print("📸  PhotoVault")
    print("Gestor inteligente de fotos y duplicados")
    print("=" * 50)


def print_menu():
    print("""
1️⃣  Limpieza guiada (recomendada)
2️⃣  Escanear y generar reporte
3️⃣  Detectar duplicados (sin eliminar)
4️⃣  About PhotoVault
5️⃣  Salir
""")


def print_about():
    print("""
📸 PhotoVault
------------------------------------------
Herramienta de organización y limpieza
de archivos multimedia.

✔ Detección segura de duplicados
✔ Organización por Año / Mes / RAW
✔ Reportes detallados
✔ Arquitectura desacoplada

Autor: Roberto Abad Ramirez
📧 roberto.rmzabad@gmail.com
📱 +52 442 333 0132
🔗 linkedin.com/in/robertoabad95
💻 github.com/RobertoAbad505   
Proyecto educativo y profesional
------------------------------------------
""")


# --------------------------------------------------
# Event handler
# --------------------------------------------------

def console_event_handler(event: dict):
    event_type = event.get("type")

    if event_type == "pipeline_started":
        print("\n🚀 Pipeline iniciado\n")

    elif event_type == "step_started":
        print(f"\n▶️ Iniciando paso: {event['step']}")

    elif event_type == "step_completed":
        print(f"✅ Paso completado: {event['step']}")

    elif event_type == "scan_progress":
        print(
            f"📂 Escaneados: {event['processed']} | "
            f"Válidos: {event['accepted']}",
            end="\r"
        )

    elif event_type == "duplicate_progress":
        print(
            f"🔍 Procesados: {event['processed']} | "
            f"Únicos: {event['unique']} | "
            f"Duplicados: {event['duplicates']}",
            end="\r"
        )

    elif event_type == "duplicates_report_ready":
        report = event["report"]
        print("\n\n📊 REPORTE DE DUPLICADOS")
        print("-" * 50)
        print(f"Total archivos : {report['total_files']}")
        print(f"Total tamaño   : {report['total_size'] / (1024**3):.2f} GB")

    elif event_type == "pipeline_completed":
        print("\n🎉 Pipeline completado con éxito\n")

    elif event_type == "hash_error":
        print(f"\n⚠️ Error leyendo {event['path']}")

    elif event_type == "organize_error":
        print(f"\n❌ Error moviendo {event['source']}")


# --------------------------------------------------
# Pipeline runners
# --------------------------------------------------

def run_pipeline(mode: str):
    orchestrator = PipelineOrchestrator(
        base_dir=PICTURES_DIR,
        on_event=console_event_handler
    )

    pipeline = orchestrator.run(mode=mode)

    try:
        for step in pipeline:
            if step == "await_decision_scan":
                input("\n📊 Escaneo completo. ENTER para continuar...")

            elif step == "await_decision_delete":
                confirm = input(
                    "\n⚠️ ¿Eliminar duplicados? (yes/no): "
                )
                if confirm.lower() != "yes":
                    print("❎ Eliminación cancelada.")
                    break

            elif step == "await_decision_organize":
                confirm = input(
                    "\n📁 ¿Organizar por Año/Mes/RAW? (yes/no): "
                )
                if confirm.lower() != "yes":
                    print("❎ Organización cancelada.")
                    break

    except KeyboardInterrupt:
        print("\n⛔ Proceso interrumpido.")
        sys.exit(1)


# --------------------------------------------------
# Main loop
# --------------------------------------------------

def main():
    while True:
        print_banner()
        print_menu()

        option = input("Selecciona una opción: ").strip()

        if option == "1":
            run_pipeline(mode="guided")

        elif option == "2":
            run_pipeline(mode="scan_only")

        elif option == "3":
            run_pipeline(mode="duplicates_only")

        elif option == "4":
            print_about()
            input("\nENTER para volver al menú...")

        elif option == "5":
            print("\n👋 Hasta luego")
            sys.exit(0)

        else:
            print("\n❌ Opción inválida")


if __name__ == "__main__":
    main()
