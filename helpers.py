
import json
from urllib.request import urlopen


def is_url_reachable(url):
    try:
        with urlopen(url, timeout=10) as response:
            return response.status == 200
    except Exception:
        return False


def retrieve_phone_code(driver):
    logs = driver.get_log("performance")

    for log in logs:
        try:
            message = json.loads(log["message"])["message"]

            if message.get("method") != "Network.responseReceived":
                continue

            params = message.get("params", {})
            response = params.get("response", {})
            url = response.get("url", "")

            if "phone" not in url.lower():
                continue

            request_id = params.get("requestId")

            body = driver.execute_cdp_cmd(
                "Network.getResponseBody",
                {"requestId": request_id}
            )

            data_response = json.loads(body["body"])

            if "code" in data_response:
                return str(data_response["code"])

        except (KeyError, ValueError, TypeError):
            continue

    raise RuntimeError(
        "Código de confirmação não encontrado nos registros do navegador."
    )
