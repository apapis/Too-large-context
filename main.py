import os
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI

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
        if 'test' in item and isinstance(item['test'], dict):
            if 'q' in item['test'] and 'a' in item['test']:
                ai_questions.append(item)
        else:
            math_questions.append(item)
    
    print(f"Found {len(math_questions)} math questions")
    print(f"Found {len(ai_questions)} AI questions")
    
    return math_questions, ai_questions

def validate_math(math_questions):
    corrected = []
    corrections = []
    
    for question in math_questions:
        expression = question['question']
        given_answer = question['answer']
        
        try:
            num1, num2 = map(int, expression.split('+'))
            correct_answer = num1 + num2
            
            if given_answer != correct_answer:
                corrections.append({
                    'expression': expression,
                    'old': given_answer,
                    'new': correct_answer
                })
                question['answer'] = correct_answer
            
            corrected.append(question)
                
        except (ValueError, TypeError) as e:
            corrected.append(question)
    
    return corrected, corrections

def process_ai_questions(ai_questions):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    for question in ai_questions:
        user_question = question['test']['q']
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Provide only short, direct answers without any additional explanation. One or two words if possible."},
                    {"role": "user", "content": user_question}
                ]
            )
            
            question['test']['a'] = response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error processing question: {user_question}")
            print(f"Error: {e}")
            
    return ai_questions

def print_corrections(corrections):
    if not corrections:
        print("\nAll math answers were correct!")
        return
        
    print(f"\nFound {len(corrections)} incorrect answers:")
    for c in corrections:
        print(f"{c['expression']}: {c['old']} -> {c['new']}")

def print_ai_results(ai_questions):
    print("\nAI Questions and Answers:")
    print("-" * 50)
    for q in ai_questions:
        print(f"Q: {q['test']['q']}")
        print(f"A: {q['test']['a']}")
        print("-" * 50)

if __name__ == "__main__":
    test_data = load_file()
    
    if test_data:
        math_questions, ai_questions = separate_questions(test_data)
        corrected_math, corrections = validate_math(math_questions)
        print_corrections(corrections)
        
        processed_ai = process_ai_questions(ai_questions)
        print_ai_results(processed_ai)