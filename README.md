### coe379L-project3 - easier to read in Code format

The API has two endpoints: /summary for information about the API and /inference for taking in an image file and returning the prediction (“damage” or “no damage”).
For deploying using Docker, first clone the repository. Next, build and start the container using “docker-compose up –build.” The API should be available at http://localhost:5000. To stop the container, run “docker-compose down.”

Example requests: 

/summary: uses GET and returns the API version, name, description, and number of parameters for the model 
curl request: curl http://localhost:5000/summary

json response: 
{
  "version": "v1",
  "name": "damage",
  "description": " ----- Categorize damage from hurricanes ------",
  "number_of_parameters": 1234567
}

/inference: uses POST to accept an image file as input and return the prediction (“damage” or “no damage”)
curl request: curl -X POST http://localhost:5000/inference \ -F "image=@path_to_your_image.jpg"
json response with success: 
{
    “prediction”: “damage”
		}
json response with error: 
{
  "error": "Invalid request; pass a binary image file as a multi-part form under the image key."
}
