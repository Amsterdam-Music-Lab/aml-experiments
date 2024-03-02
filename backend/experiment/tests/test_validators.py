from django.core.exceptions import ValidationError
from django.test import TestCase

from experiment.validators import experiment_slug_validator, consent_file_validator


class ExperimentValidatorsTest(TestCase):
    def test_valid_slug(self):
        # Test a valid lowercase slug
        slug = 'testslug'
        try:
            experiment_slug_validator(slug)
        except ValidationError:
            self.fail(f"Unexpected ValidationError raised for slug: {slug}")

    def test_disallowed_slug(self):
        # Test a disallowed slug
        slug = 'admin'
        with self.assertRaises(ValidationError) as cm:
            experiment_slug_validator(slug)
        self.assertEqual(str(cm.exception.messages[0]), 'The slug "admin" is not allowed.')

    def test_uppercase_slug(self):
        # Test an uppercase slug
        slug = 'TestSlug'
        with self.assertRaises(ValidationError) as cm:
            experiment_slug_validator(slug)
        self.assertEqual(str(cm.exception.messages[0]), 'Slugs must be lowercase.')
