# -*- coding: utf-8 -*-

"""Mediator tests
"""
import pytest

from ordnung.core.components.mediator import Mediator


@pytest.fixture()
def inst():
    return Mediator()


def test_binding(inst):
    assert 'something' not in inst
    something = object()
    inst.register('something', something)
    assert 'something' in inst
    inst.unregister('something')
    assert 'something' not in inst


def test_double_adding(inst):
    something = object()
    inst.register('something', something)
    assert inst.get('something') is something

    with pytest.raises(NameError):
        inst.register('something', something)


def test_nonexistent(inst):
    with pytest.raises(NameError):
        inst.unregister('something')

    something = object()
    inst.register('something', something)
    assert inst.get('something') is something


def test_str(inst):
    assert str(inst) == 'Mediator()'
    assert repr(inst) == 'Mediator(allow_overwrite=False)'

    inst.register('something1', 1)
    inst.register('something2', 2)
    inst.register('something3', 3)

    assert str(inst) == 'Mediator("something1", "something2", "something3")'
    assert repr(inst) == 'Mediator(allow_overwrite=False)'

    inst.register('something4', 4)

    assert str(inst) == 'Mediator(len=4, "something1", ..., "something4")'
    assert repr(inst) == 'Mediator(allow_overwrite=False)'


def test_clear(inst):
    inst.register('something1', 1)
    inst.register('something2', 2)
    inst.register('something3', 3)

    assert 'something1' in inst
    assert len(inst) == 3

    inst.clear()

    assert inst.get('something1') is None
    assert 'something1' not in inst
    assert len(inst) == 0


def test_internals(inst):
    object_1 = object()
    object_2 = object()
    object_3 = object()

    inst.register('a', object_1)
    inst.register('b', object_2)
    inst.register('c', object_3)

    assert len(inst) == 3

    assert list(inst.keys()) == ['a', 'b', 'c']
    assert list(inst.values()) == [object_1, object_2, object_3]
    assert list(inst.items()) == [('a', object_1),
                                  ('b', object_2),
                                  ('c', object_3)]


def test_get_item(inst):
    object_1 = object()
    inst.register('a', object_1)
    assert inst['a'] is object_1

    with pytest.raises(KeyError):
        _ = inst['unknown']


def test_iter(inst):
    object_1 = object()
    object_2 = object()
    object_3 = object()

    inst.register('a', object_1)
    inst.register('b', object_2)
    inst.register('c', object_3)

    for res, (key, value) in zip(inst, [('a', object_1),
                                        ('b', object_2),
                                        ('c', object_3)]):
        assert res == key
        assert inst[key] is value


def test_wrong_type(inst):
    inst.register('a', object())
    with pytest.raises(TypeError):
        inst.register(None, 'something')


def test_populate(inst):
    assert not inst.keys()

    inst.populate(key1=object(), key2=object())
    assert 'key1' in inst
    assert 'key2' in inst


def test_getattr(inst):
    assert not hasattr(inst, 'one')
    inst.register('one', 1)
    assert inst.one == 1
    assert hasattr(inst, 'one')
    inst.unregister('one')
    assert not hasattr(inst, 'one')
