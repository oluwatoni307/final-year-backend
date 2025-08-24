# goal achievement
#  milestone
# timekeeper
from goal_define_process import goal_definer
from models.milestone import status_state
from task_decompostion import task
from milestone_module import milestone_master
from timetable import timetable
from DBhelper import save
from milestone import milestones
from task_model import status_state as status
from milestone import status_state

def workflow(goal_info):
    """
    Execute the workflow for goal achievement, milestone setting, and timetable generation.
    """
  
    # Step 1: Define the goal
    goal = goal_definer(goal_info)

    # # Step 2: Set milestones based on the goal
    milestones = milestone_master(goal)
      # ✅ Step 2.1: Activate the first milestone
    if milestones:  # Make sure the list is not empty
        milestones[0].status = status_state.active
        active_milestone = milestones[0]

    
    save(goal, milestones)
    
    
    
    
    
def active_flow(milestone):
    """    Activate the next milestone in the workflow."""
    timetable(milestone)
    tasks = task(milestone)
    if tasks:  # Make sure the list is not empty
        tasks.tasks[0].status = status.active
    save(tasks, "")
    
    
    
    

    
    
    

    
    

    # # Step 3: Generate a timetable based on the milestones
    # schedule = timetable(milestones)

    # return {
    #     "goal": goal,
    #     "milestones": milestones,
    #     "schedule": schedule
    # }
