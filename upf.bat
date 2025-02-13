cls
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q mcsl_lib.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*