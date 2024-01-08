from fastapi import FastAPI
import json
# uvicorn main:app --reload
app = FastAPI()

# Chemin vers le fichier JSON contenant les données des cours
courses_file_path = "course.json"
salle_file_path= "course_date.json"

# Charger les données des cours depuis le fichier JSON
with open(courses_file_path, "r") as file:
    courses_data = json.load(file)

with open(salle_file_path, "r") as file:
    salles_data = json.load(file)

@app.get("/courses/")
async def get_courses(formation: str):
    matching_courses = [course for course in courses_data["courses"] if course["formation"] == formation]
    print(matching_courses)
    return {"courses": matching_courses}


@app.get("/room-availability/")
async def check_room_availability(name: str):
    available = False
    for room in salles_data["rooms"]:
        if room["name"] == name:
            available = room["current_availability"]
            break
    print(available)
    return {"available": available}

@app.get("/room-date/")
async def check_room_availability_date(name: str, date: str, time: str):
    for room in salles_data["rooms"]:
        if room["name"] == name:
            availability = room.get("availability")
            availability_key = f"{date}T{time}"
            if availability_key in availability:
                room_available = availability[availability_key]
                return {"available": room_available}
    
    return {"available": False}



