import aiohttp

class MiAPIRGB:
    """Cliente para la API de Mi API RGB."""

    def __init__(self, host, port, username, password):
        """Inicializa la conexión a la API."""
        self._base_url = f"http://{host}:{port}/effect/apply"
        self._auth_params = {"username": username, "password": password}

    async def apply_effect(self, effect_name, properties=None):
        """Envía una solicitud para aplicar un efecto RGB."""
        async with aiohttp.ClientSession() as session:
            params = {"effect": effect_name, **self._auth_params}
            if properties:
                params.update(properties)
            async with session.get(self._base_url, params=params) as response:
                return response.status == 200
