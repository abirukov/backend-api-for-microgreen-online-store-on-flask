from beaver_app.app import create_app
from beaver_app.commands_manager import compose_command_argparser, run_command

if __name__ == '__main__':
    app = create_app()
    args = compose_command_argparser().parse_args()
    if args.command:
        run_command(
            app,
            args.command,
            commands_module="my_wallet.commands",
        )
    else:
        app.run(debug=True)
