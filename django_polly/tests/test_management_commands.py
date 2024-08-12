import os
import pytest
from django.core.management import call_command
from django.conf import settings
from unittest.mock import patch


@pytest.mark.django_db
class TestDownloadModelCommand:
    @patch('django_polly.management.commands.download_model.requests.get')
    def test_download_model_command(self, mock_get):
        # Mock the response
        mock_get.return_value.status_code = 200
        mock_get.return_value.iter_content.return_value = [b'mock_content']

        model_name = "test_model.gguf"
        model_url = "https://example.com/test_model.gguf"

        # Call the command
        call_command('download_model', model_name, model_url)

        # Check if the file was "downloaded"
        expected_path = os.path.join(settings.AI_MODELS_PATH, model_name)
        assert os.path.exists(expected_path)

        # Clean up
        os.remove(expected_path)

    @patch('django_polly.management.commands.download_model.requests.get')
    def test_download_model_command_file_exists(self, mock_get):
        model_name = "existing_model.gguf"
        model_path = os.path.join(settings.AI_MODELS_PATH, model_name)

        # Create an empty file
        open(model_path, 'a').close()

        # Call the command
        call_command('download_model', model_name, "https://example.com/existing_model.gguf")

        # Check that the mock was not called (file should not be downloaded)
        mock_get.assert_not_called()

        # Clean up
        os.remove(model_path)
