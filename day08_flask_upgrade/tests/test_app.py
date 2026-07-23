import unittest

from app import app


class FlaskUpgradeTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret-key")
        self.client = app.test_client()

    def login(self):
        return self.client.post(
            "/login",
            data={"username": "student", "password": "day07"},
        )

    def test_health_does_not_require_login(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"ok": True, "service": "day08-flask-upgrade"},
        )

    def test_metrics_returns_four_serializable_cards(self):
        self.login()
        response = self.client.get("/api/metrics")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(len(payload["metrics"]), 4)
        self.assertEqual(
            set(payload["metrics"][0]),
            {"label", "value", "note"},
        )

    def test_categories_filters_fashion(self):
        self.login()
        response = self.client.get("/api/categories?category=Fashion")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["category"], "Fashion")
        self.assertEqual(len(payload["rows"]), 1)
        self.assertEqual(payload["rows"][0]["偏好品类"], "Fashion")

    def test_categories_defaults_to_all_rows(self):
        self.login()
        response = self.client.get("/api/categories")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["category"], "全部")
        self.assertEqual(len(payload["rows"]), 5)

    def test_unknown_category_returns_unified_400_json(self):
        self.login()
        response = self.client.get("/api/categories?category=Unknown")
        payload = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(payload["ok"])
        self.assertIn("error", payload)

    def test_empty_question_returns_unified_400_json(self):
        self.login()
        response = self.client.post("/api/ask", json={"question": "   "})
        payload = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            payload,
            {"ok": False, "error": "请输入一个与项目数据有关的问题。"},
        )

    def test_api_requires_login(self):
        response = self.client.get("/api/metrics")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
