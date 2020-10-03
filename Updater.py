meta = {
    "proj": "Updater",
    "proj_id": "5",
    "ver": "2.0.0"
}


def update():
    # -==========[ Update code ]==========-
    # Updater: Used to check for new releases on GitHub
    # github.com/smcclennon/Updater
    updater = {
        "updater_ver": "2.0.0",
        "proj": meta["proj"],
        "proj_id": meta["proj_id"],
        "current_ver": meta["ver"]
    }

    import os  # detecting OS type (nt, posix, java), clearing console window, restart the script
    from distutils.version import LooseVersion as semver  # as semver for readability
    import urllib.request, json  # load and parse the GitHub API
    import platform  # Consistantly detect MacOS
    import traceback  # Printing errors

    # Disable SSL certificate verification for MacOS (very bad practice, I know)
    # https://stackoverflow.com/a/55320961
    if platform.system() == 'Darwin':  # If MacOS
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

    print('Checking for updates...', end='\r')
    for i in range(3):  # Try to retry the update up to 3 times if an error occurs
        try:
            with urllib.request.urlopen("https://smcclennon.github.io/api/v2/update.json") as update_api:  # internal api
                update_api = json.loads(update_api.read().decode())
                #{'name': 'X', 'github_api': {'latest_release': {'info': 'https://api.github.com/repos/smcclennon/X/releases/latest', 'release_download': 'https://github.com/smcclennon/X/releases/latest/download/X.py'}, 'all_releases': {'info': 'https://api.github.com/repos/smcclennon/X/releases'}}}


                updater["proj"] = update_api["project"][updater["proj_id"]]["name"]  # Project name
            #with urllib.request.urlopen(update_api["project"][updater["proj_id"]]["github_api"]["latest_release"]["info"]) as github_api_latest:  # Latest release details
            #    latest_info = json.loads(github_api_latest.read().decode())['tag_name'].replace('v', '')  # remove 'v' from version number (v1.2.3 -> 1.2.3)

            github_releases = json.loads(urllib.request.urlopen(update_api["project"][updater["proj_id"]]["github_api"]["all_releases"]["info"]).read().decode())  # Get latest patch notes

            break
        except Exception as e:  # If updating fails 3 times
            github_releases = {0: {'tag_name': 'v0.0.0'}}
            if str(e) == "HTTP Error 404: Not Found":  # No releases found
                break
            elif str(e) == '<urlopen error [Errno 11001] getaddrinfo failed>':  # Cannot connect to website
                break
            else:
                print('Error encountered whilst checking for updates. Full traceback below...')
                traceback.print_exc()

    if semver(github_releases[0]['tag_name'].replace('v', '')) > semver(updater["current_ver"]):
        print('Update available!      ')
        print(f'Latest Version: {github_releases[0]["tag_name"]}\n')

        changelog = []
        for release in github_releases:
            try:
                if semver(release['tag_name'].replace('v', '')) > semver(updater["current_ver"]):
                    changelog.append([release["tag_name"], release["body"]])
                else:
                    break  # Stop parsing patch notes after the current version has been met
            except:  # Incorrect version format + semver causes errors (Example: semver('Build-1'))
                traceback.print_exc()
                pass  # Skip/do nothing

        for release in changelog[::-1]:  # Step backwards, print latest patch notes last
            print(f'{release[0]}:\n{release[1]}\n')

        confirm = input(str('Update now? [Y/n] ')).upper()
        if confirm != 'N':
            print(f'Downloading new file...')
            urllib.request.urlretrieve(update_api["project"][updater["proj_id"]]["github_api"]["latest_release"]["release_download"], os.path.basename(__file__)+'.update_tmp')  # download the latest version to cwd

            os.rename(os.path.basename(__file__), os.path.basename(__file__)+'.old')
            os.rename(os.path.basename(__file__)+'.update_tmp', os.path.basename(__file__))
            os.remove(os.path.basename(__file__)+'.old')
            os.system('cls||clear')  # Clear console window
            os.system('"'+os.path.basename(__file__)+'" 1')
            quit()
    # -==========[ Update code ]==========-


while True:
    update()
    print(f'{meta["proj"]} v{meta["ver"]}             ')
    print('\nThis script serves no purpose other than to update itself.')
    print('The code contained within this script is used to update many of my projects')


    print('\nYou can demo the updater functionality by typing in a version value and attempting to check for updates')
    print('This script may fail to update if it is already the latest version for these reasons:')
    print('    - The update code deletes the old version/file, however if the old file has the same filename as the newest version, it will not be deleted')
    print('    - To solve this, try renaming this python file to something else')

    print('\n\nEnter your desired current-version-number to proceed with updating (leave blank for current version)')
    print('If your version number doesn\'t conform to Semver (1.2.3), the update may fail and the script will most likely crash')
    userVer = str(input('\nver = '))
    if userVer != '': meta["ver"] = userVer