SmartCall
=========

[![Last release](https://img.shields.io/pypi/v/smartcall.svg)](https://pypi.python.org/pypi/smartcall)
[![Python version](https://img.shields.io/pypi/pyversions/smartcall.svg)](https://pypi.python.org/pypi/smartcall)
[![Documentation](https://img.shields.io/readthedocs/smartcall.svg)](https://smartcall.readthedocs.io/en/latest/)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/smartcall/test.yml?branch=master)](https://github.com/kalekundert/smartcall/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/smartcall)](https://app.codecov.io/github/kalekundert/smartcall)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/smartcall?logo=github)](https://github.com/kalekundert/smartcall)

This library provides a way to call functions that won't necessarily accept all 
of the arguments that you could pass to them.  This situation often occurs when 
writing libraries that accept callback functions.  The library might have lots 
of information that it *could* pass to callbacks, but not every callback will 
want every piece of information.

The following snippet shows how the library works.  As an example, we'll invoke 
a callback with one required positional argument and two optional keyword 
arguments.  Note that the callback only accepts the first keyword argument:

```python
>>> from smartcall import call, PosOnly, KwOnly
>>> def my_callback(a, b):
...     return a, b
...
>>> call(
...     my_callback,
...
...     # This argument is required, so if the callback can't accept it, an
...     # error will be raised.
...     PosOnly(1, required=True), KwOnly('b', 2))
...
...     # These arguments are not required, so they will only be passed to the
...     # callback if it has a compatible signature.
...     KwOnly(b=2),
...     KwOnly(c=3),
... )
(1, 2)
```

Refer to the [online 
documentation](https://smartcall.readthedocs.io/en/latest/) for more 
information.
