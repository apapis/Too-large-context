import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def load_file():
    app_url = os.getenv('APP_URL')
    
    if not app_url:
        print("Error: APP_URL not found in .env file")
        return None
    
    url = f"{app_url}"
    
    try:
        print("Downloading file...")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        test_data = data.get('test-data')
        
        if test_data is None:
            print("Error: 'test-data' section not found in file")
            return None
            
        print("Test data successfully extracted")
        return test_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error while downloading file: {e}")
        return None
        
    except json.JSONDecodeError as e:
        print(f"Error while parsing JSON: {e}")
        return None

def separate_questions(test_data):
    math_questions = []
    ai_questions = []
    
    for item in test_data:
        # Check if item has 'test' field with 'q' and 'a'
        if 'test' in item and isinstance(item['test'], dict):
            if 'q' in item['test'] and 'a' in item['test']:
                # This is an AI question
                ai_questions.append(item)
        else:
            # This is a math question
            math_questions.append(item)
    
    print(f"Found {len(math_questions)} math questions")
    print(f"Found {len(ai_questions)} AI questions")
    
    return math_questions, ai_questions

def display_sample_questions(math_questions, ai_questions, sample_size=3):
    """
    Displays sample of both types of questions
    """
    print("\nSample Math Questions:")
    for q in math_questions[:sample_size]:
        print(json.dumps(q, indent=2))
    
    print("\nSample AI Questions:")
    for q in ai_questions[:sample_size]:
        print(json.dumps(q, indent=2))

if __name__ == "__main__":
    test_data = load_file()
    
    if test_data:
        math_questions, ai_questions = separate_questions(test_data)
        
        display_sample_questions(math_questions, ai_questions)