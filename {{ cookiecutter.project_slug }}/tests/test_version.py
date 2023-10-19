import tomllib
import pathlib
import {{ cookiecutter.project_slug }}


def test_version():
    path = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(open(str(path)).read())
    pyproject_version = pyproject["tool"]["poetry"]["version"]

    package_init_version = {{ cookiecutter.project_slug }}.__version__

    assert package_init_version == pyproject_version