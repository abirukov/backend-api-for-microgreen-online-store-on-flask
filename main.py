import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration

from beaver_app.app import create_app
from beaver_app.commands_manager import compose_command_argparser, run_command

if os.path.exists(os.path.join(os.path.dirname(__file__), '.env')):
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if __name__ == '__main__':
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0,
    )
    app = create_app()
    args = compose_command_argparser().parse_args()
    if args.command:
        run_command(
            app,
            args.command,
            commands_module='beaver_app.commands',
        )
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
