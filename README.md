# DNSChanger
## Description

This project-as the name of it suggests-is for changing your Windows's connected dns with one click!

DNSChanger was made with python and CustomTkinter for custom UI and converted to EXE using PyInstaller.

You can either download the project from here or use the:
- ```git clone https://github.com/ItzAlireza/dnschanger```

## Setting.json
`setting.json` is the configuration file of the project and it also contains the dns data for project.

`setting.json` has two keys:
- `'app'`
- `'dns'`

### `app`
Contains app setting, currently has limited options!
- `geometry`: is a string that defines height and width of the app like: '350x500'
- `colorMode`: is a string that defines dark mode or light mode of the app.
### `dns`
Contains dns info like dnsName and dns ip addresses, like:
```
"Google": ["8.8.8.8", "8.8.4.4"]
```
The formatting of the dns data is essential and if done wrong, will return errors!

## Issues
If you got any issues regarding dns data format, we will suggest you to replace your `setting.json` file with the default one in the repository

## Release
To get the executable package please download the latest [release](https://github.com/ItzAlireza/dnschanger/releases) version.

In order to use the app:

- Extract ZIP file to your destination
- Make sure there's a `setting.json` and a `icon.ico` file in the directory
- Use the shortcut after the extraction to launch the app
- Finally make sure app is running with administrator privileges
