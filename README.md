# gflags2argparse
Convert gflags help message into argparse help message

# Usage

Show [gflags](https://github.com/gflags/gflags) help message.

```
./your_prog --help | python gflags2argparse.py
```

Use [genzshcomp](https://pypi.python.org/pypi/genzshcomp) to generate zsh completion.

```
./your_prog --help | python gflags2argparse.py | genzshcomp \
  > (directory in $fpath)/_your_prog
```
