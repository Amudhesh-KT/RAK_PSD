from fastapi import FastAPI, UploadFile, Form, File
from pymongo import MongoClient
import base64
import json

app = FastAPI()

# Connect to MongoDB
client = MongoClient('mongodb+srv://damudheshkt:Amudhesh_rasa@cluster0.upd64s4.mongodb.net/')
db = client['RAK_PSD']
complaint_collection = db['complaints']

@app.post('/raisecomplaint')
async def upload_file(file: UploadFile = File(...), username: str = Form(...), email: str = Form(...),
                      location: str = Form(...), complaint_details: str = Form(...)):
    # Read the file content as binary
    file_content = await file.read()

    # Encode the file content as base64
    encoded_content = base64.b64encode(file_content).decode()

    c = 1000
    for i in complaint_collection.find():
        c+=1
    
    col_id = 'RAK'+str(c)


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

    return {'file_id': file_id}

# @app.post('/trackcomplaint')
# async def track_complaint(complaint_id:str = Form(...)):
#     print(complaint_id)
#     resp = complaint_collection.find_one({'complaint_id':complaint_id})
#     print (resp)
#     status = resp['complaint_status']
#     return status

@app.post('/trackcomplaint')
async def track_complaint(complaint_id:str = Form(...),comments:str = Form(None)):
    if(comments=='' or comments==None):
        print(complaint_id)
        resp = complaint_collection.find_one({'complaint_id':complaint_id})
        print (resp)
        status = resp['complaint_status']
        return status
    else:  
        resp = complaint_collection.update_one({'complaint_id':complaint_id},{"$set":{'comments':comments}})
        resp = complaint_collection.find_one({'complaint_id':complaint_id})
        resp["_id"] = str(resp["_id"])
        return resp


