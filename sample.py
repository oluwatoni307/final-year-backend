def get_sample_task_completion_data():
    """Return sample data matching TaskCompletionDto structure"""
    return {
        "task_id": "task_123",
        "goal_name": "Learn Python Programming",
        "milestone_name": "Complete FastAPI Tutorial",
        "task_title": "Build REST API endpoints",
        "ritual": "Code for 30 minutes daily after morning coffee",
        "user_notes": "Successfully implemented CRUD operations and learned about Pydantic validation",
        "status": "completed"
    }
    

def get_sample_daily_analytics():
    return {
        "habit_completion_rate": 0.75,
        "goal_completion_rate": 0.60,
        "last_7_days_habit": {
            "Mon": 0.8,
            "Tue": 0.6,
            "Wed": 0.9,
            "Thu": 0.7,
            "Fri": 0.5,
            "Sat": 0.8,
            "Sun": 0.9
        },
        "goals_breakdown": [
            {"name": "Learn Python", "completion_rate": 0.85},
            {"name": "Get Fit", "completion_rate": 0.40},
            {"name": "Read More", "completion_rate": 0.65}
        ]
    }

def get_sample_monthly_analytics():
    return {
        "habits_achieved": 85,
        "goals_achieved": 3,
        "days_active": 28,
        "weekly_habit_completion": [0.75, 0.80, 0.65, 0.90],
        "weekly_goals_achieved": [1, 0, 1, 1],
        "insight": "Great month! Your consistency improved by 15% compared to last month."
    }
    
def get_sample_goal_data():
    return [
        {
            "goal_id": "goal_001",
            "goal_name": "Master Backend Development",
            "goal_analysis": "success_probability='high'",
            "status": "active"
        },
        {
            "goal_id": "goal_002", 
            "goal_name": "Learn Data Science",
            "goal_analysis": "success_probability='medium'",
            "status": "pending"
        },
        {
            "goal_id": "goal_003",
            "goal_name": "Build Mobile App",
            "goal_analysis": "success_probability='low'",
            "status": "completed"
        }
    ]

def get_sample_milestone_data():
    return {
        "goal_id": "goal_001",
        "goal_name": "Master Backend Development", 
        "goal_description": "Become proficient in Python backend technologies",
        "context": "Career advancement in software development",
        "milestones": [
            {
                "objective": "Learn FastAPI Framework",
                "success_criteria": "Build complete REST API with authentication",
                "targetDate": "2025-09-15T00:00:00",
                "enables": "Advanced API development skills",
                "status": "active",
                "assigned_timeslot": "Evening 7-9 PM"
            },
            {
                "objective": "Database Integration",
                "success_criteria": "Implement PostgreSQL with ORM",
                "targetDate": "2025-10-01T00:00:00", 
                "enables": "Full-stack data persistence",
                "status": "pending",
                "assigned_timeslot": "Weekend mornings"
            }
        ]
    }

def get_sample_task_data():
    return [
        {
            "task_id": "task_001",
            "task_type": "encoding",
            "title": "Learn FastAPI Fundamentals",
            "objective": "Understand core FastAPI concepts and basic implementation",
            "specific_actions": [
                "Read FastAPI documentation chapters 1-3",
                "Complete 3 basic API endpoint examples",
                "Practice request/response handling"
            ],
            "time_allocated": "2 hours daily",
            "cognitive_load": "medium",
            "success_metric": "Successfully create CRUD API with validation",
            "description": "Foundation task for web API development skills",
            "rating": 7,
            "status": "active"
        },
        {
            "task_id": "task_002",
            "task_type": "application",
            "title": "Build Authentication System",
            "objective": "Implement JWT-based user authentication",
            "specific_actions": [
                "Set up JWT token generation",
                "Create login/logout endpoints",
                "Add middleware for protected routes"
            ],
            "time_allocated": "3 hours",
            "cognitive_load": "high", 
            "success_metric": "Working auth system with token refresh",
            "description": "Security implementation for API access",
            "rating": 9,
            "status": "pending"
        }
    ]