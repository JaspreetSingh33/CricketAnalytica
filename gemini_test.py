from google import genai

client = genai.Client()

response = client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain in one sentence why cricket statistics are useful for comparing two players."
)

print(response.output_text)