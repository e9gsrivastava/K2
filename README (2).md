

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/e9gsrivastava/k2.git
    cd k2
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser (for admin access):

    ```bash
    python manage.py createsuperuser
    ```

7. Run below command to generate random data:

    ```bash
    python manage.py utils
    ```

8. Run the development server:

    ```bash
    python manage.py runserver
    ```

   Your project should now be accessible at http://127.0.0.1:8000/.
