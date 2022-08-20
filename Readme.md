## Notes
The quiz builder call requires a JWT encoded using a pre-defined secret.

## Development

For running in dev: `export FLASK_ENV=development`

Use the `/token` endpoint to get an auth token, and set that as an Auth Bearer token in a postman client.

## Running

python wsgi.py

## Deploying

git push heroku master

## Testing

python -m unittest tests/*.py

## Updates

### Apr 24, 2021
- Added auth between API and NLP Quiz Builder
- Cleaning up config/options system
- Improved OOP practices
