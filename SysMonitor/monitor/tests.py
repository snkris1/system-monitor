from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Device

User = get_user_model()

class DeviceModelTests(TestCase):
    """
    Test suite for the Device model.
    """

    def setUp(self):
        """
        Set up a test user for use in all test methods.
        """
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_create_device_and_assign_to_user(self):
        """
        Test that a Device can be created and correctly associated with a User.
        """
        # Create a new device and associate it with the user
        device = Device.objects.create(
            name='Test Workstation',
            user=self.user
        )

        # Assert that the device's user is the one we created
        self.assertEqual(device.user, self.user)
        self.assertEqual(device.name, 'Test Workstation')

        # Assert that the device appears in the user's related devices set
        self.assertIn(device, self.user.devices.all())
        self.assertEqual(self.user.devices.count(), 1)

    def test_device_str_representation(self):
        """
        Test the __str__ method of the Device model.
        """
        device = Device.objects.create(
            name='Laptop',
            user=self.user
        )
        self.assertEqual(str(device), 'Laptop')
