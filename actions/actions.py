from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import os

class ActionGetUserName(Action):
    def name(self) -> Text:
        return "action_get_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message.get('text')

        if "Mon nom est" in message:
            name = message.split("Mon nom est")[1].strip()
        elif "Je m'appelle" in message:
            name = message.split("Je m'appelle")[1].strip()
        elif "Appelez-moi" in message:
            name = message.split("Appelez-moi")[1].strip()
        else:
            name = None

        if name:
            dispatcher.utter_message(text=f"Votre nom est c'est bon  {name}!")
        else:
            dispatcher.utter_message(text="Je n'ai pas pu récupérer votre nom.")

        return []
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
courses_file_path = "data/course.json"
class ActionGetSchedule(Action):
    def name(self) -> Text:
        return "action_get_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        groupe_entity = next(tracker.get_latest_entity_values("groupe"), None)
        enseignant_entity = next(tracker.get_latest_entity_values("enseignant"), None)
        salle_entity = next(tracker.get_latest_entity_values("salle"), None)

        response = "Voici les cours disponibles pour aujourd'hui :"

        with open(courses_file_path, "r") as file:
            courses_data = json.load(file)
        
        if groupe_entity:
            response += f" pour le groupe {groupe_entity}"
            

        if enseignant_entity:
            response += f" de l'enseignant {enseignant_entity}"

        if salle_entity:
            response += f" dans la salle {salle_entity}"

        # Utilisez les données pour dispatcher les cours, par exemple :
        dispatcher.utter_message(text=f"Voici les cours : {courses_data['courses']}")
        
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetFORMATIONS(Action):
    def name(self) -> Text:
        return "action_get_formation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        formation = next(tracker.get_latest_entity_values("formation"), None)

        if formation:
            url = f"http://127.0.0.1:8000/courses/?formation={formation}"
            response = requests.get(url)
            courses = response.json()["courses"]
            courses_response = ""
            for course in courses:
                course_details = (
                    f"Cours {course['course_name']} (Groupe {course['group']}), enseigné par {course['teacher']} "
                    f"dans la salle {course['room']['name']} au créneau {course['time']}."
                )

            courses_response += course_details + "\n"


            if courses:
                dispatcher.utter_message(text=f"Voici les cours pour la formation {formation}: {courses_response}")
            else:
                dispatcher.utter_message(text=f"Aucun cours trouvé pour la formation {formation}")
        else:
            dispatcher.utter_message(text="Je n'ai pas compris la formation spécifiée.")

        return []
    

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionCheckRoomAvailability(Action):
    def name(self) -> Text:
        return "action_check_room_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        room_name = tracker.get_slot("room")  # Obtenir le nom de la salle de l'entité correspondante

        # Faire une requête à votre API pour vérifier la disponibilité de la salle
        url = f"http://127.0.0.1:8000/room-availability/?name={room_name}"  # Adapter l'URL à votre API
        response = requests.get(url)
        
        if response.status_code == 200:
            room_info = response.json()
            print(" je suissss Dansss Actions")
            print(room_info)
            if room_info.get("available"):
                dispatcher.utter_message(text=f"La salle {room_name} est disponible.")
            else:
                dispatcher.utter_message(text=f"La salle {room_name} n'est pas disponible.")

        else:
            dispatcher.utter_message(text="Désolé, je n'ai pas pu vérifier la disponibilité de la salle pour le moment.")

        return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionCheckRoomAvailabilityDate(Action):
    def name(self) -> Text:
        return "action_check_room_availability_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        room_name = tracker.get_slot("room")
        time = tracker.get_slot("time")
        date = tracker.get_slot("date")
        if room_name:
            url = f"http://127.0.0.1:8000/room-date/?name={room_name}&time={time}&date={date}"
            response = requests.get(url)
            room_info = response.json()
            print( room_info)
            if room_info.get("available"):
                dispatcher.utter_message(text=f"La salle {room_name} est  disponible.")
            else:
                dispatcher.utter_message(text=f"La salle {room_name}  n' est  pas  disponible.")
        else:
            dispatcher.utter_message(text="Je n'ai pas compris la salle spécifiée.")

        return []

# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Récupérer la ville et le moment (temps) à partir des slots
        city = tracker.get_slot("city")
        times = tracker.get_slot("times")

        # Utiliser une valeur par défaut si la ville ou le moment n'est pas spécifié
        city = city if city else "Paris"
        times = times if times else "maintenant"

        # Clé API pour le service OpenWeatherMap
        api_key = "e8667bfb9b5430b9a27438426a770ec7"

        # URL pour l'API OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        # Faire une requête à l'API OpenWeatherMap
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Récupérer la température et la description de la météo
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            # Envoyer le message avec les informations météorologiques
            dispatcher.utter_message(text=f"La météo à {city} pour {times} est : {temperature}°C, {weather_description}.")
        else:
            # Message d'erreur si la requête a échoué
            dispatcher.utter_message(
                text="Je n'ai pas pu récupérer la météo pour vous. Veuillez vérifier si la localisation est correcte.")

        return []
class ActionShowRoomInfo(Action):
    def name(self) -> Text:
        return "action_show_room_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        salle_name = tracker.get_slot('salle')
        room_info = self.get_room_info(salle_name)
        if room_info:
            dispatcher.utter_message(text=room_info['description'])
        else:
            dispatcher.utter_message(text="Désolé, je n'ai pas trouvé d'informations sur cette salle.")
        return []

    def get_room_info(self, salle_name):
        file_path = os.path.join(os.path.dirname(__file__), '../data/salles.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            for room in data['salles']:
                if room['nom'].lower() == salle_name.lower():
                    return room
        return None

class ActionShowDirections(Action):
    def name(self) -> Text:
        return "action_show_directions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        salle_depart = tracker.get_slot('salle_depart')
        salle_arrivee = tracker.get_slot('salle_arrivee')
        directions = self.get_directions(salle_depart, salle_arrivee)
        if directions:
            dispatcher.utter_message(text=directions)
        else:
            dispatcher.utter_message(text="Je ne peux pas trouver le chemin entre ces salles.")
        return []

    def get_directions(self, salle_depart, salle_arrivee):
        file_path = os.path.join(os.path.dirname(__file__), '../data/salles.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            for direction in data['directions']:
                if direction['de'] == salle_depart and direction['vers'] == salle_arrivee:
                    return direction['chemin']
        return None

class ActionShowSalleLocation(Action):
    def name(self) -> Text:
        return "action_show_salle_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        salle_name = tracker.get_slot('salle')
        dispatcher.utter_message(text=f"De quelle salle partez-vous pour aller à la salle {salle_name}?")
        return []

class ActionShowRoomPlan(Action):
    def name(self) -> Text:
        return "action_show_room_plan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        salle_name = tracker.get_slot('salle')
        room_info = self.get_room_info(salle_name)
        if room_info and 'plan' in room_info:
            plan_url = room_info['plan']
            dispatcher.utter_message(text=plan_url)
        else:
            dispatcher.utter_message(text="Désolé, je n'ai pas de plan pour cette salle.")
        return []

    def get_room_info(self, salle_name):
        file_path = os.path.join(os.path.dirname(__file__), '../data/salles.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            for room in data['salles']:
                if room['nom'].lower() == salle_name.lower():
                    return room
        return None

class ActionSetSalleDepart(Action):
    def name(self) -> Text:
        return "action_set_salle_depart"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        salle_depart = self.extract_salle_from_text(user_message)
        if salle_depart:
            return [SlotSet("salle_depart", salle_depart)]
        else:
            dispatcher.utter_message(text="Je n'ai pas compris quelle est votre salle de départ.")
            return []

    def extract_salle_from_text(self, text):
        # Exemple d'extraction simple. Peut être amélioré avec NER ou des règles plus complexes.
        match = re.search(r'salle\s+([A-Z])', text, re.IGNORECASE)
        return match.group(1) if match else None
