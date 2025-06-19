import json
import argparse
import csv
import jmespath
import aiohttp
import asyncio
from urllib.parse import urljoin
from typing import Any, List, Dict, Union, TypeAlias

JSONType: TypeAlias = Union[dict[str, 'JSONType'], list['JSONType'], str, int, float, bool, None]

env_to_extension: Dict[str, str] = {"commercial": "com", "government": "us"}

async def http_get_json(url: str, access_token: str) -> JSONType:
    headers: dict[str, str] = {
        "Authorization": f"Bearer {access_token}"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            # Raise an exception if a 200 response is not recieved.
            if resp.status != 200:
                body: str = await resp.text()
                raise Exception(f"Request to {url} failed with status {resp.status}:\n{body}")

            # Then ensure the content type of the response is JSON.
            content_type: str = resp.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                body: str = await resp.text()
                raise Exception(f"Unexpected content type: {content_type}\nBody:\n{body}")

            return await resp.json()


def save_array_to_csv(arr: List[str], filename: str) -> None:
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        for elem in arr:
            writer.writerow([elem])

env_choices = ["commercial", "comm", "c", "government", "gov", "g"]
def normalize_env(env: str) -> str:
    # This function is only called after it is ensured that env is in env_choices. 
    if "c" in env:
        return "commercial"
    else: # in this case env.contains("g") is true
        return "government"

async def main() -> None:
    # Parse arguments from the command line.
    parser = argparse.ArgumentParser(description="Saves all template IDs in the account to a .csv.")
    parser.add_argument("--access_token", help="A Bearer access token, without the \"Bearer \".", required=True)
    parser.add_argument("--environment", "--env", choices=env_choices,help=f"Must be one of {",".join(env_choices)}", required=True)
    args: argparse.Namespace = parser.parse_args()
    env = normalize_env(args.environment)
    ext = env_to_extension[env]

    # Get the base URL for the Adobe Sign API. We have to ask the API what this URL is since it varies across Sign instances.
    baseUrl: str = f"https://api.na1.adobesign.{ext}/api/rest/v6"
    baseUrl = (await http_get_json(f"{baseUrl}/baseUris", args.access_token))["apiAccessPoint"]
    baseUrl = urljoin(baseUrl, "/api/rest/v6")

    # Send a GET request to /libraryDocuments to get a JSON array of all of the library documents, i.e. templates.
    resp = await http_get_json(f"{baseUrl}/libraryDocuments", args.access_token)
    template_ids = jmespath.search("libraryDocumentList[*].id", resp)
    save_array_to_csv(template_ids, "./template_ids.csv")
    print("The template IDs have been saved to ./template_ids.csv.")
 
if __name__ == "__main__":
    asyncio.run(main())
