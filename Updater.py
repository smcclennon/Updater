proj = 'Updater'
ver = '1.0.0'

while True:

    # Updater: Used to check for new releases on GitHub
    # github.com/smcclennon/Updater
    import os  # detecting OS type (nt, posix, java), clearing console window,
    import sys  # flush stdout before restarting the script
    from distutils.version import LooseVersion as semver  # as semver for readability
    if os.name == 'nt':
        Windows = True
    else:
        Windows = False
    import urllib.request, json  # load and parse the GitHub API
    if Windows:
        import ctypes  # set Windows console window title
        ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==   Checking for updates...')

    updateAttempt = 0  # Keep track of failed attempts
    print('Checking for updates...', end='\r')
    while updateAttempt < 3:  # Try to retry the update up to 3 times if an error occurs
        updateAttempt = updateAttempt+1
        try:
            with urllib.request.urlopen("https://smcclennon.github.io/update/api/5") as internalAPI:
                repo = []
                for line in internalAPI.readlines():
                    repo.append(line.decode().strip())
                apiLatest = repo[0]  # Latest release details
                proj = repo[1]  # Project name
                ddl = repo[2]  # Direct download link
                apiReleases = repo[3]  # List of patch notes
            with urllib.request.urlopen(apiLatest) as githubAPILatest:
                data = json.loads(githubAPILatest.read().decode())
                latest = data['tag_name'][1:]  # remove 'v' from version number (v1.2.3 -> 1.2.3)
            del data  # Prevent overlapping variable data
            release = json.loads(urllib.request.urlopen(  # Get latest patch notes
                apiReleases).read().decode())
            releases = [  # Store latest patch notes in a list
                (data['tag_name'], data['body'])
                for data in release
                if semver(data['tag_name'][1:]) > semver(ver)]
            updateAttempt = 3
        except:  # If updating fails 3 times
            latest = '0'
    if semver(latest) > semver(ver):
        print('Update available!      ')
        print(f'Latest Version: v{latest}\n')
        for release in releases:
            print(f'{release[0]}:\n{release[1]}\n')
        confirm = input(str('Update now? [Y/n] ')).upper()
        if confirm != 'N':
            print(f'Downloading {proj} v{latest}...')
            urllib.request.urlretrieve(ddl, os.path.basename(__file__))  # download the latest version to cwd
            import sys; sys.stdout.flush()  # flush any prints still in the buffer
            os.system('cls||clear')  # Clear console window
            os.system(f'"{__file__}"' if Windows else f'python3 "{__file__}"')
            import time; time.sleep(0.2)
            quit()



    if os.name == 'nt': ctypes.windll.kernel32.SetConsoleTitleW(f'   == {proj} v{ver} ==')
    print(f'{proj} v{ver}             ')
    print('\nThis script serves no purpose other than to update itself.')
    print('The code contained within this script is used to update many of my projects')


    print('\nYou can demo the updater functionality by typing in a version value and attempting to check for updates')
    print('This script may fail to update if it is already the latest version for these reasons:')
    print('    - The update code deletes the old version/file, however if the old file has the same filename as the newest version, it will not be deleted')
    print('    - To solve this, try renaming this python file to something else')

    print('\n\nEnter your desired current-version-number to proceed with updating (leave blank for current version)')
    print('If your version number doesn\'t conform to Semver (1.2.3), the update may fail and the script will most likely crash')
    userVer = str(input('\nver = '))
    if userVer != '': ver = userVer