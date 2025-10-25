from google import genai

client = genai.Client(api_key="AIzaSyBcI3rMgFb2ShRbCKiS2ypcPeF6jbYoiXs")

response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents="How does AI work?"
)
print(response. Text)
