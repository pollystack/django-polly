## Running the Example

To run the example project:

1. Navigate to the example directory: `cd example`
2. Install the requirements: `pip install -r requirements.txt`
3. Download a model
    ```
    python manage.py download_model "Qwen2-500M-Instruct-Q8_0.gguf" "https://huggingface.co/lmstudio-community/Qwen2-500M-Instruct-GGUF/resolve/main/Qwen2-500M-Instruct-Q8_0.gguf" 
    ```
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`
7. Visit `http://127.0.0.1:8000/admin/` to add some parrots
8. Visit `http://127.0.0.1:8000/` to see the example home page