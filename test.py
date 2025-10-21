# scripts/show_real_responses.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def show_resp(resp):
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    print(f"== {resp.request.method} {resp.request.url} -> {resp.status_code} ==")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    print()

def main():
    # GET /home
    # show_resp(requests.get(f"{BASE_URL}/home"))

    # GET /goals
    # show_resp(requests.get(f"{BASE_URL}/goals"))

    # POST /goals/analyze (adjust payload to your GoalInput model)
    # show_resp(requests.post(f"{BASE_URL}/goals/analyze", json={
    #     "statement": "Complete my Python project",
    #     "date": "2025-12-31T23:59:59",
    #     "importance": 8,
    #     "context": "I have intermediate Python skills, experience with FastAPI, and 10 hours per week available to work on this"
    # }))
    # POST /goals/verify_and_save (adjust payload to your model)
#     show_resp(requests.post(f"{BASE_URL}/goals/verify_and_save", json={
#     "goal_type": "Achievement",
#     "specific": 6,
#     "complexity": "Moderate",
#     "motivation": "Intrinsic",
#     "skill_level": "Small",
#     "dependencies": "Independent",
#     "measurability": "Milestone",
#     "decomposability": "Medium",
#     "urgency": "Medium",
#     "autonomy": "Self-Directed",
#     "readiness": "Ready",
#     "identity_alignment": "Medium",
#     "goal_classification": "Moderate Achievement Goal with Medium Identity Alignment and Small Skill Gap",
#     "complexity_rating": 6.0,
#     "success_probability": "Medium",
#     "recommended_approach": "Structure milestones..."
# }))
    # # POST /goals
    # show_resp(requests.get(f"{BASE_URL}/goals", json={
    #     "id": "g1",
    #     "name": "My Goal",
    #     "completion_rate": 0.0,
    #     "is_completed": False
    # }))

    # GET /goals/{goal_id}/milestones
    # show_resp(requests.get(f"{BASE_URL}/goals/1a2155ae-8adf-4dbe-b9bc-d78f831cc66d/milestones"))

    # GET /milestones/{milestone_id}/tasks
    # show_resp(requests.get(f"{BASE_URL}/milestones/07e9a05c-714a-4bc1-974a-dc86a9ee00dc/tasks"))

# #     # GET /tasks/{task_id}/completion
#     show_resp(requests.get(f"{BASE_URL}/tasks/d21f9a21-8666-4fdb-a414-b3d47565ba8f/completion"))

# #     # PATCH /tasks/{task_id}
#     show_resp(requests.patch(f"{BASE_URL}/tasks/t1", json={"completed": True, "notes": "Done"}))

#     # GET /analytics/daily
    show_resp(requests.get(f"{BASE_URL}/analytics/daily"))

#     # GET /analytics/monthly
    show_resp(requests.get(f"{BASE_URL}/analytics/monthly"))

#     # GET /schedule
#     show_resp(requests.get(f"{BASE_URL}/schedule"))

if __name__ == "__main__":
    main()
