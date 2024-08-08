import os
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Download an AI model'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to download')
        parser.add_argument('model_url', type=str, help='URL of the model file to download')

    def handle(self, *args, **options):
        model_name = options['model_name']
        model_url = options['model_url']

        ai_models_path = getattr(settings, 'AI_MODELS_PATH', None)
        if ai_models_path is None:
            ai_models_path = os.path.join(settings.BASE_DIR, "ai_models")
            self.stdout.write(self.style.WARNING("AI_MODELS_PATH not set in settings file"))
            self.stdout.write(f"Setting AI_MODELS_PATH to default value: {ai_models_path}")

        if not os.path.exists(ai_models_path):
            os.makedirs(ai_models_path)

        model_path = os.path.join(ai_models_path, model_name)
        if os.path.exists(model_path):
            self.stdout.write(self.style.WARNING(f"Model {model_name} already exists. Skipping download."))
            return

        self.stdout.write(f"Downloading model {model_name} from {model_url}")

        response = requests.get(model_url, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))

        with open(model_path, "wb") as file, tqdm(
                desc=model_name,
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)

        self.stdout.write(self.style.SUCCESS(f"Model {model_name} downloaded successfully."))
