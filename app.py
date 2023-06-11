# from fastapi import FastAPI, UploadFile, Form, File
# from pymongo import MongoClient
# import base64
# import json

# app = FastAPI()

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://damudheshkt:Amudhesh_rasa@cluster0.upd64s4.mongodb.net/')
# db = client['RAK_PSD']
# complaint_collection = db['complaints']

# @app.post('/raisecomplaint')
# async def upload_file(file: UploadFile = File(...), username: str = Form(...), email: str = Form(...),
#                       location: str = Form(...), complaint_details: str = Form(...)):
#     # Read the file content as binary
#     file_content = await file.read()

#     # Encode the file content as base64
#     encoded_content = base64.b64encode(file_content).decode()

#     c = 1000
#     for i in complaint_collection.find():
#         c+=1
    
#     col_id = 'RAK'+str(c)


#     # Create a document to store in the complaint_collection
#     document = {
#         'filename': file.filename,
#         'content_type': file.content_type,
#         'content': encoded_content,
#         'username': username,
#         'email': email,
#         'location': location,
#         'complaint_details': complaint_details,
#         'complaint_id': col_id,
#         'complaint_status': 'pending',
#         'comments': 'nil'
#     }

#     # Insert the document into the complaint_collection
#     result = complaint_collection.insert_one(document)
#     file_id = str(result.inserted_id)

#     return {'file_id': file_id}

# # @app.post('/trackcomplaint')
# # async def track_complaint(complaint_id:str = Form(...)):
# #     print(complaint_id)
# #     resp = complaint_collection.find_one({'complaint_id':complaint_id})
# #     print (resp)
# #     status = resp['complaint_status']
# #     return status

# @app.post('/trackcomplaint')
# async def track_complaint(complaint_id:str = Form(...),comments:str = Form(None)):
#     if(comments=='' or comments==None):
#         print(complaint_id)
#         resp = complaint_collection.find_one({'complaint_id':complaint_id})
#         print (resp)
#         trackID = complaint_id
#         print(complaint_id)
#         status = resp['complaint_status']
#         return status
#     else:  
#         resp = complaint_collection.update_one({'complaint_id':complaint_id},{"$set":{'comments':comments}})
#         resp = complaint_collection.find_one({'complaint_id':complaint_id})
#         resp["_id"] = str(resp["_id"])
#         return resp


from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from pymongo import MongoClient

from passlib.context import CryptContext






client = MongoClient('mongodb+srv://damudheshkt:Amudhesh_rasa@cluster0.upd64s4.mongodb.net/')

db = client['RAK_PSD']

collection = db['Users']





app = FastAPI()




# Password hashing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





class UserRegister(BaseModel):

    username: str

    email: str

    password: str

    location: str





class UserLogin(BaseModel):

    username: str

    password: str





@app.post("/register")

def register(user: UserRegister):

    # Check if user already exists

    if collection.find_one({"username": user.username}):

        raise HTTPException(status_code=400, detail="User already exists")




    # Hash the password

    hashed_password = pwd_context.hash(user.password)




    # Store user in database

    user_data = {

        "username": user.username,

        "email": user.email,

        "password": hashed_password,

        "location": user.location

    }

    collection.insert_one(user_data)




    return {"message": "User registered successfully"}





@app.post("/login")

def login(user: UserLogin):

    # Find the user in the database

    db_user = collection.find_one({"username": user.username})

    if not db_user:

        raise HTTPException(status_code=400, detail="Invalid credentials")




    # Verify the password

    if not pwd_context.verify(user.password, db_user["password"]):

        raise HTTPException(status_code=400, detail="Invalid credentials")


    email = db_user.get("email")
    location = db_user.get("location")

    response = {
        "username": db_user["username"],
        "email": email,
        "location": location
    }

    print(response) 

    return {"message": "Login successful"}





if __name__ == "__main__":

    import uvicorn




    uvicorn.run(app, host="0.0.0.0", port=8000)