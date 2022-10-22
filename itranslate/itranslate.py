"""Translate via googlge translate.

  if url is None:
        url = "https://translate.google.cn"  # => https://translate.google.com.hk

  url_ = f"{url}/_/TranslateWebserverUi/data/batchexecute"
  seems no longer work

https://github.com/ssut/py-googletrans/issues/268

For manual testing:
from typing import Union

import json
# from urllib.parse import (quote, urlencode,)

# import urllib3
from datetime import datetime
from joblib import Memory
import httpx

text: str = 'organic'
from_lang: str = "en"
to_lang: str = "zh"
proxies: Union[str, dict] = None
timeout: Union[float, httpx.Timeout] = 10
verify: bool = False
url: str = None


"""
from typing import Union

import json

# from urllib.parse import (quote, urlencode,)

# import urllib3
from datetime import datetime
from joblib import Memory
import httpx
from logzero import logger

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
location = "./cachedir"
memory = Memory(location, verbose=0)


@memory.cache
def get_client(
    proxies: Union[str, dict] = None, verify: bool = False, headers: dict = None
) -> httpx.Client:
    """Gen and cache a httpx.Client.

    Args:
        proxies: setup and persistant
    """
    # url = "https://translate.google.cn"
    if headers is None:
        headers = {
            # 'Referer': 'http://translate.google.cn/',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }

    if proxies is None:
        client = httpx.Client(verify=verify, headers=headers)
    else:
        client = httpx.Client(proxies=proxies, verify=verify, headers=headers)

    # client.event_hooks["response"] = [raise_on_4xx_5xx]
    # client.event_hooks["request"] = [log_request]
    # client.event_hooks["request"] = [add_timestamp]
    return client


def add_timestamp(request):
    """Add timestamp to request."""
    # request.headers['x-request-timestamp'] = datetime.now(tz=datetime.utc).isoformat()  # datetime.timetz
    request.headers["x-request-timestamp"] = datetime.now().isoformat()


def log_request(request):
    """Log requset."""
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")


def raise_on_4xx_5xx(response):
    """Raise for 4xx/5xx event_hook."""
    response.raise_for_status()


# fmt: off
def itranslate(
        text: str,
        from_lang: str = "auto",
        to_lang: str = "zh",
        proxies: Union[str, dict] = None,
        timeout: Union[float, httpx.Timeout] = 10,
        verify: bool = False,
        url: str = None,
        cf: bool = False,  # for people who cant access google, set this to True
) -> str:
    r"""Tranaslate via googlge translate.

    Args:
        text: string
        from_lang:, "auto" (default), "zh", "en" etc
        from_lang:, "zh" (default), "en" etc
        proxies: "http://...", {"http": "http:...", "https": "https://..."}
        timeout: default 10 sec, use a larger value for slow net.
            More granular timeouts can be set, refer to https://www.python-httpx.org/advanced/#timeout-configuration
        url: which site to use, default https://translate.google.cn
    Returns:
        translated text: string

    >>> itranslate('test this and that')
    '测试这个'
    >>> itranslate('test this and that', to_lang="de")
    'Testen Sie das und das'
    """
    # fmt: on
    text_ = text
    text = str(text)
    if not text.strip():
        return text

    if len(text) > 5000:
        logger.warning(" text (%s) too long, trimmed to 5000", len(text))
        text = text[:5000]

    try:
        from_lang = str(from_lang).strip()
    except Exception as e:
        logger.error("from_lang errors: %s, setting to 'auto'", e)
        from_lang = "auto"
    try:
        to_lang = str(to_lang).strip()
    except Exception as e:
        logger.error("to_lang errors: %s, setting to 'zh'", e)
        from_lang = "zh"
    if to_lang == "auto":
        if from_lang not in ["zh"]:
            to_lang = "zh"
        elif from_lang not in ["en"]:
            to_lang = "en"
        # other cases?
    if to_lang == from_lang:
        logger.info("Nothing to do man, returning the original")
        return text_

    if url is None:
        url = "https://translate.google.com.hk"

    url_ = f"{url}/_/TranslateWebserverUi/data/batchexecute"

    # url_ = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute"
    
    client = get_client(
        proxies=proxies,
        verify=verify,
        # headers={}  # no headers if params is set
    )

    # better use json.dumps(_, separators=(',', ":")) than str(_)
    # no need, just use default json.dumps
    # def dumps(x): return json.dumps(x, separators=(',', ":"))

    if cf:
        data = {"text": text, "from_lang": from_lang, "to_lang": to_lang}
        try:
            resp = client.post("https://gtr.ttw.workers.dev", json=data, timeout=timeout)
            resp.raise_for_status()
        except Exception as e:
            logger.error(e)
            raise        
    else:
        # [None] or [1] both work
        _ = [[text, from_lang, to_lang, True], [None]]
        _ = [[["MkEWBc", json.dumps(_), None, "generic"]]]

        data = {"f.req": json.dumps(_)}
        # data = {"rpcids": json.dumps(_)}

        # data = {"f.req": rf"""[[["MkEWBc","[[\"{text}\",\"{from_lang}\",\"{to_lang}\",true],[null]]",null,"generic"]]]"""}
        # _ = f"f.req={quote(dumps(_))}"

        # logger.debug("url: %s", f"{url}/_/TranslateWebserverUi/data/batchexecute")
        try:
            # resp = client.post(url_, data=_, timeout=timeout)

            resp = client.post(url_, data=data, timeout=timeout)

            # resp = client.post(url_, data=urlencode(data), timeout=timeout)
            resp.raise_for_status()
        except Exception as e:
            logger.error(e)
            raise
    try:
        jdata = json.loads(resp.text.splitlines()[2])
    except Exception as e:
        logger.error(e)
        raise
    try:
        _ = json.loads(jdata[0][2])
    except Exception as e:
        logger.error(e)
        raise

    if to_lang in ['zh']:
        trtext = "".join([elm[0] for elm in _[1][0][0][5]])
    else:
        try:
            trtext = " ".join([elm[0] for elm in _[1][0][0][-1]])
        except TypeError:  # try
            try:
                trtext = _[1][0][-1][0]
            except Exception as e:
                logger.error(e)
                # trtext = str(e)
                raise
        except Exception as e:
            logger.error(e)
            raise

    # ic(trtext)

    return trtext
