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
user_collection = db['Users']

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
        metadata = tracker.latest_message.get("metadata")
        form = metadata.get("track_form",{})
        print(form)
        username = form.get("username")
        print(username)
        # username = "aravind"
        user_filter = complaint_collection.find({"username": username})
        track_id = []
        for i in user_filter:
        
            track_id_str = i.get("complaint_id")
            track_id.append(track_id_str)

        resp = {
                "formType": "track your complaint",
	            "trackbutton":track_id
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
        status_id = complaint_collection.find_one({"complaint_id": complaint_id})
        if status_id:
            print("Inside loop")
            # for status in status_id:
            # Do something with the user data
            statusI = status_id.get('complaint_status')
            complait_details = status_id.get('complaint_details')
            comments = status_id.get('comments')
            print(statusI)
            resp = {
                "formType": "track your complaint",
                "trackID": complaint_id,
                
             "complaint_details":[
                     {
                            "type":"text","value":"Enter comments if any",
                     },
                     {
                            "title":"comment","value": comments,
                     },
                     {
                            "title":"complaint_details","value":complait_details,
                     },
                     {
                            "title":"status","value": statusI,
                     }
                        ]
                }
            response_json = json.dumps(resp)
            dispatcher.utter_message(text=response_json)
            print(resp)
            
            

        
        else:
            resp = {
                "formType": "track your complaint",
	            "form":[
	                    {
                            "type":"text","value":"Invalid complaint ID",
                            
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
    
class ActionServiceForm(Action):

    def name(self) -> Text:
        return "action_send_apply_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp =  {
                    "msg": "Please download the mRAK application for services.",
                    "redirectLink": "https://play.google.com/store/apps/details?id=ae.rak.ega.mrak",
                    "isActionEnded": "completed"
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
        resp =  {
                    "msg": f"Complaint with ID: {col_id} has been raised successfully. One of our team member will contact you shortly",
                    "isActionEnded": "completed"
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text=f"Complaint with ID: {col_id} has been raised successfully. One of our team member will contact you shortly")
        

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
        
        resp1 = complaint_collection.update_one({'complaint_id':complaint_id},{"$set":{'comments':comments}})

        resp =  {
                    "msg": "Thank you for your comments",
                    "isActionEnded": "completed"
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thank you for your comments")
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
        suggestion_details = suggestion_form.get("suggestion_details")
        attachments = suggestion_form.get("attachments")

    # Create a document to store in the complaint_collection
        document = {
            'username': username,
            'email': email,
            'location': location,
            'suggestion_details': suggestion_details,
            'attachments': attachments,
        }

            # Insert the document into the complaint_collection
        result = suggestion_collection.insert_one(document)
        file_id = str(result.inserted_id)

        resp =  {
                    "msg":"Thankyou for your suggestions",
                    "isActionEnded": "completed"
                }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thankyou for your suggestions")
        

        return []
    

class ActionAdminCards(Action):

    def name(self) -> Text:
        return "action_admin_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        complaint_completed_count = complaint_collection.count_documents({"complaint_status":"completed"})
        complaint_pending_count = complaint_collection.count_documents({"complaint_status":"pending"})
        users_count = user_collection.count_documents({"role":"user"})
        complaint_count = complaint_collection.count_documents({})
        suggestion_count = suggestion_collection.count_documents({})

        resp =  {
                    "complaintRaised":complaint_count,
                    "complaintCompleted":complaint_completed_count,
                    "complaintPending":complaint_pending_count,
                    "registrationCount":users_count,
                    "complaintSuggestion":suggestion_count
                }
        
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thankyou for your suggestions")
        

        return []
    

class ActionUserslist(Action):

    def name(self) -> Text:
        return "action_user_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user = user_collection.find()
        user_list = []
        for doc in user:
            user_list.append(doc['username'])
    
        # print(user_list)

        resp =  {
                    "userName" : user_list
                }
        
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thankyou for your suggestions")
        

        return []
    

class ActionComplaintslist(Action):

    def name(self) -> Text:
        return "action_complaint_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        complaint = complaint_collection.find()
        complaint_list= []
        for doc in complaint:
            complaint_list.append(doc['complaint_id'])

        resp =  {
                    "complaint_list" : complaint_list
                }
        
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thankyou for your suggestions")
        

        return []


class ActionComplaintsDetails(Action):

    def name(self) -> Text:
        return "action_complaint_details_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata = tracker.latest_message.get("metadata")
        form = metadata.get("complaint_id_form",{})
        print(form)
        id = form.get("complaint_id")
        # id = 'RAK1012'
        print(id)
        complaint = complaint_collection.find_one({"complaint_id": id})
        if complaint:
            complaint_user = complaint.get("username")
            complaint_detail = complaint.get("complaint_details")
            complaint_status = complaint.get("complaint_status")

        resp = {
            "username":complaint_user,
            "complaint detail":complaint_detail,
            "complaint status":complaint_status
        }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)

        # dispatcher.utter_message(text="Thankyou for your suggestions")
        

        return []


class ActionSuggestionDetails(Action):

    def name(self) -> Text:
        return "action_suggestion_details_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        suggestion = suggestion_collection.find({},{'username':1,'_id':0,'suggestion_details':1})
        suggestions_list = []
        for i in suggestion:
            suggestions_list.append(i)

        # print (suggestion_list)
        resp = {
            "suggestions":suggestions_list
        }
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)
        

        return []
    
class ActionPendingComplaints(Action):

    def name(self) -> Text:
        return "action_pending_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pending_complaint = complaint_collection.find({'complaint_status':'pending'})
        pending_complaint_list= []
        for doc in pending_complaint:
            pending_complaint_list.append(doc['complaint_id'])

        resp =  {
                    "pending_complaint_list" : pending_complaint_list
                }      
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)
        

        return []
    

class ActionCompletedComplaints(Action):

    def name(self) -> Text:
        return "action_completed_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        completed_complaint = complaint_collection.find({'complaint_status':'completed'})
        completed_complaint_list= []
        for doc in completed_complaint:
            completed_complaint_list.append(doc['complaint_id'])

        resp =  {
                    "completed_complaint_list" : completed_complaint_list
                }     
        response_json = json.dumps(resp)
        dispatcher.utter_message(text=response_json)
        print(resp)
        

        return []