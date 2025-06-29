from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime
import json
from . import database
from .emailer import send_email
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")
database.init_db()

@app.get("/")
def index(request: Request):
    conn = database.get_db_connection()
    today = datetime.now()
    events = conn.execute('''
        SELECT * FROM events ORDER BY start_time ASC
    ''').fetchall()

    all_data = []
    for e in events:
        members = conn.execute('SELECT name, email FROM members WHERE event_id = ?', (e['id'],)).fetchall()
        all_data.append({
            "title": e["title"],
            "description": e["description"],
            "start_time": e["start_time"],
            "end_time": e["end_time"],
            "members": members
        })
    return templates.TemplateResponse("index.html", {
        "request": request,
        "events": all_data,
        "now": today.strftime("%A, %d %B %Y %I:%M %p")
    })

@app.post("/add")
def add_event(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    start_time: str = Form(...),
    end_time: str = Form(...),
    members: str = Form(...)
):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (title, description, start_time, end_time)
        VALUES (?, ?, ?, ?)
    ''', (title, description, start_time, end_time))
    event_id = cursor.lastrowid

    members_data = json.loads(members)
    for member in members_data:
        cursor.execute('''
            INSERT INTO members (event_id, name, email)
            VALUES (?, ?, ?)
        ''', (event_id, member['name'], member['email']))
        send_email(
            member['email'],
            f"📅 New Meeting Scheduled: {title}",
            f"Hello {member['name']},\n\nYou have a new meeting scheduled:\n\nTitle: {title}\nDescription: {description}\nStart: {start_time}\nEnd: {end_time}\n\nRegards,\nEvent Scheduler"
        )

    conn.commit()
    return RedirectResponse("/", status_code=303)