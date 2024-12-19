import os
from typing import Optional
from rich.spinner import Spinner
from rich.live import Live

from easycloud.infra_utils.terraform import TerraformWrapper
from rich import print as rprint

from easycloud.utils.os import get_package_directory, copy_assets
from easycloud.ai.chat import ChatSession


def init_project(workdir: str = ".easycloud/default", verbose: bool=False):
    """Initialize a new project."""

    # Ensure default directory exists inside .easycloud
    os.makedirs(workdir, exist_ok=True)

    # Copy boilerplate assets from assets/ to workdir
    package_dir = get_package_directory("easycloud")
    assets_dir = os.path.join(package_dir, "../../assets/terraform/")
    copy_assets(assets_dir, workdir)
    rprint(f"[green] Initialized project directory ({workdir})[/green]")

    # Initialize Terraform in the default directory
    terraform_wrapper = TerraformWrapper(workdir)

    # Create a spinner
    spinner = Spinner("dots", text="Initializing terraform (backend, plugins, etc)...")


    try:
        # Use Live context to manage the spinner
        # TODO: Actually a live spinner does not play well with stdout outputs from terraform init
        with Live(spinner, refresh_per_second=10) as live:
            terraform_wrapper.init(verbose=verbose)
        rprint(f"[green]Initialized terraform[/green]")
    except Exception as e:
        rprint(f"[bold red]{e}[/bold red]")
    
    rprint(f"[bold green]Project initialized successfully[/bold green]")


def start_chat_session(component_name: Optional[str] = None, workdir: str = ".easycloud/default"):
    """Start an interactive chat session about infrastructure components."""
    chat_session = ChatSession(workdir=workdir)
    chat_session.start_chat(component_name)
