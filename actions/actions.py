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
        resp = {
                "formType": "track your complaint",
	            "form":[
	                    {
                            "type":"text","value":"Enter comments if any"
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

        username = complaint_form.get("username")
        email = complaint_form.get("email")
        location = complaint_form.get("location")
        complaint_details = complaint_form.get("complaint_details")
        file = complaint_form.get("attachments")

        if file:
            # Read the file content as binary
            file_content = file.read()

            # Encode the file content as base64
            encoded_content = base64.b64encode(file_content).decode()

        c = 1000
        for _ in complaint_collection.find():
            c += 1
        col_id = 'RAK' + str(c)
        # Create a document to store in the complaint_collection
        document = {
                'filename': file.filename,
                'content_type': file.content_type,
                'content': encoded_content,
                'username': username,
                'email': email,
                'location': location,
                'complaint_details': complaint_details,
                'complaint_id': col_id,
                'complaint_status': 'pending',
                'comments': 'nil'
            }

            # Insert the document into the complaint_collection
        result = complaint_collection.insert_one(document)
        file_id = str(result.inserted_id)
        dispatcher.utter_message(text=f"Complaint with ID {col_id} has been raised successfully.")
        return [SlotSet("file_id", file_id)]

        return []
    