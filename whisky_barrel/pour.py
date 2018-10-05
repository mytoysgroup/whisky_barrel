import click
@click.command()
@click.argument('arg')
def main(arg):
    print("bla: '" + arg + "'")

