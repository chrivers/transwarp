# Transwarp #

Transwarp is a user-friendly compiler, that takes specification (in
the form of `*.stf` files) as input, and helps you generate code,
documentation, test cases, or whatever you like! Your documentation
will never be outdated again!

You can use `stf` files to describe protocols, data format, parsers,
or pretty much anything that deals with structured data. The output
can be source code, documentation, or any other user- or
machine-readable thing you write a template for.

The input data format is simple, and very easily extensible. It only
enforces the most basic structure - you decide the rest!

## Overview ##

```
+--------------------------+                                +-------------------------+
|                          |  Templates can load plugins    |                         |
|  Template files (*.tpl)  <--------------------------------+ Compiler plugins (*.py) |
|                          |                                |                         |
+-+------------------------+                                +-------------------------+
  |
  | Compiler loads templates  +----------------------+
  +--------------------------->                      |  Compiler writes output
                              |  Transwarp Compiler  +-------------------------+
  +--------------------------->                      |                         |
  | Compiler loads stf files  +----------------------+                         |
  |                                                                            |
+-+------------------------+                                +------------------v------+
|                          |                                |                         |
|    Source files (*.stf)  |                                |    Generated content    |
|                          |                                |                         |
+--------------------------+                                +-------------------------+
```

To use transwarp, you need a specification, and a corresponding
template (or set of templates). The transwarp compiler parses all
input files, and generates the output from your templates.

After all input files are parsed, the data is put into a tree
structure, which is made available for the template code to inspect
and transform. Since the templates are completely in charge of the
output, there are no requirements for how (or how much) you have to
use the available data. More importantly, you can start by making your
existing source files into templates, and slowly build conversion
logic into them!

The widely used, well-tested and well-documented [Mako
template](http://www.makotemplates.org/) system is used for templating.

## Quick start example ##

Okay, so you want to try out transwarp! Let's take a look at
generating parser code and templates for the Artemis Space Bridge
Simulator game.

Here's what you need:

 0. python 3
 0. The transwarp compiler (https://github.com/chrivers/transwarp)
 0. A protocol specification (for example, https://github.com/chrivers/isolinear-chips)
 0. Templates for that protocol (for example, https://github.com/chrivers/duranium-templates)

```bash
# download and install transwarp
$ git clone https://github.com/chrivers/transwarp
$ cd transwarp
$ ./setup.py -q install # use sudo if you want to install system-wide
$ cd ..

# as an example, get artemis protocol spec
$ git clone https://github.com/chrivers/isolinear-chips isolinear

# as an example, get rust code templates
$ git clone https://github.com/chrivers/duranium-templates duranium

# to see the complete set of options:
$ transwarp --help
```

If you get a list of commend line arguments, transwarp is installed
correctly. Otherwise, please open an issue so we can fix the problem.

Now we are ready to compile!
```bash
# let's see a summary of what transwarp would like to compile
$ transwarp -D isolinear/protocol -I duranium/templates -L duranium/lib -O output-dir -s
[*] Will create:
    output-dir/client/mod.rs
    output-dir/client/reader.rs
    output-dir/client/writer.rs
    output-dir/enums.rs
    output-dir/maps.rs
    output-dir/server/mod.rs
    output-dir/server/object.rs
    output-dir/server/reader.rs
    output-dir/server/update.rs
    output-dir/server/writer.rs
    output-dir/structs.rs
    ...
```

Let's do a quick breakdown of the arguments here:

```-D isolinear-chips/protocol```

This points transwarp to the protocol specification. From this
directory, all `*.stf` files are loaded. The files are always loaded
in alphabetical order, for consistency between runs. The templates
will have access to each file, as a variable with the filename
(without extension), prefixed by underscore.

Example: `protocol.stf`, will be available as `_protocol` in the
templates.

```-I duranium-templates/templates```

Here we point transwarp to the templates. This directory is
*recursively* scanned for templates, to be generated. The default
template file extension is `.tpl`, but this can be changed with the
--extension (-e) option. For each input template, an output file will
be generated in the output dir, except for the `.tpl` extension.

Example: `server/writer.rs.tpl` will be output to `server/writer.rs`.

```-L duranium-templates/lib```

Templates can load python code into the templates, which advanced
templates can use to do more serious data processing. The duranium
templates (which generate rust code), use a single such plugin
module. This is not strictly required, but makes the template code
cleaner, since some repeated functionality can easily be shared in one
place.

Simpler templates, such as documentation generators, wouldn't have to
use any plugins at all. It is very reasonable to write self-contained
templates.

```-O output-dir```

Here we set the output directory. The relative path of the input file
from the input-dir is used as the output file name.

```-s (summarize)```

Transwarp defaults to showing a diff (like `git diff`), but since the
files have not been initially generated yet, this would produce a very
large amount of output. To avoid this, we use `-s` to produce only a
list of changes.


If we agree with the summary, we can write all the files by appending
`-u` (update mode):

```
$ transwarp -D isolinear/protocol -I duranium/templates -L duranium/lib -O output-dir -u
[*] Updated output-dir/server/mod.rs
[*] Updated output-dir/structs.rs
[*] Updated output-dir/server/object.rs
[*] Updated output-dir/server/writer.rs
[*] Updated output-dir/client/writer.rs
[*] Updated output-dir/client/reader.rs
...
```

Transwarp looks at the modification time of both stf files and
template files, and tries to only update changed files, so if we run
it again, we can see we are synchronized:

```
$ transwarp -D isolinear/protocol -I duranium/templates -L duranium/lib -O output-dir -u
[*] All templates up-to-date
```

## Command examples ##

Render templates from "foo" into "bar":

```
$ transwarp -I foo -O bar -u
```

Summarize changes caused by rendering templates from "src" into current dir:

```
$ transwarp -D someproto -I src -s
```

Show diff caused by rendering templates from current dir (recursively) into "target":

```
$ transwarp -D myspec -O target
```

Enable verbose mode to explain what is going on behind the scenes:

```
$ transwarp -D data -I template_dir -O output_dir -v
```

Enable quiet mode to compile from build scripts without unnecessary output:

```
$ transwarp -D specfiles -I ../templates -O src/protocol-parser/ -q
```

## STF specifications ##

The input data format, the Simple Type Framework (.stf), is
a user-friendly text-based format, designed to be easily
human-readable while still being parsable.

There are *no keywords* in stf, only a few different types of
structure. The stf files describe a data structure, which is then used
by the template in whatever manner they wish. This leaves you in
charge of how to structure and organize your specification data.

There are exactly 4 kinds of "things" in stf files:

 - blocks
 - fields,
 - constants
 - types

There are no reserved words, and no identifiers have special
meanings. Let's discuss each of them in more detail.

### Constants ###

A constant is simple to define. The syntax is the following:

 `name = 0x{hexvalue}`

The name can consist of all alphanumeric characters, and the integer
must be in hex format. Here's an example of a list of constants:

```r
InfusionPCoils        = 0x00
HydrogenRam           = 0x01
TauronFocusers        = 0x02
CarapactionCoils      = 0x03
PolyphasicCapacitors  = 0x04
CetrociteCrystals     = 0x05
```

That's all you need to know about constants.

### Fields ###

If you need to store something that isn't an integer constant, you'll
want to use a field. The syntax is:

 `name : type`

Notice that we use `:` instead of `=`. That's what separates fields
from constants! In the next section, we will take a look at how types
work, but here are some examples of fields for now:

```yaml
index: u32
vessel_type_id: u32
x_coordinate: f32
y_coordinate: f32
z_coordinate: f32
pitch: f32
```

As you can probably surmise, "u32" and "f32" are valid types. But
remember, there *are no* built-in types, keywords, or reserved
identifiers in stf! In fact, all simple strings are valid type
names. It is up to you (in the templates) to give these names meaning!

But types can do more, when you need them to. We'll take a closer look
in the next section.

### Types ###

As we saw in the previous section, any string of alphanumeric
characters is a valid type: However, types have a powerful feature:
*type arguments*. Any type can have type argument, and they are
written in angle brackets, like so:

`type<arg1, arg2, ...>`

All type arguments are, themselves, types! This means that your type
arguments can have type arguments, which can have.. you get the
idea. Types are really just a compact way to describe a tree structure
with named nodes.

If a type is not followed by angle brackets, it has 0 type
arguments. Here are some examples of valid types:

```yaml
f32
u32
string
GameMasterButton<u8>
DriveType<u8>
map<ShipSystem, f32>
map<TubeIndex, TubeStatus<u8>>
```

Again, *none* of these examples assume anything about the names given,
and it is completely up to you to pick the names you would like to
use. It is syntactically valid to construct a type called
`u32<bool<string<with_milk>>>`, but it might be harder to come up with
a reasonable explanation for what it *means*. But that's your job ;-)



### Blocks ###

A block is, in essence, a namespace. Think of it as a container you
can put things into.

 -

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

## Licence ##

This project is licences under the GNU [General Public
Licence](https://www.gnu.org/licenses/gpl-3.0.txt) (GPL) Version 3.

## Etymology ##

In the Star Trek universe, *Transwarp* refers to speeds faster than
Warp 10. This is the theoretical warp speed limit, much the like the
speed of light is limit in our universe.
