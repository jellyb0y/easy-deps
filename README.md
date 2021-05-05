# easy-deps

Package manager for python based on `pip3`  
Solve the main problem of pip - ~~fucking~~ horrible deps.  

*Just try it, and you will understand it.*

All your project config and deps will store in `.ezdeps.json` like this:

```
{
    "name": "ezdeps",
    "version": "1.0.4",
    "description": "Package manager for python",
    "documentation_path": "./README.md",
    "author": {
        "name": "Vitaly Kisel <jellyb0y>",
        "email": "kisel@internet.ru"
    },
    "scripts": [
        "./scripts/ezdeps"
    ],
    "dependencies": {
        "pip": "^20.0.0",
        "wheel": "0.36.2",
        "twine": "3.4.1"
    },
    "dev_dependencies": {},
    "python_requires": ">=3.8",
    "classifiers": [
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    "include_package_data": true
}

```

You don't more need use `setuptools`, it is already in it.

## install

Install package: `pip install ezdeps`

## Usage

Common usage:  
`ezdeps <command> [options] [packages]`

Commands:  
- `install` - Install packages  
    - options:
        - `<-S | --default>? [packages, ...]`       Install packages to default dependencies
        - `<-D | --development> [packages, ...]`    Install packages to dev_dependencies
        - `<-A | --all>`                            Install packages from dependency list `.ezdeps.json`

- `uninstall` - Uninstall packages
    - options:
        - `[packages, ...]`                         Uninstall packages from deps

- `update` - Update packages
    - options:
        - `[packages, ...]`                         Update packages in deps

- `build` - Build package

- `publish` - Publish packages
    - options:
        - `<-C | --clear>`                          Clear temp files after publishing
        - `<-R | --repository>`                     Set up repository name in your `.ezdepsrc`
        - `<--repository-url> [url]`                Set up repository url
        - `<--username> [username]`                 Set up registry username
        - `<--password> [password]`                 Set up registry password

## Using `.ezdepsrc`

To store your keys and tokens you have to create `~/.ezdepsrc` file:  

```
[gitlab.com]
USER=myuser # Test user for gitlab regitsry
PASSWORD=topsecret # Test passwd for gitlab regitsry

[github.com]
USER=myuser # Test user for github regitsry
PASSWORD=topsecret # Test passwd for github regitsry
REPOSITORY_URL=https://example.com/ # regitsry url for github (optional)
REPOSITORY_NAME=github # regitsry name (optional) to rewrite `github.com` to `github`
e (optional) to rewrite `github.com` to `github`

```
