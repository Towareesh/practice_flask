# Building

This is a training project on flask.

## Installation

```bash
git clone https://github.com/Towareesh/practice_flask.git
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

```bash
pip install -r requirements.txt
```

## Usage

```cmd
flask shell
```
```flask shell
db.create_all()
db.session.commit()
```
## Launch
```cmd
flask run
```
or
```cmd
python3 runner.py
```
## Translate commands
```cmd
pybabel extract -F babel.cfg -k _l -o messages.pot .
```
```cmd
pybabel init -i messages.pot -d app/translations -l 'your lang'
```
```cmd
pybabel compile -d app/translations
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
