# itranslate
[![tests](https://github.com/ffreemt/google-itranslate/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/google-itranslate/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/itranslate.svg)](https://badge.fury.io/py/itranslate)

Google translate free and unlimited access, `itranslate` because gtranslate is taken

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

# new lines are preserved
itrans("test this \n\nand that")  # '测试这一点\n\n然后'

itrans("test this and that", to_lang="de")  # 'Testen Sie das und das'
itrans("test this and that", to_lang="ja")  # 'これとそれをテストします'
```

### `async version`: `atranslate`
If you feel so inclined, you may use the async version of itranslate: atranslate:
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

### Proxies support
```
itrans("test this and that", proxies="http://localhost:8030")
```
or
```python
proxies = {
    "http://": "http://localhost:8030",
    "https://": "http://localhost:8031",
}
itrans("test this and that\n another test", proxies=proxies)
```

Check [https://www.python-httpx.org/advanced/](https://www.python-httpx.org/advanced/) for other ways of setting up proxies.

## Disclaimer
``itranslate`` takes advantage of a google translate interface floating around the net and is for study and research purpose only. The interface may become invalid without notice, which will render ``itranslate`` completely useless.
