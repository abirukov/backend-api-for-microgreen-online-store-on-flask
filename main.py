import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from beaver_app.app import create_app
from beaver_app.commands_manager import compose_command_argparser, run_command

if __name__ == '__main__':
    sentry_sdk.init(
        dsn='https://46ba4ee456734c1e88da5ba1b320ad18@o1164730.ingest.sentry.io/4505240675942400',
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
