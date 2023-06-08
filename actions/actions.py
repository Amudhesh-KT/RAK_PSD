# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionSendOptions(Action):

    def name(self) -> Text:
        return "action_send_options_english"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "msg": "How may we help you",
                    "welcome": [
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
                    "msg": "Please find below",
                    "redirectLink": "https://www.google.com/"
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        return []
    