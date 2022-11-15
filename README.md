# microblog

An online broadcast medium.

## How-Tos

### Precursive

Clone the repository to your local machine via HTTPS:

```bash
$ git clone https://github.com/jamespatrickryan/microblog.git
```

Navigate to the directory through its relative path:

```bash
$ cd microblog
```

Execute the `venv` module as a script to initiate a [virtual environment](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.):

```bash
$ python -m venv venv
```

Activate it:

```bash
$ source venv/Scripts/activate
```

Install the dependencies:

```bash
(venv)
$ pip install -r requirements.txt
```

### Initialize the Database File

Like so:

```bash
$ flask --app microblog initialize-database
```

### Application

```bash
$ flask --app microblog --debug run
```
