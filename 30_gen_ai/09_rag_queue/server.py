from dotenv import load_dotenv
load_dotenv() 

from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

# Create an instance of FastAPI application
app = FastAPI()

# Root endpoint to check if the server is running
@app.get("/")
def root():
    # Returns a simple response confirming server status
    return {"message": "Server is up and running"}

# POST endpoint to handle incoming user chat queries
@app.post("/chat")
def chat(
    # 'query' is a required query parameter sent by the user
    # Query(...) means it is mandatory
    # description is used for API documentation (Swagger UI)
    query: str = Query(..., description="The chat query of user")
):
    # Enqueue the process_query function with 'query' as argument
    # NOTE: This does NOT execute the function immediately 
    # It only schedules the job in the queue (Redis)
    # A background worker will later pick this job and run:
    # process_query(query)
    # This prevents blocking the API while heavy RAG processing runs
    job = queue.enqueue(process_query, query)

    # Return immediate response with job status and job ID
    # Client can use this job_id to fetch result later from /result endpoint
    return {"status": "queued", "job_id": job.id}



# GET endpoint to check the status/result of a queued job
@app.get("/job-status")
def job_result(
    # 'job_id' is required and used to identify the background job
    job_id: str = Query(..., description="Job ID to fetch result")
):
    # Fetch the job from the queue using its ID
    job = queue.fetch_job(job_id=job_id)

    # Get the result returned by the background worker (process_query)
    # NOTE: If the job is not completed yet, this may return None
    result = job.return_value()

    # Return the result to the client
    return {"result": result}