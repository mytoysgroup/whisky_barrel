import click
@click.command()
@click.argument('arg')
def openvpn(arg):
    print("openvpn: '" + arg + "'")

@click.command()
@click.argument('arg')
def pour(arg):
    print("pour: " + arg)