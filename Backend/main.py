from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from entities import FeedbackRequest
from utils.json_formatter import format_feedback_json
from fastapi.middleware.cors import CORSMiddleware
from utils.mongo_connector import save_feedback_to_mongo
from fastapi import UploadFile, File
from utils.csv_processor import process_csv
from utils.dashboard_data import get_dashboard_data


app = FastAPI(title="Feedback Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  #  allow requests from frontend
    allow_credentials=False,
    allow_methods=["*"],  # or just ["POST", "GET"]
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Feedback Analyzer API"}

@app.post("/analyze-feedback")
def analyze_feedback(data: FeedbackRequest):
    output = format_feedback_json(data.feedback_text, data.user_id)
    save_feedback_to_mongo(output)
    return jsonable_encoder(output)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    result = await process_csv(file)
    return result

@app.get("/dashboard-data")
async def dashboard_data():
    try:
        data = get_dashboard_data()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
