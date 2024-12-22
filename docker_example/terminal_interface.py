import requests
import json
import os

def main():
    job_tokens = []

    print("Welcome to the server communication interface!")
    
    # Prompt for server address
    server_address = input("Enter the server address (e.g., http://127.0.0.1:42709): ").strip()

    while True:
        print("\nWhat would you like to do?")
        print("1. POST - Make a prediction (/api/classifier/analyze)")
        print("2. GET - Check status of a job (/api/classifier/analyze_status/<id_>)")
        print("3. GET - Get result of a job (/api/classifier/get_result/<id_>)")
        print("4. Get list of all submitted jobs during current session")
        print("5. Get number of all submitted jobs stored in the database")
        print("6. Clear screen")
        print("7. Exit")
        
        try:
            choice = int(input("Enter the number corresponding to your choice: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            continue

        if choice == 1:
            # POST request
            print("Enter the following features for the prediction as float values:")
            try:
                sepal_length = float(input("Sepal length: "))
                sepal_width = float(input("Sepal width: "))
                petal_length = float(input("Petal length: "))
                petal_width = float(input("Petal width: "))
            except ValueError:
                print("Invalid input. Please enter numeric values for the features.")
                continue
            
            data = {
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            }
            
            try:
                response = requests.post(f"{server_address}/api/classifier/analyze", json=data)
                if response.status_code in [200, 202]:
                    job_id = response.json().get("ok")
                    job_tokens.append(job_id)
                    print(f"Prediction request submitted successfully. Job ID: {job_id}")
                else:
                    print(f"Error: {response.status_code}, {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to the server: {e}")
            print('-' * 90)

        elif choice == 2:
            # GET status request
            job_id = input("Enter the job ID to check the status: ").strip()
            try:
                response = requests.get(f"{server_address}/api/classifier/analyze_status/{job_id}")
                if response.status_code in [200, 202]:
                    print(f"Job status: {response.json().get('status')}")
                else:
                    print(f"Error: {response.status_code}, {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to the server: {e}")
            print('-' * 90)

        elif choice == 3:
            # GET result request
            job_id = input("Enter the job ID to get the result: ").strip()
            try:
                response = requests.get(f"{server_address}/api/classifier/get_result/{job_id}")
                if response.status_code in [200, 202]:
                    print(f"Prediction result: {response.json().get('result')}")
                else:
                    print(f"Error: {response.status_code}, {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to the server: {e}")
            print('-' * 50)

        elif choice == 4:
            print()
            for i, job_token in enumerate(job_tokens):
                print(f'{i}:   {job_token}')
            print('-' * 90)
            print()

        elif  choice == 5:
            response = requests.get(f"{server_address}/api/classifier/all_jobs")
            print(f'Number of elements in Redis database: {len(response.json().get("jobs"))}')

        elif choice == 6:
            os.system('cls' if os.name == 'nt' else 'clear')

        elif choice == 7:
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()