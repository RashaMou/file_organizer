from organize.file_organizer import FileOrganizer
from rich.console import Console

import os


def main():
    console = Console()

    while True:
        folder_input = console.input(
            "\n[bold blue]>> :file_folder: Enter folder to organize:[/bold blue] (or 'q' to quit)\n"
        )
        if folder_input.lower() in ["q", "quit"]:
            console.print("\n:wave: Goodbye\n")
            return

        if os.path.isdir(os.path.expanduser(folder_input)):
            folder_path = os.path.expanduser(folder_input)
            organizer = FileOrganizer(folder_path)
            organizer.organize()
            report = organizer.get_report()
            print_report(report, console)
            break
        else:
            console.print(
                f"\n[red bold]Folder [blue]{folder_input}[/blue] is invalid, try again[/red bold]"
            )


def print_report(report, console):
    if len(report["summary"]) > 0:
        console.rule("[bold red]Summary\n")
        console.print("\n".join(report["summary"]))

    if len(report["details"]) > 0:
        console.rule("\n[bold red]Details\n")
        console.print("\n".join(report["details"]))
        print("")


if __name__ == "__main__":
    main()
