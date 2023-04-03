from rest_framework.test import APITestCase


class TestAmenities(APITestCase):

    def test_all_amenities(self):

        response = self.client.get("/api/v1/rooms/amenities/")
        data =response.json()

        self.assertEqual(response.status_code, 201, "Status code isn`t 200.")
