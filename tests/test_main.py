import requests

api_url = "http://localhost:8001"


def test_healthcheck():
    response = requests.get(f"{api_url}/__health")
    assert response.status_code == 200


class TestLaptops:
    def test_get_empty_laptops(self):
        response = requests.get(f"{api_url}/v1/laptops")
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_laptops(self):
        body = {'model': "Model", "developer": "Developer"}
        response = requests.post(f"{api_url}/v1/laptops", json=body)
        assert response.status_code == 200
        assert response.json().get('model') == 'Model'
        assert response.json().get('developer') == 'Developer'
        assert response.json().get('id') == 0

    def test_get_laptops_by_id(self):
        response = requests.get(f"{api_url}/v1/laptops/0")
        assert response.status_code == 200
        assert response.json().get('model') == 'Model'
        assert response.json().get('developer') == 'Developer'
        assert response.json().get('id') == 0

    def test_get_not_empty_laptops(self):
        response = requests.get(f"{api_url}/v1/laptops")
        assert response.status_code == 200
        assert len(response.json()) == 1