"""Тридцять наборів даних з карток (відкриті приклади): запускайте лише свій, наприклад pytest -k v13."""
import inspect

import pytest
from conftest import load
from cases import SETS


def _params():
    return [pytest.param(number, run, id=f"v{index + 1:02d}")
            for index, (number, label, run) in enumerate(SETS)]


@pytest.mark.parametrize("number,run", _params())
def test_набір_з_картки(number, run, tmp_path):
    module = load(number)
    if "tmp_path" in inspect.signature(run).parameters:
        run(module, tmp_path)
    else:
        run(module)
