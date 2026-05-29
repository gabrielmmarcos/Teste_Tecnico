from http import HTTPStatus


# teste para verificar se a menssagem de boas vindas esta correta
def test_read_root_should_return_welcome_message(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Teste técnico Mundo Invest!"}
