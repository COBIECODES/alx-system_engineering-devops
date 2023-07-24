import requests
import sys

def is_valid_employee_id(employee_id):
    try:
        int(employee_id)
        return True
    except ValueError:
        return False

def get_employee_todo_list_progress(employee_id):
    base_url = 'https://jsonplaceholder.typicode.com'
    employee_url = f'{base_url}/users/{employee_id}'
    todos_url = f'{base_url}/todos?userId={employee_id}'

    try:
        # Fetch employee data
        employee_response = requests.get(employee_url)
        employee_data = employee_response.json()
        username = employee_data.get('username')

        # Fetch todos data
        todos_response = requests.get(todos_url)
        tasks = todos_response.json()

        with open(f'{employee_id}.csv', 'w') as file:
            file.write('"USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"\n')
            for task in tasks:
                file.write(f'"{employee_id}","{username}","{task.get("completed")}","{task.get("title")}"\n')

        print(f'TODO list progress for Employee {username} has been exported to {employee_id}.csv')

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Invalid JSON response from the API.")
    except KeyError:
        print("Error: Invalid data in the JSON response.")

if __name__ == '__main__':
    if len(sys.argv) != 2 or not is_valid_employee_id(sys.argv[1]):
        print("Usage: python script.py EMPLOYEE_ID (where EMPLOYEE_ID is an integer)")
    else:
        employee_id = int(sys.argv[1])
        get_employee_todo_list_progress(employee_id)

