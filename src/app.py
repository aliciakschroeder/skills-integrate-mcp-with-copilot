"""
High School Management System API (persistent storage)
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
import json

from .db import init_db, get_session, get_activity_by_name, get_all_activities
from .models import Activity

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.on_event("startup")
def on_startup():
    # Initialize DB and seed with defaults if empty
    init_db()
    with get_session() as session:
        count = session.exec("SELECT COUNT(*) FROM activity").one()
        if count == 0:
            seed_activities = [
                {
                    "name": "Chess Club",
                    "description": "Learn strategies and compete in chess tournaments",
                    "schedule": "Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 12,
                    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
                },
                {
                    "name": "Programming Class",
                    "description": "Learn programming fundamentals and build software projects",
                    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                    "max_participants": 20,
                    "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
                },
                {
                    "name": "Gym Class",
                    "description": "Physical education and sports activities",
                    "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                    "max_participants": 30,
                    "participants": ["john@mergington.edu", "olivia@mergington.edu"]
                },
                {
                    "name": "Soccer Team",
                    "description": "Join the school soccer team and compete in matches",
                    "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                    "max_participants": 22,
                    "participants": ["liam@mergington.edu", "noah@mergington.edu"]
                },
                {
                    "name": "Basketball Team",
                    "description": "Practice and play basketball with the school team",
                    "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 15,
                    "participants": ["ava@mergington.edu", "mia@mergington.edu"]
                },
                {
                    "name": "Art Club",
                    "description": "Explore your creativity through painting and drawing",
                    "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                    "max_participants": 15,
                    "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
                },
                {
                    "name": "Drama Club",
                    "description": "Act, direct, and produce plays and performances",
                    "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                    "max_participants": 20,
                    "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
                },
                {
                    "name": "Math Club",
                    "description": "Solve challenging problems and participate in math competitions",
                    "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                    "max_participants": 10,
                    "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
                },
                {
                    "name": "Debate Team",
                    "description": "Develop public speaking and argumentation skills",
                    "schedule": "Fridays, 4:00 PM - 5:30 PM",
                    "max_participants": 12,
                    "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
                }
            ]
            for a in seed_activities:
                activity = Activity(**a)
                session.add(activity)
            session.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    activities = get_all_activities()
    return [a.dict() for a in activities]


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    activity = get_activity_by_name(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if email in (activity.participants or []):
        raise HTTPException(status_code=400, detail="Student is already signed up")

    activity.participants = (activity.participants or []) + [email]
    with get_session() as session:
        session.add(activity)
        session.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    activity = get_activity_by_name(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if email not in (activity.participants or []):
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    activity.participants = [p for p in (activity.participants or []) if p != email]
    with get_session() as session:
        session.add(activity)
        session.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
