# stranslate
[![tests](https://github.com/ffreemt/google-stranslate/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/google-stranslate/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/itranslate.svg)](https://badge.fury.io/py/itranslate)

Google translate free and unlimited access, `stranslate` because gtranslate is taken

## Install it

```shell
pip install itranslate

# or pip install git+https://github.com/ffreemt/google-itranslate
# or use poetry
# poetry add itranslate
# poetry add git+https://github.com/ffreemt/google-itranslate

# to upgrade:
pip install itranslate -U

# or poetry add itranslate@latest
```

## Use it

The quality from this service is not as good as web google translate. There is nothing we can do about it.

It's unclear whether your ip will be blocked if you relentlessly use the service. Please feedback should you find out any information.

```python
from itranslate import itranslate as itrans

itrans("test this and that")  # '测试这一点'

# new lines are preserved, tabs are not
itrans("test this \n\nand test that \t and so on")
# '测试这一点\n\n并测试这一点等等'

itrans("test this and that", to_lang="de")  # 'Testen Sie das und das'
itrans("test this and that", to_lang="ja")  # 'これとそれをテストします'
```

Text longer than 5000 characters will be trimmed to 5000. Hence for a long document, you may try something like the following or similar.
```python
from textwrap import wrap
from itranslate import itranslate as itrans

long_doc = """ long long text formatted with \n and so on"""
tr_doc = " ".join([itrans(elm) for elm in wrap(long_doc,
    width=5000,
    break_long_words=False,
    break_on_hyphens=False,
    drop_whitespace=False,
    replace_whitespace=False,
)])
```

### `async version`: `atranslate`
If you feel so inclined, you may use the async version of itranslate ``atranslate``:
```python
import asyncio
from itranslate import atranslate as atrans

texts = ["test this", "test that"]
coros = [atrans(elm) for elm in texts]

loop = asyncio.get_event_loop()

trtexts = loop.run_until_complete(asyncio.gather(*coros))

print(trtexts)
# ['测试这一点', '测试']
```

### Proxy support
```
itrans("test this and that", proxies="http://localhost:8030")
```
or
```python
proxies = {
    "http": "http://localhost:8030",
    "https": "http://localhost:8031",
}
itrans("test this and that\n another test", proxies=proxies)
```

`itranslate` uses ``httpx`` to fetch contents and inherits ``httpx``'s proxy mechanism. Check [https://www.python-httpx.org/advanced/](https://www.python-httpx.org/advanced/) for other ways of setting up proxies.

## Other google translate related repos
Much more sophisticated than `itranslate`
*   [https://github.com/ssut/py-googletrans](https://github.com/ssut/py-googletrans) [![](https://img.shields.io/github/stars/ssut/py-googletrans)](https://github.com/ssut/py-googletrans)
*   [https://github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) [![](https://img.shields.io/github/stars/nidhaloff/deep-translator)](https://github.com/nidhaloff/deep-translator)

*   [https://github.com/mouuff/mtranslate](https://github.com/mouuff/mtranslate) [![](https://img.shields.io/github/stars/mouuff/mtranslate)](https://github.com/mouuff/mtranslate)
*   [https://github.com/lushan88a/google_trans_new](https://github.com/lushan88a/google_trans_new) [![https://github.com/lushan88a/google_trans_new](https://img.shields.io/github/stars/lushan88a/google_trans_new)](https://github.com/lushan88a/google_trans_new)
*   [https://github.com/Animenosekai/translate](https://github.com/Animenosekai/translate) [![https://github.com/Animenosekai/translate](https://img.shields.io/github/stars/Animenosekai/translate)](https://github.com/Animenosekai/translate)

## Disclaimer
``google-stranslate`` makes use of a translate interface floating around the net and is for study and research purpose only. The interface may become invalid without notice, which would of course render the package totally unusable.
