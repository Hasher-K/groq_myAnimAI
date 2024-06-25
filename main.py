import os
import requests
from groq import Groq

MAL_API_URL = "https://api.myanimelist.net/v2"
CLIENT_ID = os.environ.get("MAL_CLIENT_ID")

def fetch_anime_info(anime_name):
    url = f"{MAL_API_URL}/anime?q={anime_name}&limit=1&fields=title,synopsis,mean,genres"
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from MyAnimeList API. Status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return None

def main():
    # Initialize Groq client
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Get user input for anime search
    anime_name = input("Enter the name of the anime you want to know about: ")

    # Fetch anime information
    anime_info = fetch_anime_info(anime_name)
    if anime_info and anime_info.get('data'):
        anime_data = anime_info['data'][0]['node']
        title = anime_data['title']
        synopsis = anime_data['synopsis']
        mean_score = anime_data.get('mean', 'N/A')
        genres = ', '.join([genre['name'] for genre in anime_data.get('genres', [])])

        # Format response for Groq chat completion
        summary = f"Title: {title}\nMean Score: {mean_score}\nGenres: {genres}\nSynopsis: {synopsis}..."  
    else:
        summary = "Sorry, I couldn't find any information on that anime."

    # User Question
    question = input("What do you want to know about this anime? ")

    # Log the messages being sent to Groq
    messages = [
        {
            "role": "user",
            "content": f"{anime_name}: {question}?",
        },
        {
            "role": "assistant",
            "content": summary,
        }
    ]
    print("Messages sent to Groq:", messages)

    # Groq chat completion
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    # Print the response from Groq chat completion
    print("Groq Response:", chat_completion.choices[0].message.content)

if __name__ == "__main__":
    main()
