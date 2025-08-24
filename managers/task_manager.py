from uuid import UUID

from .milestones.model import milestone
from .task.model import Task


class TaskManager:
    # 6️⃣  Called immediately after MilestoneManager.mark_active
    @staticmethod
    def create_tasks( active_milestone: milestone):
        """
        Returns task objects ready for insert (status = 'pending').
        """
        pass

    # 7️⃣  Scheduling layer decides which task to pull next
    def mark_active(self,task_id: UUID) -> None:
        """Set task.status = 'active'."""

    def complete_task(self,task_id: UUID) -> None:
        # """Set task.status = 'completed'."""
        pass
    @staticmethod
    def return_task_list(milestone_id: str) -> Task: # type: ignore
        pass
        