import torch


def test_torch_tensor_operation() -> None:
    values = torch.tensor([1.0, 2.0, 3.0])
    assert values.sum().item() == 6.0


def test_project_import() -> None:
    import src

    assert src.__doc__
