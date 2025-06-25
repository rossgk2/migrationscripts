import csv
import requests
import sys

def getDefaultHeadersConfig(bearerToken: str):
  return {'Authorization': f'Bearer {bearerToken}'}

'''
Retrieves the base URI that is the first part of all Adobe Sign API endpoints.
'''
def getBaseUri(bearerToken: str):
  response = requests.get('https://api.na1.adobesign.com:443/api/rest/v6/baseUris', headers=getDefaultHeadersConfig(bearerToken))
  baseUri = response.json()['apiAccessPoint']
  baseUri = baseUri[0:len(baseUri) - 1] + '/api/rest/v6'
  return baseUri

def getAgreementsFromWebform(bearerToken: str, webformId: str):
  baseUri = getBaseUri(bearerToken)
  defaultHeadersConfig = getDefaultHeadersConfig(bearerToken)

  pageSize = 100; pageLimit = 10
  agreements = []
  response = None
  cursorQueryString = ''
  i = 1; done = False
  while (not done):
    # Add all the agreements from the next page to the array.
    url = f'{baseUri}/widgets/{webformId}/agreements?pageSize={pageSize}' + cursorQueryString
    response = requests.get(url, headers=defaultHeadersConfig).json()
    agreements.extend(response['userAgreementList'])
    
    # If there are more pages, update the cursor query string. Otherwise, we are done.
    if len(response['page']) != 0 and 'nextCursor' in response['page']:
      cursorQueryString = f'&cursor={cursor}'
      done = pageLimit >= 0 and i >= pageLimit
    else:
      done = True

    print(f'Loaded page {i} of agreements.')
    i += 1

  return agreements

def main():
  bearerToken = sys.argv[1]
  baseUri = getBaseUri(bearerToken)
  defaultHeadersConfig = getDefaultHeadersConfig(bearerToken)

  testWebformId = 'CBJCHBCAABAAsu1PvN84aZXyj9Vwk5y5095nNlyEDh9z'
  webformId = sys.argv[2]

  # Get all agreement IDs associated with the webform.
  agreements = getAgreementsFromWebform(bearerToken, webformId)
  agreementIds = [a['id'] for a in agreements if a['parentId'] == webformId]

  # Get the emails of the senders associated with each agreement ID.
  def getEmailFromAgreement(agreementId: str):
    response = requests.get(f'{baseUri}/agreements/{agreementId}', headers=defaultHeadersConfig)
    return response.json()['senderEmail']
  emails = [getEmailFromAgreement(id) for id in agreementIds]
  
  # Write the emails and agreement IDs to a csv file in the format required by the bulk download tool.
  csvZip = zip(emails, agreementIds, agreementIds)
  with open('ags.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(['sender', 'agr_id', 'secure_id']) # headers
    for row in csvZip:
        writer.writerow(row)

main()