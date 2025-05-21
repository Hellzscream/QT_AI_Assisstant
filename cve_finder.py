import re
import requests

def extract_cve_ids(text):
    pattern = r'CVE-\d{4}-\d{4,7}'
    return re.findall(pattern, text)

def fetch_cve_details(cve_id, api_key):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    headers = {
        "apiKey": api_key
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        cve_info = data['vulnerabilities'][0]['cve']

        description = cve_info['descriptions'][0]['value']

        # Extract reference URLs
        references = cve_info.get('references', [])
        links = []
        for ref in references:
            if 'url' in ref:
                links.append(ref['url'])

        return description, links
    except Exception as e:
        print(f"Error fetching details for {cve_id}: {e}")
        return "Description not available.", []
