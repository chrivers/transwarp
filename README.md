# Transwarp #

Transwarp helps you describe protocol formats, and automatically
generate corresponding code, documentation, test cases, or whatever
you like! Your documentation will never be outdated again!

The input data format is simple, and very easily extensible. It only
enforces the most basic structure - you decide the rest!

## Getting started ##

To use transwarp, you need a protocol description, and a corresponding
template (or set of templates). The transwarp compiler parses all
input files, and generates the output from your templates.

After all input files are parsed, the data is put into a tree
structure, which is made available for the templates to
introspect. Since the templates are completely in charge of the
output, there are no requirements for how (or how much) you have to
use the available data. More importantly, you can start by making your
existing source files into templates, and slowly build conversion
logic into them!

## Input data format ##

The input data format, boringly named Standard Type Framework (.stf),
is a simple text-based format, designed to be easily human-readable
while still being parsable.

There are a few different types of sections, that can be used to
describe different structures of data.

### enum ###

With the enum section, you can describe a collection of constants. It
is up to the template to use this information later, so there's no
requirement that your target language has an "enum" type.

```java
enum ShipSystem
    Beams                = 0x00
    Torpedoes            = 0x01
    Sensors              = 0x02
    Maneuvering          = 0x03
    Impulse              = 0x04
    WarpDrive            = 0x05
    ForeShields          = 0x06
    AftShields           = 0x07
```

