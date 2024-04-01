# Simple-XSS

<p align="center">
  <img src="resources/images/logo.png"  alt="Simple-XSS logo"/>
</p>

<p align="center">
    <a href="https://github.com/CrazyProger1/Simple-XSS/releases/download/V0.0.3/Simple-XSS-Windows-x64.zip"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/CrazyProger1/Simple-XSS/total"></a>
    <a href="https://github.com/CrazyProger1/Simple-XSS/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/CrazyProger1/Simple-XSS"></a>
    <a href="https://github.com/CrazyProger1/Simple-XSS/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/CrazyProger1/Simple-XSS"></a>
</p>

Simple-XSS is a multi-platform cross-site scripting (XSS) vulnerability exploitation tool for pentesting.

Problems solved by Simple-XSS:

- [x] Easy creatable payloads & hooks
- [x] Support of several transport services (HTTP, Websocket)
- [x] Support of several tunneling services (to deliver payload even without white IP)

**Disclaimer:** This program is provided for educational and research purposes only.
The creator of this program does not condone or support any illegal or malicious activity,
and will not be held responsible for any such actions taken by others who may use this program.
By downloading or using this program, you acknowledge that you are solely responsible for any consequences
that may result from the use of this program.

## Documentation

See **[docs](./docs/README.md)**

## Status

**V0.0.3 - released**

## Interface

### Graphical

![v0.0.3](resources/images/v0.0.3.png)

## Warning

In favor of ease of use and expanded capabilities, we had to sacrifice backward compatibility between versions 0.2 and
0.0.3. The features of the previous version are retained and expanded, but older versions of hook & payload will not
work.

## Installation

**Note:** _make sure you have installed [Python 3.12](https://www.python.org/) or higher._

First you need to clone the repository:

```commandline
git clone https://github.com/CrazyProger1/Simple-XSS
```

Then go to the folder & install the requirements:

**For Window:**

```commandline
cd Simple-XSS
pip install -r requirements/windows.txt
```

**For Linux:**

```commandline
cd Simple-XSS
pip install -r  requirements/linux.txt
```

And finally you can launch it:

```commandline
python simplexss
```

## License

Simple-XSS is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
