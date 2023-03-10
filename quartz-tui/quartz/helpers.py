import signal
import multitasking

from icmplib import ICMPv4Socket, ICMPRequest
from icmplib import ICMPLibError, ICMPError, TimeoutExceeded
from icmplib import PID
from time import sleep
from quartz.utils import generate_output


signal.signal(signal.SIGINT, multitasking.killall)


class HostPinguer:
    """
    Pings a host multiple times and get the response time and status.
    """

    def __init__(self, host: str, count: int):
        """
        Initializes a HostPinguer object with the specified host and number of pings.

        Parameters:
            host (str): The IP address or domain name of the host to ping.
            count (int): The number of times to ping the host.
        """

        self.host: str = host
        self.count: int = count
        self.status = None
        self.status_color = "green"
        self.sock = ICMPv4Socket(privileged=False)

    @multitasking.task
    def ping(self, timeout=2, id=PID):
        """
        Pings the host multiple times and updates the status of the HostPinguer object.

        Parameters:
            timeout (int): The timeout value in seconds for the ping request (default: 2).
            id (int): The ID of the ping request (default: PID).

        Returns:
            None
        """
        accumulated_ms, successful_requests, average = 0, -1, 0

        for sequence in range(self.count * 4):
            request = ICMPRequest(destination=self.host, id=id, sequence=sequence)

            try:
                self.sock.send(request)
                reply = self.sock.receive(request, timeout)

                reply.raise_for_status()
                round_trip_time = (reply.time - request.time) * 1000

                accumulated_ms += round_trip_time
                successful_requests += 1

                average = (
                    round(accumulated_ms / successful_requests, 3)
                    if successful_requests > 0
                    else round(accumulated_ms, 3)
                )

                self.status = generate_output(
                    {
                        "ms": round(round_trip_time, 3),
                        "host": self.host,
                        "ip_address": reply.source,
                        "avg_ms": average,
                        "sent_req": sequence,
                        "success_req": successful_requests,
                    }
                )
                self.status_color = "green"

            except TimeoutExceeded as err:
                # The timeout has been reached
                self.status = generate_output(
                    {
                        "error": "timeout",
                        "host": self.host,
                        "avg_ms": average,
                        "sent_req": sequence,
                        "success_req": successful_requests,
                    }
                )
                self.status_color = "red"

            except ICMPError as err:
                # An ICMP error message has been received
                self.status = generate_output(
                    {
                        "error": f"Unknown error. {err}",
                        "host": self.host,
                        "avg_ms": average,
                        "sent_req": sequence,
                        "success_req": successful_requests,
                    }
                )
                self.status_color = "red"

            except ICMPLibError as err:
                if "-3" in err.__str__():
                    self.status = generate_output(
                        {
                            "error": "dns",
                            "host": self.host,
                            "avg_ms": average,
                            "sent_req": sequence,
                            "success_req": successful_requests,
                        }
                    )
                    self.status_color = "red"
                elif "101" in err.__str__():
                    self.status = generate_output(
                        {
                            "error": "unreachable",
                            "host": self.host,
                            "avg_ms": average,
                            "sent_req": sequence,
                            "success_req": successful_requests,
                        }
                    )
                    self.status_color = "red"
                else:
                    if self.host is None:
                        self.status = generate_output(None)
                    else:
                        self.status = generate_output(
                            {
                                "error": err,
                                "host": self.host,
                                "avg_ms": average,
                                "sent_req": sequence,
                                "success_req": successful_requests,
                            }
                        )
                    self.status_color = "red"

            if sequence < (self.count * 4) - 1:
                sleep(0.25)
        return

    def get_status(self):
        return self.status

    def get_status_color(self):
        return self.status_color

    def get_host(self):
        if self.host == "auth.afip.gob.ar":
            return "[bold blue]AFIP[/bold blue] :man_police_officer:"
        if self.host == "cdn.netflix.com":
            return "[bold red]Netflix[/bold red] :movie_camera:"
        if self.host == "ec2.us-east-1.amazonaws.com":
            return "[bold #FF9900]AWS[/bold #FF9900] :cloud:"
        return self.host
