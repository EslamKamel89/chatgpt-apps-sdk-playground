import requests

from src.mcp import mcp


@mcp.tool()
def get_cryptocurrency_price(crypto: str) -> str | None:
    """
    Gets the price of a cryptocurrency
    Args:
        crypto (str): symbol of the cryptocurrency (for example 'bitcoin' , 'ethereum')
    Returns:
        str|None: return price in usd, if None is returned this means something went wrong
    """
    crypto = crypto.lower().strip()
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto, "vs_currencies": "usd"}
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        price = data.get(crypto, {}).get("usd")
        return str(price)
    except Exception as e:
        print(e)
        return None
