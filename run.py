import sys
from Core.orchestrator import PipelineOrchestrator

PICTURES_DIR = "/Users/RobertoAbad/Pictures"


def console_event_handler(event: dict):
    """
    Maneja todos los eventos emitidos por el pipeline.
    """
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
            f"Archivos válidos: {event['accepted']}",
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

        print("\nPor tipo:")
        for ext, data in sorted(
            report["by_extension"].items(),
            key=lambda x: x[1]["size"],
            reverse=True
        ):
            size_gb = data["size"] / (1024**3)
            print(f"{ext:8} → {data['count']:6} archivos | {size_gb:6.2f} GB")

    elif event_type == "organize_moved":
        print(f"📁 Movido: {event['source']} → {event['destination']}")

    elif event_type == "pipeline_completed":
        print("\n🎉 Pipeline completado con éxito")

    elif event_type == "hash_error":
        print(f"\n⚠️ Error leyendo {event['path']}")

    elif event_type == "organize_error":
        print(f"\n❌ Error moviendo {event['source']}")

    elif event_type == "await_user_decision":
        # El CLI decide fuera
        pass


def run_cli():
    orchestrator = PipelineOrchestrator(
        base_dir=PICTURES_DIR,
        on_event=console_event_handler
    )

    pipeline = orchestrator.run()

    try:
        for step in pipeline:
            if step == "await_decision_scan":
                input("\n📊 Escaneo completo. ENTER para continuar...")

            elif step == "await_decision_delete":
                confirm = input(
                    "\n⚠️ ¿Deseas ELIMINAR duplicados? (yes/no): "
                )
                if confirm.lower() != "yes":
                    print("❎ Eliminación cancelada. Fin del proceso.")
                    break

            elif step == "await_decision_organize":
                confirm = input(
                    "\n📁 ¿Deseas organizar por Año/Mes/RAW? (yes/no): "
                )
                if confirm.lower() != "yes":
                    print("❎ Organización cancelada. Fin del proceso.")
                    break

    except KeyboardInterrupt:
        print("\n⛔ Proceso interrumpido por el usuario.")
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
