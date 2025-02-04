"Call a function, and pass it only the arguments it expects."

import inspect
from typing import Callable, Any, Union

__version__ = '0.1.0'

class Argument:

    def __init__(
            self,
            positional_ok: bool,
            keyword_ok: bool,
            required: bool,
    ):
        self.positional_ok = positional_ok
        self.keyword_ok = keyword_ok
        self.required = required

class PosOnly(Argument):
    """
    A value that must be passed as a positional argument.

    Arguments:
        value:
            The value to pass to the function.

        required:
            What to do when passing this argument to a function with an 
            incompatible signature.  If `True`, raise an error.  If `False` 
            (the default), ignore it.

    Example:

        >>> from smartcall import PosOnly, call
        >>> def f(a):
        ...     return a
        ...
        >>> call(f, PosOnly(1))
        1
    """

    def __init__(self, value: Any, *, required: bool = False):
        super().__init__(True, False, required)
        self.value = value

    def __repr__(self):
        return _format_repr(self, [repr(self.value)])

class PosOrKw(Argument):
    """
    A value that can be passed as either a positional or a keyword argument.

    Arguments:
        kwarg:
            A single name-value pair.  The name is the "keyword" that will 
            be used when passing this argument as a keyword argument.

        required:
            What to do when passing this argument to a function with an 
            incompatible signature.  If `True`, raise an error.  If `False` 
            (the default), ignore it.

    When the function could accept either kind of argument, a positional 
    argument will be used.  This is because positional arguments don't require 
    that the function use the same argument names as the caller.

    Examples:

        >>> from smartcall import PosOnly, call
        >>> def f(a):
        ...     return a
        ...
        >>> call(f, PosOrKw(a=1))
        1

        Note that the name given to the argument doesn't need to match the 
        function's signature, if the argument is to be passed positionally:

        >>> call(f, PosOrKw(b=1))
        1
    """

    def __init__(self, *, required: bool = False, **kwarg: Any):
        super().__init__(True, True, required)
        self.name, self.value = _parse_kwarg(kwarg)

    def __repr__(self):
        return _format_repr(self, [f'{self.name}={self.value!r}'])

class KwOnly(Argument):
    """
    A value that must be passed as a keyword argument.

    Arguments:
        kwarg:
            A single name-value pair.

        required:
            What to do when passing this argument to a function with an 
            incompatible signature.  If `True`, raise an error.  If `False` 
            (the default), ignore it.

    Example:

        >>> from smartcall import PosOnly, call
        >>> def f(a):
        ...     return a
        ...
        >>> call(f, KwOnly(a=1))
        1
    """

    def __init__(self, *, required: bool = False, **kwarg: Any):
        super().__init__(False, True, required)
        self.name, self.value = _parse_kwarg(kwarg)

    def __repr__(self):
        return _format_repr(self, [f'{self.name}={self.value!r}'])

def call(f: Callable[..., Any], *args: Union[PosOnly, PosOrKw, KwOnly]) -> Any:
    """
    Call the given function with as many of the given arguments as it can 
    accept.

    Arguments:
        f:
            The function to call.  This can be any callable.

            Note that :func:`inspect.signature` is used to determine which 
            arguments the function expects.  This might not work as expected if 
            the function is wrapped by something that changes its signature.  A 
            common example of this is :func:`functools.partial`.  Consider the 
            following example:

                >>> from functools import partial
                >>> def f(a, b):
                ...     return a, b
                ...
                >>> g1 = partial(f, 1)
                >>> g2 = partial(f, a=1)

            While ``g1`` and ``g2`` both supply the first argument to ``f``, 
            the former does so in a way that allows additional positional 
            arguments to be passed, while the latter doesn't.  In other words, 
            the way that :func:`~functools.partial` is invoked can affect the 
            signature of the resulting callable.

        args:
            The arguments to pass to the function.  Any number of arguments can 
            be specified.  Each argument must be an instance of `PosOnly`, 
            `PosOrKw`, or `KwOnly`.  These objects determine how each argument 
            can be passed to the function.  Refer to the above links for more 
            details.  Positional argument are preferred, when there's an 
            option, because they don't require that the function use the same 
            argument names as the caller.

            It's ok to specify more arguments than the function expects.  Any 
            arguments that are incompatible with the given function signature, 
            and that are not marked as "required", will simply not be used.

    Returns:
        The result of calling the given function with the given arguments.

    Example:

        Invoke a callback function with one required positional argument and 
        several optional keyword arguments:

            >>> from smartcall import PosOnly, PosOrKw, KwOnly, call
            >>> def my_callback(a, b):
            ...     return a, b
            ...
            >>> call(
            ...     my_callback,
            ...     PosOnly(1, required=True),  # the required argument
            ...     KwOnly(b=2),                # the optional arguments
            ...     KwOnly(c=2),
            ... )
            (1, 2)
    """
    args = list(args)
    _check_args(args)

    pos_args = []
    kw_args = {}

    pos_params = []
    num_pos_params = 0
    kw_names = set()

    def has_kw_param(name):
        return name in kw_names

    sig = inspect.signature(f)

    for param in sig.parameters.values():
        match param.kind:
            case inspect.Parameter.POSITIONAL_ONLY:
                pos_params.append(param)
                num_pos_params += 1

            case inspect.Parameter.POSITIONAL_OR_KEYWORD:
                pos_params.append(param)
                num_pos_params += 1
                kw_names.add(param.name)

            case inspect.Parameter.VAR_POSITIONAL:
                num_pos_params = float('inf')

            case inspect.Parameter.KEYWORD_ONLY:
                kw_names.add(param.name)

            case inspect.Parameter.VAR_KEYWORD:
                has_kw_param = lambda name: True

            case _:  # pragma: no cover
                raise AssertionError(f"unexpected parameter kind: {param.kind}")

    # Pass as many positional arguments as possible:

    while len(pos_args) < num_pos_params and args:
        if not args[0].positional_ok:
            break

        pos_arg = args.pop(0)
        pos_args.append(pos_arg.value)

        if pos_params:
            pos_param = pos_params.pop(0)
            kw_names.discard(pos_param.name)

    # Pass all eligible keyword arguments, and complain if any required 
    # arguments are skipped:

    for arg in args:
        if arg.keyword_ok:
            if has_kw_param(arg.name):
                kw_args[arg.name] = arg.value
                continue

        if arg.required:
            name = f'`{arg.name}`' if arg.keyword_ok else 'positional'
            raise TypeError(f"{f.__name__}() missing required {name} argument.")

    return f(*pos_args, **kw_args)

def _check_args(args):
    allowed_types = {
            PosOnly: {PosOnly, PosOrKw, KwOnly},
            PosOrKw: {PosOrKw, KwOnly},
            KwOnly:  {KwOnly}
    }
    curr_allowed_types = allowed_types[PosOnly]
    prev_type = None
    pos_required_ok = True
    used_names = set()

    for arg in args:
        if not isinstance(arg, Argument):
            raise TypeError(f"cannot use {arg!r} as an argument.\nArguments must be instances of PosOnly, PosOrKw, or KwOnly")

        curr_type = type(arg)
        if curr_type not in curr_allowed_types:
            raise TypeError(f"cannot use {curr_type.__name__} after {prev_type.__name__}")
        curr_allowed_types = allowed_types[curr_type]
        prev_type = curr_type

        if arg.positional_ok:
            if arg.required and not pos_required_ok:
                raise TypeError("cannot give required positional argument after optional positional argument")
            pos_required_ok = pos_required_ok and arg.required

        if arg.keyword_ok:
            if arg.name in used_names:
                raise TypeError(f"cannot reuse keyword `{arg.name}`")
            used_names.add(arg.name)

def _parse_kwarg(kwarg):
    if len(kwarg) != 1:
        raise ValueError("must specify exactly one key-value pair")

    return next(iter(kwarg.items()))

def _format_repr(self, arg_strs):
    if self.required: arg_strs.append('required=True')
    return f"{self.__class__.__name__}({', '.join(arg_strs)})"

