
import json
import time
from urllib.request import urlopen


def is_url_reachable(url):
    """Verifica se o servidor Urban Routes está acessível."""
    try:
        with urlopen(url, timeout=10) as response:
            return response.status == 200
    except Exception:
        return False


def retrieve_phone_code(driver):
    """Recupera o código SMS dos logs de rede do Chrome."""

    pending_requests = {}

    for _ in range(15):
        try:
            logs = driver.get_log("performance")

            for log in logs:
                try:
                    message = json.loads(log["message"])["message"]
                    method = message.get("method")
                    params = message.get("params", {})

                    if method == "Network.responseReceived":
                        request_id = params.get("requestId")
                        response = params.get("response", {})
                        url = response.get("url", "")

                        if request_id:
                            pending_requests[request_id] = url

                    elif method == "Network.loadingFinished":
                        request_id = params.get("requestId")

                        if request_id not in pending_requests:
                            continue

                        try:
                            result = driver.execute_cdp_cmd(
                                "Network.getResponseBody",
                                {"requestId": request_id}
                            )

                            body_text = result.get("body", "")

                            if not body_text:
                                continue

                            body_data = json.loads(body_text)

                            if (
                                isinstance(body_data, dict)
                                and "code" in body_data
                            ):
                                return str(body_data["code"])

                        except Exception:
                            continue

                except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                    continue

        except Exception:
            pass

        time.sleep(1)

    raise RuntimeError(
        "Código de confirmação não encontrado nos logs de rede."
    )