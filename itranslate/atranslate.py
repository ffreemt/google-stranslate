"""Translate via googlge translate."""
from typing import Union

import json
from urllib.parse import quote
import httpx
from logzero import logger


# fmt: off
async def atranslate(
        text: str,
        from_lang: str = "auto",
        to_lang: str = "zh",
        proxies: Union[str, dict] = None,
        timeout: Union[float, httpx.Timeout] = 10,
        verify: bool = False,
        url: str = None,
        cf: bool = False,  # for people who cant access google, set this to True
) -> str:
    r"""Tranaslate via googlge translate, async version.

    Args:
        text: string
        from_lang:, "auto" (default), "zh", "en" etc
        from_lang:, "zh" (default), "en" etc
        proxies: "http://...", {"http": "http:...", "https": "https://..."}
        timeout: default 5 sec, use a larger value for slow net.
            More granular timeouts can be set. refer to https://www.python-httpx.org/advanced/#timeout-configuration
        url: which site to use, default https://translate.google.cn
    Returns:
        translated text: string

    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(atranslate('test this and that'))
    '测试这一点'
    >>> loop.run_until_complete(atranslate('test this and that', to_lang="de"))
    'Testen Sie das und das'
    """
    # fmt: on
    text_ = text
    text = str(text)
    if not text:
        return ""

    if len(text) > 5000:
        logger.warning(" text (%s) too longer, trimmed to 5000", len(text))
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

    _ = """
    client = get_client(
        proxies=proxies,
        verify=verify,
    )
    # """

    # _ = [[text, from_lang, to_lang, True], [1]]
    # _ = [[["MkEWBc", str(_), None, "generic"]]]
    # _ = f"f.req={quote(str(_))}"

    # [None] or [1] both work
    _ = [[text, from_lang, to_lang, True], [None]]
    _ = [[["MkEWBc", json.dumps(_), None, "generic"]]]
    data = {"f.req": json.dumps(_)}

    # logger.debug("url: %s", f"{url}/_/TranslateWebserverUi/data/batchexecute")
    async with httpx.AsyncClient(
        proxies=proxies,
        verify=verify,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    ) as client:
        if cf:
            try:
                resp = await client.post("https://gtr.ttw.workers.dev", json=data, timeout=timeout)
                resp.raise_for_status()
            except Exception as e:
                logger.error(e)
                raise   
        else:
            try:
                # resp = await client.post(f"{url}/_/TranslateWebserverUi/data/batchexecute", data=_, timeout=timeout)
                resp = await client.post(f"{url}/_/TranslateWebserverUi/data/batchexecute", data=data, timeout=timeout)
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
            trtext = " ".join([elm[0] for elm in _[1][0][0][5]])
        # ic(trtext)

    return trtext
