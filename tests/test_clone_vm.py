# tests/test_clone_vm.py

from scripts import clone_vm


# 'monkeypatch' is a special pytest tool to safely modify things for a test.
# Here, we use it to simulate command-line arguments.
def test_parsing_with_all_arguments(monkeypatch):
    """
    Tests if the script correctly parses a command with all arguments.
    """
    # Simulate the user typing: python clone_vm.py my-test-pi --ram 2048 --cpus 2 --disk-size 32
    monkeypatch.setattr(
        "sys.argv",
        [
            "clone_vm.py",
            "my-test-pi",
            "--ram",
            "2048",
            "--cpus",
            "2",
            "--disk-size",
            "32",
        ],
    )

    # We will create a function called 'parse_arguments' in clone_vm.py
    args = clone_vm.parse_arguments()

    assert args.name == "my-test-pi"
    assert args.ram == 2048
    assert args.cpus == 2
    assert args.disk_size == 32


def test_parsing_with_only_required_name(monkeypatch):
    """
    Tests if the script works with only the required name argument and sets
    optional arguments to None.
    """
    # Simulate the user typing: python clone_vm.py my-minimal-pi
    monkeypatch.setattr("sys.argv", ["clone_vm.py", "my-minimal-pi"])

    args = clone_vm.parse_arguments()

    assert args.name == "my-minimal-pi"
    assert args.ram is None
    assert args.cpus is None
    assert args.disk_size is None


def test_parsing_with_some_arguments(monkeypatch):
    """
    Tests if the script correctly parses a mix of provided and omitted arguments.
    """
    # Simulate the user typing: python clone_vm.py my-ram-pi --ram 4096
    monkeypatch.setattr("sys.argv", ["clone_vm.py", "my-ram-pi", "--ram", "4096"])

    args = clone_vm.parse_arguments()

    assert args.name == "my-ram-pi"
    assert args.ram == 4096
    assert args.cpus is None
    assert args.disk_size is None
