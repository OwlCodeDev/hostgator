import os
import sys
import requests
import zipfile
import shutil

GITHUB_API = "https://api.github.com"

def get_latest_release(user, repo):
    response = requests.get(f"{GITHUB_API}/repos/{user}/{repo}/releases/latest")
    response.raise_for_status()
    return response.json()

def download_and_extract_release_asset(release, name, asset_name):
    asset = next((a for a in release['assets'] if a['name'] == asset_name), None)
    if asset is None:
        print(f"Asset {asset_name} not found in the latest release")
        sys.exit(1)

    url = asset['browser_download_url']
    response = requests.get(url, stream=True)
    response.raise_for_status()

    zip_path = f"{name}.zip"
    with open(zip_path, 'wb') as out_file:
        out_file.write(response.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(name)

    os.remove(zip_path)

    # If the content of the zip file is a single folder, move its content to the named folder
    extracted_path = os.path.join(name, os.listdir(name)[0])
    if os.path.isdir(extracted_path) and len(os.listdir(name)) == 1:
        for file_name in os.listdir(extracted_path):
            shutil.move(os.path.join(extracted_path, file_name), name)
        os.rmdir(extracted_path)

def read_version_file():
    if not os.path.exists('.version'):
        return {}
    with open('.version', 'r') as f:
        lines = f.read().splitlines()
    return dict(line.split('=') for line in lines)

def write_version_file(versions):
    with open('.version', 'w') as f:
        for name, version in versions.items():
            f.write(f"{name}={version}\n")

def main():
    if len(sys.argv) != 4:
        print("Usage: python Deployer.py <github_repo_url> <name> <asset_name>")
        sys.exit(1)

    github_repo_url = sys.argv[1]
    name = sys.argv[2]
    asset_name = sys.argv[3]

    user, repo = github_repo_url.split('/')[-2:]

    versions = read_version_file()

    try:
        release = get_latest_release(user, repo)
    except requests.HTTPError as err:
        print(f"Failed to get the latest release: {err}")
        sys.exit(1)

    if versions.get(name) == release['tag_name']:
        print(f"Latest version {release['tag_name']} is already downloaded for {name}")
        return

    try:
        download_and_extract_release_asset(release, name, asset_name)
    except Exception as err:
        print(f"Failed to download and extract the release asset: {err}")
        sys.exit(1)

    versions[name] = release['tag_name']
    write_version_file(versions)

    print(f"Successfully downloaded and extracted {release['tag_name']} to {name}")

if __name__ == "__main__":
    main()
