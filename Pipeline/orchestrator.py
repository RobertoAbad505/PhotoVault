from typing import Callable, Optional
from Core.scanner import scan_photos
from Core.duplicates import detect_duplicates
from Core.reports import summarize_duplicates
from Core.organizer import organize_photos


class PipelineOrchestrator:

    def __init__(
        self,
        base_dir: str,
        on_event: Optional[Callable[[dict], None]] = None
    ):
        self.base_dir = base_dir
        self.on_event = on_event
        self.state = "idle"

    def _emit(self, event: dict):
        if self.on_event:
            self.on_event(event)

    def run(self):
        self.state = "running"
        self._emit({"type": "pipeline_started"})

        # 1️⃣ Scan
        self._emit({"type": "step_started", "step": "scan"})
        photos = list(scan_photos(self.base_dir, self._emit))
        self._emit({"type": "step_completed", "step": "scan", "count": len(photos)})

        # 2️⃣ Ask UI: continue?
        self._emit({"type": "await_user_decision", "decision": "continue_after_scan"})
        yield "await_decision_scan"

        # 3️⃣ Duplicates
        self._emit({"type": "step_started", "step": "duplicates"})
        dup_result = detect_duplicates(photos, self._emit)
        self._emit({"type": "step_completed", "step": "duplicates"})

        # 4️⃣ Report
        dup_report = summarize_duplicates(dup_result["duplicates"])
        self._emit({
            "type": "duplicates_report_ready",
            "report": dup_report
        })

        # 5️⃣ Ask UI: delete?
        self._emit({"type": "await_user_decision", "decision": "delete_duplicates"})
        yield "await_decision_delete"

        # 6️⃣ Ask UI: organize?
        self._emit({"type": "await_user_decision", "decision": "organize"})
        yield "await_decision_organize"

        # 7️⃣ Organize
        self._emit({"type": "step_started", "step": "organize"})
        organize_photos(
            photos,
            self.base_dir,
            mode="execute",
            on_event=self._emit
        )

        self.state = "completed"
        self._emit({"type": "pipeline_completed"})
