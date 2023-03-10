import netifaces
import re

GATEWAYS = netifaces.gateways()


def get_default_gateway():
    """Returns the host's default interface's gateway IPv4 address.

    Returns:
        str: IPv4 address of the gateway.
    """
    return GATEWAYS.get("default", {}).get(netifaces.AF_INET, [None])[0]


def get_icmp_color(icmp_ms: int) -> str:
    """
    Returns a string representation of the given ICMP round trip time in milliseconds, along with a corresponding color.

    Args:
        icmp_ms (int): The ICMP round trip time in milliseconds.

    """
    if icmp_ms > 200:
        return f"[red]{icmp_ms} ms[/red]"
    elif icmp_ms > 100:
        return f"[orange1]{icmp_ms} ms[/orange1]"
    else:
        return f"[green]{icmp_ms} ms[/green]"


def get_error_message(error_type: str) -> str:
    if error_type == "dns":
        return "No se pudo resolver la URL, error de DNS."
    if error_type == "unreachable":
        return "No se puede llegar al destino."
    return error_type


def generate_output(icmp_reply):
    """
    Generates a formatted string with information about an ICMP reply.

    Args:
        icmp_reply (dict): A dictionary containing information about an ICMP reply.
            If the 'error' key is present, the dictionary is assumed to represent
            a failed ping attempt. Otherwise, the dictionary is assumed to represent
            a successful ping attempt.

    Returns:
        A formatted string with the text to ouput in a Quartz panel.
        If icmp_reply is None, returns a default error message.
    """
    if icmp_reply is None:
        return "No se pudo detectar dirección de IP automáticamente ¯\_(ツ)_/¯"

    if "error" in icmp_reply.keys():
        panel_info = "\n".join(
            [
                f"[bold]URL de destino:[/bold] {icmp_reply['host']}",
                f"[bold]Error:[/bold] {get_error_message(icmp_reply['error'])}",
                f"[bold]Tiempo promedio:[/bold] {icmp_reply['avg_ms']} ms",
                f"[bold]Requests exitosas:[/bold] {icmp_reply['success_req'] if icmp_reply['success_req'] > 0 else 0}/{icmp_reply['sent_req']}",
            ]
        )
    else:
        panel_info = "\n".join(
            [
                f"[bold]IP de destino:[/bold] {icmp_reply['ip_address']}"
                if re.match(
                    r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",
                    icmp_reply["host"],
                )
                else f"[bold]IP de destino:[/bold] {icmp_reply['ip_address']}\n[bold]URL de destino:[/bold] {icmp_reply['host']}",
                f"[bold]Tiempo:[/bold] {get_icmp_color(icmp_reply['ms'])}",
                f"[bold]Tiempo promedio:[/bold] {icmp_reply['avg_ms']} ms",
                f"[bold]Requests exitosas:[/bold] {icmp_reply['success_req']}/{icmp_reply['sent_req']}",
            ]
        )

    return panel_info
