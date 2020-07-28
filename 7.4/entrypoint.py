import click
import sys
import subprocess


@click.group(invoke_without_command=True, context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def cli(ctx, args):
    subprocess.check_call("sh /update-host-machine.sh", shell=True)
    try:
        if args[0] == 'serve':
            ctx.invoke(serve)
    except IndexError:
        pass
    try:
        subprocess.check_call(list(args))
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


@cli.command()
def serve():
    """ Run PHP-fpm, cron, nginx """
    click.echo("Starting crond...")
    subprocess.check_call("crond")
    click.echo("Starting nginx & fpm...")
    subprocess.check_call("nginx -g \"daemon off;\" & docker-php-entrypoint php-fpm -R", shell=True)


if __name__ == '__main__':
    cli()
