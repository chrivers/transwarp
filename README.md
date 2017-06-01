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

Any line that has `##` as the first non-whitespace contents, is
regarded as a comment line, and will be completely ignored.

There are exactly 4 kinds of "things" in stf files:

 - blocks
 - fields
 - types
 - constants

There are no reserved words, and no identifiers have special
meanings. Let's discuss each of them in more detail.

### Constants ###

A constant is simple to define. The syntax is the following:

 `name = 0x{hexvalue}`

The name can consist of all alphanumeric characters, and the integer
must be in hex format. Here's an example of a list of constants:

```ruby
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

```ruby
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

```
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

Now that we have the basic kinds of content explained, let's see how
we can group it together to make it more useful.

### Blocks ###

A block is, in essence, a namespace for a group of things. Think of it
as a container with a name you can refer to.

Here's an example of the block syntax:

```ruby
expr name
    const1 = 0x01
    const2 = 0x02
    const3 = 0x03
    ...

    field1: type1
    field2: type2<foo>
    field3: type3<a, b, c>
    ...
```

There's a few things going on here, so let's take a look at them one at a time.

First of all, you start a block by writing 2 names on a line, with any
amount of whitespace in between. The `name` part is used to refer to
the block from the templates, and `expr` is any kind of descriptive
word you like, to give your templates something some more
information. For instance, you might like to refer to a block as an
`enum`, a `struct` a `class`, or something like that. But you could
just as well have a `document`, a `protocol` or a `spaceship`.

Second, we can see that blocks contain any number of constants and
fields. These follow the exact syntax described earlier, so there
should be no surprises here. It is customary (but not enforced) to put
constants first, and fields later, although having blocks with both
constants and fields is a uncommon in practice.

Third, you need to put *exactly 4 spaces* in front of all content that
goes in a block, to mark it as being part of that block. This is a
little rigid, and could maybe be relaxed in a future stf
specification, but for now it's always 4 spaces.

Finally, you should know that only the header (expr + name) is
mandatory - blocks do not have to have any constants or fields at
all. Also, you can put blocks inside blocks (.. inside blocks,
etc). As you have probably guessed by now, stf is not going to tell
you how to structure your data. Of course, you add 4 more spaces for
each additional level of nesting.

That was a bit of a mouthful, so let's take a look at some valid blocks:

```ruby
enum MediaCommand
    Delete   = 0x00
    Play     = 0x01
    Create   = 0x02
```

Here we have a block with the name `MediaCommand` and the expr
`enum`. It contains 3 constants, named `Delete`, `Play` and `Create`.

Let's see a slightly more complex example:

```ruby
struct PlayerShipUpgrades
    mask_bytes = 11

    active: map<UpgradeType, bool8>
    count: map<UpgradeType, i8>
    time: map<UpgradeType, u16>
```

This is a block with the name `PlayerShipUpgrades` and expr
`struct`. It contains 1 constant, `mask_bytes` and 3 fields, `active`,
`count` and `time`.

Finally, let's take a look at an example of nested blocks:

```ruby
packet ServerPacket

    struct AllShipSettings
        ships: map<ShipIndex, ShipV240>

    struct BeamFired
        id: i32
```

In this example, our `ServerPacket` block contains 2 blocks, named
`AllShipSettings` (which contains the field `ships`) and `BeamFired`
(which contains the field `id`), respectively.

Now that you know how blocks, fields, types and constants work, you
are free to combine them in any way you like!

## Advanced features ##

There are a few advanced features available, designed to make the
format easier and more powerful to work with. Let's go through all
three of them here, and afterwards you will know everything there is
to know about the format!

### Doc comments ###

Making comments in the stf files is not a bad idea, but what if you'd
like to use access your descriptions and examples from inside the
templates? No problem, you simply need to mark a comment with `#` (doc
comment) instead of `##` (regular comment). Lines marked when `#` will
NOT be ignored by the compiler, but will instead have their text
contents appended to the next item. Here are some examples:

```ruby
## this line is completely ignored by the compiler

## the next line is a doc comment (but this line is not)
# this enum is super important, because reasons
enum VeryImportant
  Wow = 0x10
  NotWow = 0x20

# this struct is less important than the enum
struct LessImportant

  ## You can also add docs for constants and fields, of course!
  ## this is demonstrated below

  # compared to VeryImportant, this is definitely not as good
  KindOfWow: bool

  # remember to do that thing here, because of...
  ## you can inject normal comments in the middle of doc comments too
  ## and it will work as expected (be ignored)
  # ..the reasons for doing it
  NoBigDeal: u32
```

To summarize: Like normal comments, doc comments do nothing on their
own, but unlike normal comments, they are available to the templates,
meaning you can use them to provide descriptions for your items, for
example by converting them into comments in whatever target language
your templates generate.

## Licence ##

This project is licences under the GNU [General Public
Licence](https://www.gnu.org/licenses/gpl-3.0.txt) (GPL) Version 3.

## Etymology ##

In the Star Trek universe, *Transwarp* refers to speeds faster than
Warp 10. This is the theoretical warp speed limit, much the like the
speed of light is limit in our universe.
