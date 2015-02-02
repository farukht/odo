from into.backends.text import (TextFile, resource, convert, discover, append,
        drop, chunks)
from into.utils import tmpfile, filetexts, filetext
from datashape import dshape
import os


def test_resource():
    assert isinstance(resource('foo.txt'), TextFile)
    assert isinstance(resource('/path/to/foo.log'), TextFile)


def test_convert():
    with filetext('Hello\nWorld') as fn:
        assert convert(list, TextFile(fn)) == ['Hello\n', 'World']


def test_append():
    with tmpfile('log') as fn:
        t = TextFile(fn)
        append(t, ['Hello', 'World'])

        assert os.path.exists(fn)
        with open(fn) as f:
            assert list(map(str.strip, f.readlines())) == ['Hello', 'World']


def test_discover():
    assert discover(TextFile('')) == dshape('var * string')


def test_drop():
    with filetext('hello\nworld') as fn:
        t = TextFile(fn)
        assert os.path.exists(fn)
        drop(t)
        assert not os.path.exists(fn)


def test_chunks_textfile():
    with filetexts({'a1.log': 'Hello\nWorld', 'a2.log': 'Hola\nMundo'}) as fns:
        logs = chunks(TextFile)(list(map(TextFile, fns)))
        assert set(map(str.strip, convert(list, logs))) == \
                set(['Hello', 'World', 'Hola', 'Mundo'])
