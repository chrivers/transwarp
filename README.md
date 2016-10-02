# Transwarp #

Transwarp helps you describe protocol formats, and automatically
generate corresponding code, documentation, test cases, or whatever
you like! Your documentation will never be outdated again!

The input data format is simple, and very easily extensible. It only
enforces the most basic structure - you decide the rest!

## Overview ##

```
+--------------------------+                                +---------------------+
|                          |  Templates can load plugins    |                     |
|  Template files (*.tpl)  <--------------------------------+  Compiler plugins   |
|                          |                                |                     |
+-+------------------------+                                +---------------------+
  |
  | Compiler loads templates  +----------------------+
  +--------------------------->                      |  Compiler writes output
                              |  Transwarp Compiler  +-------------------------+
  +--------------------------->                      |                         |
  | Compiler loads stf files  +----------------------+                         |
  |                                                                            |
+-+------------------------+                                +------------------v--+
|                          |                                |                     |
|    Source files (*.stf)  |                                |  Generated content  |
|                          |                                |                     |
+--------------------------+                                +---------------------+
```

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

## Quick start ##

Okay, so you want to try out transwarp! Here's what you need:

 0. python 3
 0. The transwarp compiler (https://github.com/chrivers/transwarp)
 0. A protocol specification (for example, https://github.com/chrivers/isolinear-chips)
 0. Templates for that protocol (for example, https://github.com/chrivers/duranium-templates)

```bash
# download and install transwarp
$ git clone https:/a/github.com/chrivers/transwarp
$ cd transwarp
$ ./setup.py install # use sudo if you want to install system-wide

# as an example, get artemis protocol spec
$ git clone https://github.com/chrivers/isolinear-chips protocol

# as an example, get rust code templates
$ git clone https://github.com/chrivers/duranium-templates templates
```

## STF specifications ##

The input data format, boringly named Simple Type Framework (.stf), is
a user-friendly text-based format, designed to be easily
human-readable while still being parsable.

There are a few different types of sections, that can be used to
describe different structures of data.

### Enum ###

With the enum section, you can describe a collection of constants. It
is up to the template to use this information later, so there's no
requirement that your target language has an "enum" type.

```capnp
enum ShipSystem
    Beams         = 0x00
    Torpedoes     = 0x01
    Sensors       = 0x02
    Maneuvering   = 0x03
    Impulse       = 0x04
    WarpDrive     = 0x05
    ForeShields   = 0x06
    AftShields    = 0x07
```

### Flags ###

If you want to describe bitflags rather than an enum, you can use the
"flags" section. The syntax and format is exactly identical to enums,
but the templates have access to them in a separate node of the data
structure.

```capnp
flags EliteAbilities
    STEALTH             = 0x0001
    LOWVIS              = 0x0002
    CLOAK               = 0x0004
    HET                 = 0x0008
    WARP                = 0x0010
    TELEPORT            = 0x0020
    TRACTOR             = 0x0040
```

### Struct ###

Next up, we have the "struct" section type. Each struct is simply a
list of fields (name, type), with an optional comment, like so:

```capnp
struct SystemNodeStatus
    # The X coordinate of the node relative to the ship's center.
    x_coordinate: u8

    # The Y coordinate of the node relative to the ship's center.
    y_coordinate: u8

    # The Z coordinate of the node relative to the ship's center.
    z_coordinate: u8

    # The current damage level for this node. An undamaged node has a
    # value of 0.0; any higher value indicates damage.
    damage: f32
```

Here we see a struct with 4 fields, each with a simple (primitive)
type. STF attached no particular meaning to these type names, however!
That work is entirely left up to the user. There is also no limitation
on type names, as long as they are grammatically valid.

### Object ###

Sometimes, it is useful to attach data to structures, without putting
it in a comment, or having it as a formal field. In this case, one can
use the "object" section type:

```capnp
## bit mask size is 2
object Torpedo(2)
    # X coordinate (bit 1.1, float)
    # The torpedo's location on the X axis.
    x_coordinate: f32

    # Y coordinate (bit 1.2, float)
    # The torpedo's location on the Y axis.
    y_coordinate: f32

    # Z coordinate (bit 1.3, float)
    # The torpedo's location on the Z axis.
    z_coordinate: f32
```

In this example, a `Torpedo` object is defined, with the parameter
`2`. Except for the definition line, the syntax for `object` is
exactly equal to `struct`

### Packets ###

One of the last section types is `packet`, which is the only section
type that has two levels. It allows you to describe a multiple-choice
type situation, where each individual case works like a struct. It
looks like this:

```capnp
packet ClientPacket
    ActivateUpgrade
        # The upgrade to activate. The game is prepared for 28 (30?)
        # different types of powerups, but only 8 are available as
        # of Artemis 2.4.
        target: enum<u32, UpgradeActivation>

    AudioCommand
        # The ID for the audio message. This is given by the
        # IncomingAudioPacket.
        audio_id: i32

        # The desired action to perform.
        audio_command: enum<u32, AudioCommand>

    CaptainSelect
        # The object ID for the new target, or 1 if the target has been cleared.
        target_id: i32
```

Here we see a packet definition for `ClientPacket`, with 3 cases. Each
case is then specified just like a `struct`.

### Parsers ###



### Types ###
