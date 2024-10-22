from dataclasses import dataclass
import datetime

import requests
from dateutil.parser import isoparse

from npmview.exceptions import Npm404Exception

@dataclass
class NpmData:
    name: str
    description: str
    modified: datetime.datetime
    created: datetime.datetime
    latest: str
    author_name: str
    author_email: str
    license: str

    @classmethod
    def _from_registry_response(cls, data):
        name = data.get("name", "")
        description = data.get("description", "")
        modified = isoparse(data.get("time", {}).get("modified", ""))
        created = isoparse(data.get("time", {}).get("created", ""))
        latest = data.get("dist-tags", {}).get("latest")
        author = data.get("author", {})
        author_email = author.get("email")
        author_name = author.get("name")
        _license = data.get("license")

        return cls(name, description, modified, created,
                   latest, author_name, author_email, _license)

    def pretty_print(self):
        return f'{self}'


class NpmView(object):
    REGISTRY_URL = 'https://registry.npmjs.org/'

    def __init__(self) -> None:
        pass


    def _resolve_package_query_url(self, package_name: str) -> str:
        return ''.join([self.REGISTRY_URL, package_name])


    def _make_request(self, url: str):
        # NOTE: do we need a session ? extra provision for retrying and return exception
        response = requests.get(url, timeout=60)
        if response.status_code == 404: raise Npm404Exception
        return response


    def request_metadata(self, package_name: str) -> NpmData:
        resolve_url = self._resolve_package_query_url(package_name)
        response = self._make_request(resolve_url)
        response_json = response.json()
        return NpmData._from_registry_response(response_json)

