import pytest
from smartcall import PosOnly, PosOrKw, KwOnly, call

def test_call_empty():

    def f(): pass

    # 0 arguments:
    assert call(f) == None

    # 1 argument:
    assert call(f, PosOnly(1)) == None
    assert call(f, PosOrKw(a=1)) == None
    assert call(f, KwOnly(a=1)) == None

    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True))

def test_call_pos_only_1():

    def f(a, /):
        return a

    # 0 arguments:
    with pytest.raises(TypeError):
        call(f)

    # 1 argument:
    assert call(f, PosOnly(1)) == 1
    assert call(f, PosOrKw(a=1)) == 1

    assert call(f, PosOnly(1, required=True)) == 1
    assert call(f, PosOrKw(a=1, required=True)) == 1

    with pytest.raises(TypeError):
        call(f, KwOnly(a=1))  # [1]
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True))  # [1]

    # 2 arguments:
    assert call(f, PosOnly(1), PosOnly(2)) == 1
    assert call(f, PosOnly(1), PosOrKw(a=2)) == 1
    assert call(f, PosOnly(1), KwOnly(a=2)) == 1
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(b=1), PosOrKw(c=2)) == 1  # [2]
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == 1
    assert call(f, PosOrKw(b=1), KwOnly(c=2)) == 1  # [2]

    assert call(f, PosOnly(1, required=True), PosOnly(2)) == 1
    assert call(f, PosOnly(1, required=True), PosOrKw(a=2)) == 1
    assert call(f, PosOnly(1, required=True), KwOnly(a=2)) == 1
    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(b=1, required=True), PosOrKw(c=2)) == 1  # [2]
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2)) == 1
    assert call(f, PosOrKw(b=1, required=True), KwOnly(c=2)) == 1  # [2]

    with pytest.raises(TypeError):
        call(f, KwOnly(b=1), KwOnly(c=2))
    with pytest.raises(TypeError):
        call(f, KwOnly(b=1, required=True), KwOnly(c=2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOnly(2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOrKw(a=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), KwOnly(a=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), PosOrKw(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1, required=True), PosOrKw(c=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), KwOnly(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1, required=True), KwOnly(c=2, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(b=1, required=True), KwOnly(c=2, required=True))

    # [1] Even though argument names match, the argument is positional-only, so 
    #     it won't be passed.  As a result, the function will raise because it 
    #     didn't get an argument.
    #
    # [2] Ok that the argument has the wrong name, because it's passed 
    #     positionally.

def test_call_pos_or_kw_1():

    def f(a):
        return a

    # 0 arguments:
    with pytest.raises(TypeError):
        call(f)

    # 1 argument:
    assert call(f, PosOnly(1)) == 1
    assert call(f, PosOrKw(a=1)) == 1
    assert call(f, PosOrKw(b=1)) == 1  # [1]

    assert call(f, PosOnly(1, required=True)) == 1
    assert call(f, PosOrKw(a=1, required=True)) == 1
    assert call(f, PosOrKw(b=1, required=True)) == 1  # [1]

    # 2 arguments:
    assert call(f, PosOnly(1), PosOnly(2)) == 1
    assert call(f, PosOnly(1), PosOrKw(a=2)) == 1  # [2]
    assert call(f, PosOnly(1), KwOnly(a=2)) == 1  # [2]
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(b=1), PosOrKw(c=2)) == 1  # [1]
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == 1
    assert call(f, PosOrKw(b=1), KwOnly(c=2)) == 1  # [1]
    assert call(f, KwOnly(a=1), KwOnly(b=2)) == 1
    assert call(f, KwOnly(b=1), KwOnly(a=2)) == 2

    assert call(f, PosOnly(1, required=True), PosOnly(2)) == 1
    assert call(f, PosOnly(1, required=True), PosOrKw(a=2)) == 1  # [2]
    assert call(f, PosOnly(1, required=True), KwOnly(a=2)) == 1  # [2]
    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(b=1, required=True), PosOrKw(c=2)) == 1  # [1]
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2)) == 1
    assert call(f, PosOrKw(b=1, required=True), KwOnly(c=2)) == 1  # [1]
    assert call(f, KwOnly(a=1, required=True), KwOnly(b=2)) == 1

    with pytest.raises(TypeError):
        call(f, KwOnly(b=1, required=True), KwOnly(a=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOnly(2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOrKw(a=2, required=True))  # [2]
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), KwOnly(a=2, required=True))  # [2]
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), PosOrKw(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1, required=True), PosOrKw(c=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), KwOnly(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1, required=True), KwOnly(c=2, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True), KwOnly(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(b=1, required=True), KwOnly(a=2, required=True))

    # [1] Ok that the argument has the wrong name, because keyword arguments 
    #     are only used if positional arguments are impossible.
    #
    # [2] Even though the `a` argument has a value of 2, the positional 
    #     argument is the one that gets used.

def test_call_pos_or_kw_2():

    def f(a, b):
        return a, b

    # 0 arguments:
    with pytest.raises(TypeError):
        call(f)

    # 1 argument:
    with pytest.raises(TypeError):
        call(f, PosOnly(1))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1))

    # 2 arguments:
    assert call(f, PosOnly(1), PosOnly(2)) == (1, 2)
    assert call(f, PosOnly(1), PosOrKw(a=2)) == (1, 2)  # [1]
    assert call(f, PosOnly(1), KwOnly(b=2)) == (1, 2)
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == (1, 2)
    assert call(f, PosOrKw(b=1), PosOrKw(a=2)) == (1, 2) # [1]
    assert call(f, PosOrKw(c=1), PosOrKw(d=2)) == (1, 2)
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == (1, 2)
    assert call(f, PosOrKw(c=1), KwOnly(b=2)) == (1, 2)
    assert call(f, KwOnly(a=1), KwOnly(b=2)) == (1, 2)
    assert call(f, KwOnly(b=1), KwOnly(a=2)) == (2, 1)

    with pytest.raises(TypeError):
        call(f, PosOnly(1), KwOnly(a=2))  # [1]
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1), KwOnly(a=2))

    # [1] These are tricky cases.  If the 'a' argument is given as "positional 
    #     or keyword", then it can get mapped to the 'b' parameter if the 'a' 
    #     parameter is already taken.  But if the 'a' argument is "keyword 
    #     only", then it must get mapped to the 'a' parameter.

def test_call_kw_only():

    def f(*, a):
        return a

    # 0 arguments:
    with pytest.raises(TypeError):
        call(f)

    # 1 argument:
    assert call(f, PosOrKw(a=1)) == 1
    assert call(f, KwOnly(a=1)) == 1

    assert call(f, PosOrKw(a=1, required=True)) == 1
    assert call(f, KwOnly(a=1, required=True)) == 1

    with pytest.raises(TypeError):
        call(f, PosOnly(1))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1))

    # 2 arguments:
    assert call(f, PosOnly(1), PosOrKw(a=2)) == 2
    assert call(f, PosOnly(1), KwOnly(a=2)) == 2
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == 1
    assert call(f, KwOnly(a=1), KwOnly(b=2)) == 1

    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2)) == 1
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2)) == 1
    assert call(f, KwOnly(a=1, required=True), KwOnly(b=2)) == 1

    with pytest.raises(TypeError):
        call(f, PosOnly(1), PosOrKw(b=2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1), KwOnly(b=2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOrKw(a=2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), KwOnly(a=2))
    with pytest.raises(TypeError):
        call(f, PosOrKw(b=1, required=True), PosOrKw(a=2))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), PosOrKw(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), KwOnly(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True), KwOnly(b=2, required=True))

def test_call_var_pos():

    def f(*args):
        return args

    # 0 arguments:
    assert call(f) == ()

    # 1 argument:
    assert call(f, PosOnly(1)) == (1,)
    assert call(f, PosOrKw(a=1)) == (1,)
    assert call(f, KwOnly(a=1)) == ()

    assert call(f, PosOnly(1, required=True)) == (1,)
    assert call(f, PosOrKw(a=1, required=True)) == (1,)

    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True))

    # 2 arguments:
    assert call(f, PosOnly(1), PosOnly(2)) == (1, 2)
    assert call(f, PosOnly(1), PosOrKw(b=2)) == (1, 2)
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == (1, 2)
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == (1,)
    assert call(f, KwOnly(a=1), KwOnly(b=2)) == ()

    assert call(f, PosOnly(1, required=True), PosOnly(2)) == (1, 2)
    assert call(f, PosOnly(1, required=True), PosOrKw(b=2)) == (1, 2)
    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2)) == (1, 2)
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2)) == (1,)

    assert call(f, PosOnly(1, required=True), PosOnly(2, required=True)) == (1, 2)
    assert call(f, PosOnly(1, required=True), PosOrKw(b=2, required=True)) == (1, 2)
    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2, required=True)) == (1, 2)

    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True), KwOnly(b=2))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1, required=True), KwOnly(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1, required=True), KwOnly(b=2, required=True))

def test_call_var_kw():

    def f(**kwargs):
        return kwargs

    # 0 arguments:
    assert call(f) == {}

    # 1 argument:
    assert call(f, PosOnly(1)) == {}
    assert call(f, PosOrKw(a=1)) == {'a': 1}
    assert call(f, KwOnly(a=1)) == {'a': 1}

    assert call(f, PosOrKw(a=1, required=True)) == {'a': 1}
    assert call(f, KwOnly(a=1, required=True)) == {'a': 1}

    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True))

    # 2 arguments:
    assert call(f, PosOnly(1), PosOnly(2)) == {}
    assert call(f, PosOnly(1), PosOrKw(b=2)) == {'b': 2}
    assert call(f, PosOnly(1), KwOnly(b=2)) == {'b': 2}
    assert call(f, PosOrKw(a=1), PosOrKw(b=2)) == {'a': 1, 'b': 2}
    assert call(f, PosOrKw(a=1), KwOnly(b=2)) == {'a': 1, 'b': 2}
    assert call(f, KwOnly(a=1), KwOnly(b=2)) == {'a': 1, 'b': 2}

    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2)) == {'a': 1, 'b': 2}
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2)) == {'a': 1, 'b': 2}
    assert call(f, KwOnly(a=1, required=True), KwOnly(b=2)) == {'a': 1, 'b': 2}

    assert call(f, PosOrKw(a=1, required=True), PosOrKw(b=2, required=True)) == {'a': 1, 'b': 2}
    assert call(f, PosOrKw(a=1, required=True), KwOnly(b=2, required=True)) == {'a': 1, 'b': 2}
    assert call(f, KwOnly(a=1, required=True), KwOnly(b=2, required=True)) == {'a': 1, 'b': 2}

    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOnly(2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOrKw(b=2))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), KwOnly(b=2))

    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOnly(2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), PosOrKw(b=2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOnly(1, required=True), KwOnly(b=2, required=True))

def test_call_int():
    # `inspect.signature` doesn't work for some built-in functions, like `int`.  
    # See python/cpython#107161 for more details.  In such cases, the best we 
    # can do is to pass all the required arguments.

    # 0 arguments:
    assert call(int) == 0

    # 1 argument:
    assert call(int, PosOnly(1)) == 0  # [1]
    assert call(int, PosOnly(1, required=True)) == 1

    assert call(int, PosOrKw(x=1)) == 0  # [1]
    assert call(int, PosOrKw(x=1, required=True)) == 1

    assert call(int, KwOnly(x=1)) == 0

    with pytest.raises(TypeError):
        call(int, KwOnly(x=1, required=True))

    # 2 arguments:
    # Note that `int` actually can take two arguments, but only if the first is 
    # a string (in which case the second is the base).
    with pytest.raises(TypeError):
        call(int, PosOnly(1, required=True), PosOnly(2, required=True))
    with pytest.raises(TypeError):
        call(int, PosOnly(1, required=True), PosOrKw(x=2, required=True))
    with pytest.raises(TypeError):
        call(int, PosOnly(1, required=True), KwOnly(x=2, required=True))
    with pytest.raises(TypeError):
        call(int, PosOrKw(x=1, required=True), PosOrKw(y=2, required=True))

    # [1] Although we specified 1 as a positional argument, it wasn't used 
    #     because we can't confirm that the function accepts any positional 
    #     arguments, so we get the default 0 value.

def test_call_partial():
    from functools import partial

    def f(a, b):
        return a, b

    # If we invoke `partial` with a positional argument, then we can add more 
    # positional arguments after it.  Otherwise we can't.

    g1 = partial(f, 1)

    assert call(g1, PosOnly(2)) == (1, 2)
    assert call(g1, PosOrKw(b=2)) == (1, 2)
    assert call(g1, PosOrKw(c=2)) == (1, 2)
    assert call(g1, KwOnly(b=2)) == (1, 2)

    g1 = partial(f, a=1)

    assert call(g1, PosOrKw(b=2)) == (1, 2)
    assert call(g1, KwOnly(b=2)) == (1, 2)

    with pytest.raises(TypeError):
        call(g1, PosOnly(2))
    with pytest.raises(TypeError):
        call(g1, PosOrKw(c=2))

def test_call_err_wrong_arg_type():

    def f(a, b): pass

    with pytest.raises(TypeError):
        call(f, 1, 2)

def test_call_err_out_of_order():

    def f(a, b): pass

    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1), PosOnly(2))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1), PosOrKw(b=2))

def test_call_err_duplicate_kw():

    def f(a, b): pass

    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1), PosOrKw(a=2))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1), KwOnly(a=2))
    with pytest.raises(TypeError):
        call(f, KwOnly(a=1), KwOnly(a=2))

def test_call_err_required_after_non_required():

    def f(a, b): pass

    with pytest.raises(TypeError):
        call(f, PosOnly(1), PosOnly(2, required=True))
    with pytest.raises(TypeError):
        call(f, PosOrKw(a=1), PosOrKw(b=2, required=True))

def test_repr():
    assert repr(PosOnly(1)) == 'PosOnly(1)'
    assert repr(PosOrKw(a=1)) == 'PosOrKw(a=1)'
    assert repr(KwOnly(a=1)) == 'KwOnly(a=1)'

    assert repr(PosOnly(1, required=True)) == 'PosOnly(1, required=True)'
    assert repr(PosOrKw(a=1, required=True)) == 'PosOrKw(a=1, required=True)'
    assert repr(KwOnly(a=1, required=True)) == 'KwOnly(a=1, required=True)'
