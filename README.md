## Order processing scheduling system built with FastAPI

This project utilizes
- Queues for processing orders safely
- Field validation with pydantic models
- Stack feature for reverting previous orders

## Running

### Auto

- Just build the docker image and run a container exposing the 8000 port
`docker build -t <image-name> .`
`docker run -p 8000:8000 <image-name>`

### Manually

1. Clone the project
2. run `python -m venv venv`
3. based on your operating system run
Windows -> `./venv/Scripts/activate`
Linux/Mac -> `source ./venv/bin/activate`
4. run the dev server `uvicorn app:app --reload`
