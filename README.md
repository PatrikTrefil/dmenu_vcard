# Dmenu script to extract e-mail and phone numbers from vcard files

## Usage

1. Clone this repository `git clone https://github.com/eventable/vobject.git`
2. Go into the repository `cd <path to repo>`
3. Run `pipenv install` to install all the dependencies
4. Run (always from the root folder of the project) `pipenv run go` to run the program

Optionally, you can add a keyboard shortcut or a shell alias like this (this example is for sxhkd)

```sxhkdrc
super + c
  cd <absolute path to repo> && pipenv run go
```
