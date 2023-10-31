# Hostgator

The content of this directory is intended to be located at `public_html`, where it'll be composing the management of the website.

## Deployer Script

This Python script is designed to be run on a Linux server and is intended to be called from a cron job. It automates the process of downloading the latest release of a specified GitHub repository, extracting the contents, and keeping track of the version.

### Usage

The script takes three parameters:

1. A GitHub repository URL
2. A name for the folder where the release will be extracted
3. The name of the release asset file to be downloaded

Example usage:

```bash
python Deployer.py https://github.com/user/repo folder_name asset_name.zip
```

### Version Control

The script maintains a `.version` file, where it registers the current version of the downloaded release. The file contains a line for each repository in the format `{name}={version}`.

Before downloading a release, the script checks the `.version` file to see if the latest release is already downloaded. If the versions do not match, the script downloads and extracts the new release.

### Error Handling

The script provides terminal logs, which can be used by the cron job for email notifications. If there is an error during any of the steps, the script will terminate and log the reason for the error.

### Note

If the content of the zip file is a single folder, the script will extract the content of that folder to the named folder. After extraction, the downloaded zip file is deleted.
