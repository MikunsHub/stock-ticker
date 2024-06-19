from typing import Any, Dict, Optional

from requests import RequestException, Session

from env import EODHD_API_TOKEN, EODHD_BASE_URL
from interfaces.constants import GET, EODHDResources


class EODHDAPIClientError(Exception):
	pass


class EODHDAPIClient:
	def __init__(self) -> None:
		self.session = Session()
		self.api_token = EODHD_API_TOKEN
		self.base_url = EODHD_BASE_URL

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.session.close()

	def _request(
		self,
		method: str,
		url: str,
		params: Optional[Dict[str, Any]] = None,
		headers: Optional[Dict[str, str]] = None,
		json_body: Optional[Dict[str, Any]] = None,
		ssl: bool = True,
	) -> Dict[str, Any]:
		try:
			response = self.session.request(
				method=method, url=url, params=params, headers=headers, json=json_body, verify=ssl
			)
			response.raise_for_status()
			return response.json()
		except RequestException as e:
			error_message = f'EODHDAPIClientError: Failed to make the API request to {url}.'
			raise EODHDAPIClientError(error_message) from e

	def get(
		self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
	) -> Dict[str, Any]:
		return self._request(method=GET, url=url, params=params, headers=headers)

	def fetch_data(self, resource: EODHDResources, **kwargs) -> Dict[str, Any]:
		# Extract the template and default parameters from the resource
		template, default_params = resource.value

		# Prepare the parameters, starting with defaults from the resource
		params = {key: value for key, value in default_params}
		params.update(kwargs)
		params['api_token'] = self.api_token
		params['base_url'] = self.base_url

		# Generate the URL
		url = template.substitute(params)
		return self.get(url)
