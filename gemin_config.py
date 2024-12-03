import google.generativeai as genai

# Configure the API key to allow access to the model
genai.configure(api_key="Enter you API-KEY")
model = genai.GenerativeModel("gemini-pro")


def send_request(query):
    try:
        # Send the request to the model and get the response
        response = model.generate_content(query)
        # It's good practice to log or print the response for debugging purposes
        print(f"AI Response: {response.text}")
        return response.text  # Return just the text part of the response
    except Exception as e:
        print(f"Error during AI request: {e}")
        return "Sorry, I couldn't get a response from the AI."


if __name__ == "__main__":
    sentence = input("What do you want: ")
    reply = send_request(sentence)
    print(f"Reply from AI: {reply}")
