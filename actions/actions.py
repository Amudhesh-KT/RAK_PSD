# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import base64
from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from rasa_sdk.events import SlotSet
#
#

client = MongoClient('mongodb+srv://damudheshkt:Amudhesh_rasa@cluster0.upd64s4.mongodb.net/')
db = client['RAK_PSD']
complaint_collection = db['complaints']
suggestion_collection = db['suggestions']

class ActionSendOptions(Action):

    def name(self) -> Text:
        return "action_send_options_english"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "welcome": [
                    {
                        "type": "title", "value":"How may we help you?"
                    },
                    {
                        "type":"button","value":"Raise a complaint"
                    },
                    {
                        "type":"button","value":"Track a complaint"
                    },
                    {
                        "type":"button","value":"Suggestion"
                    },
                    {
                        "type":"button","value":"Apply for service"
                    }
                    ]
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)
        return []
    
class ActionRaiseComplaint(Action):

    def name(self) -> Text:
        return "action_send_raise_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "formType": "raise a complaint",
                    "form":[
		                {
                            "type":"text","value":"Enter complaint details"
		                },
		                {
                            "type":"doc","value":"Give attachments if any"
		                }
                    ]
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return []
    
class ActionSendComplaintID(Action):

    def name(self) -> Text:
        return "action_send_complaintid"
    
    def run(self ,dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        resp = {
                "formType": "track your complaint",
	            "form":[
	                    {
                            "type":"text","value":"Enter complaint number"
	                    }
                        ]
                }

        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return[]
    

class ActionAskforTrackComments(Action):

    def name(self) -> Text:
        return "action_send_track_comments"
    
    def run(self ,dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        
        complaint_id = tracker.get_slot("complaint_id")
        print(f"{complaint_id}")
        resp = {
                "formType": "track your complaint",
                "trackID": complaint_id,
	            "form":[
	                    {
                            "type":"text","value":"Enter comments if any",
                            
	                    }
                        ]
                }

        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return[]

class ActionSuggestionForm(Action):

    def name(self) -> Text:
        return "action_send_suggestion_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "formType": "suggestion",
                    "form":[
		                {
                            "type":"text","value":"Enter suggestion if any"
		                },
		                {
                            "type":"doc","value":"Give attachments if any"
		                }
                    ]
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return []
    
class ActionSuggestionForm(Action):

    def name(self) -> Text:
        return "action_send_apply_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "msg": "Please download the mRAK application for services.",
                    "redirectLink": "https://play.google.com/store/apps/details?id=ae.rak.ega.mrak"
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return []
    
class ActionSubmitComplaint(Action):

    def name(self) -> Text:
        return "action_submit_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata = tracker.latest_message.get("metadata")
        complaint_form = metadata.get("complaint_form", {})


        c = 1000
        for _ in complaint_collection.find():
            c += 1
        col_id = 'RAK' + str(c)
        username = complaint_form.get("username")
        email = complaint_form.get("email")
        location = complaint_form.get("location")
        complaint_details = complaint_form.get("complaint_details")
        attachments = complaint_form.get("attachments")
        complaint_status = complaint_form.get("complaint_status")
        comments = complaint_form.get("comments")

    # Create a document to store in the complaint_collection
        document = {
            'username': username,
            'email': email,
            'location': location,
            'complaint_details': complaint_details,
            'attachments': attachments,
            'complaint_id': col_id,
            'complaint_status': complaint_status,
            'comments': comments
        }

            # Insert the document into the complaint_collection
        result = complaint_collection.insert_one(document)
        file_id = str(result.inserted_id)
        dispatcher.utter_message(text=f"Complaint with ID: {col_id} has been raised successfully.")
        

        return []
    
class ActionSubmitTrack(Action):

    def name(self) -> Text:
        return "action_submit_track"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata = tracker.latest_message.get("metadata")
        track_form = metadata.get("track_form", {})


        c = 1000
        for _ in complaint_collection.find():
            c += 1
        col_id = 'RAK' + str(c)
        complaint_id = track_form.get("complaint_id")
        comments = track_form.get("comments")
        
        resp = complaint_collection.update_one({'complaint_id':complaint_id},{"$set":{'comments':comments}})
        return []
    
class ActionSubmitSuggestion(Action):

    def name(self) -> Text:
        return "action_submit_suggestion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata = tracker.latest_message.get("metadata")
        suggestion_form = metadata.get("suggestion_form", {})

        username = suggestion_form.get("username")
        email = suggestion_form.get("email")
        location = suggestion_form.get("location")
        suggestion_details = suggestion_form.get("complaint_details")
        attachments = suggestion_form.get("attachments")

    # Create a document to store in the complaint_collection
        document = {
            'username': username,
            'email': email,
            'location': location,
            'complaint_details': suggestion_details,
            'attachments': attachments,
        }

            # Insert the document into the complaint_collection
        result = suggestion_collection.insert_one(document)
        file_id = str(result.inserted_id)
        dispatcher.utter_message(text="Suggestion saved")
        

        return []